from django import http

from django import http
from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test, permission_required
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_protect

from finch.models import Page
from finch.forms import PageForm
from finch.signals import url_changed

from datetime import datetime

# The csrf_protect decorator is required here because this view is not
# covered by csrfviewmiddleware because it is only called in a later
# stage in the middleware process (process_response)
@csrf_protect
def view_page(request, urlpath):
    """ Get the page if it's online and the user has access.

    When a request (by non-editors) is made to an offline pages the
    finch returns an Http404 Exception to prevent information
    'leaking'.

    A online page is visible to anyone, logged in or not unless access
    is restricted.

    A(n online) page that is restricted is only accesible to members
    of the selected group(s). When access is denied the (anonymous)
    user is redirected to the login page with the forbidden page's url
    set as the next paramenter.
    if user
    """
    page = get_object_or_404(Page, urlpath=urlpath)
    if not (page.online or request.user.has_perm('finch.change_page')):
        raise http.Http404('Not Found')
    context = RequestContext(request, {'page': page })
    return render_to_response(page.template, context)


@permission_required('finch.add_page')
def create_page(request, pageid):
    page = get_object_or_404(Page, id=pageid)
    if request.POST:
        form = PageForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data['site_id'] =  settings.SITE_ID
            data['created_by'] = request.user
            data['updated_by'] = request.user
            # No longer needed...
            data.pop('parent_page_id')
            newpage = page.add_child(**data)
            if request.is_ajax():
                response = http.HttpResponse('', 'text/plain')
                response['X-Finch'] = newpage.get_absolute_url()
                # This is mostly for automated tests ...
                # The test-client never is_ajax of course but when
                # creating automated tests (using django-viewtester
                # for example) this would (otherwise) generate a 200
                # response code and the test will fail

                # Needs a fix for crap IE browsers that strip the
                # X-Finch when the response code is 302 Assuming
                # no developers worth their salt will use IE to create
                # tests I think this is ok
                if request.META.get('HTTP_USER_AGENT', '').find('MSIE')<0:
                    response.status_code = 302
                return response
            else:
                return http.HttpResponseRedirect(newpage.get_absolute_url())
    else:
        form = PageForm(initial={'parent_page_id':pageid,
                                 'online':page.online
                                 })
    caption = _("Create Childpage")
    action_url = reverse('create_page', args=[page.id])
    if request.is_ajax():
        template = 'finch/ajax.html'
    else:
        template = 'contentmanager/contentmanager_base.html'
    context = RequestContext(request, locals())
    return render_to_response('finch/edit.html', context)


@permission_required('finch.change_page')
def edit_page(request, pageid):
    page = get_object_or_404(Page, id=pageid)
    # Store values in case the url_changed signal needs to be sent
    oldpath = page.get_absolute_url()
    oldtitle = page.title
    if request.POST and request.POST.get('save','') == _('Save'):
        form = PageForm(request.POST, instance=page)
        if form.is_valid():
            form.cleaned_data['updated_by'] = request.user
            page = form.save()
            # TODO: Move this stuff (up till 'is_ajax') to models.py
            # Notify those who care that url to this page has changed
            if 'slug' in form.changed_data:
                url_changed.send(
                    Page,
                    id=page.id,
                    oldpath=oldpath,
                    oldtitle=oldtitle,
                    newpath=page.get_absolute_url(),
                    newtitle=page.title)
            if not page.is_leaf():
                if any([x in form.changed_data for x in ('online')]):
                    page.propagate()
            if request.is_ajax():
                response = http.HttpResponse('', 'text/plain')
                response['X-Finch'] = page.get_absolute_url()
                # This is mostly for tests. See remarks above
                if request.META.get('HTTP_USER_AGENT', '').find('MSIE')<0:
                    response.status_code = 302
                return response
            else:
                return http.HttpResponseRedirect(page.get_absolute_url())
    else:
        form = PageForm(instance=page)
    if page.is_root():
        # Slug is not updatable for a rootpage (it is always '')
        form.fields.pop('slug', None)
    caption = _("Edit Page")
    action_url = reverse('edit_page', args=[page.id])
    if request.is_ajax():
        template = 'finch/ajax.html'
    else:
        template = 'contentmanager/contentmanager_base.html'
    context = RequestContext(request, locals())
    return render_to_response('finch/edit.html', context)


@permission_required('finch.change_page')
def order_pages(request, pageid):
    page = get_object_or_404(Page, id=pageid)
    siblings = page.get_siblings()
    selected = page
    if request.POST:
        sibindex = int(request.POST.get('sibindex', -1))
        try:
            direction = {
                _('Up'):'up',
                _('Down'):'down'
                }[request.POST.get('direction', '')]
        except KeyError:
            return http.HttpResponseBadRequest("400 Bad Request")
        n = siblings.count()
        if sibindex in range(n) and (
            (direction == 'up' and sibindex>0)
            or (direction == 'down' and sibindex<n-1)):
            sib = siblings[sibindex]
            # This way the selected option 'sticks' after the postback
            selected = sib
            if direction == 'up':
                target = siblings[sibindex-1]
                sib.move(target, 'left')
            if direction == 'down':
                target = siblings[sibindex+1]
                sib.move(target, 'right')
    if request.is_ajax():
        template = 'finch/ajax.html'
    else:
        template = 'contentmanager/contentmanager_base.html'
    context = RequestContext(request, locals())
    return render_to_response('finch/order.html', context)


@permission_required('finch.change_page')
def move_page(request, pageid):
    page = get_object_or_404(Page, id=pageid)
    tree = Page.get_tree()
    if request.is_ajax():
        template = 'finch/ajax.html'
    else:
        template = 'contentmanager/contentmanager_base.html'
    context = RequestContext(request, locals())
    return render_to_response('finch/move.html', context)


@permission_required('finch.change_page')
def move_confirm(request, pageid, targetid):
    page = get_object_or_404(Page, id=pageid)
    target = get_object_or_404(Page, id=targetid)

    is_valid = True
    if target.get_children().filter(slug=page.slug).count()>0:
        errormessage = "Target already contains a page at %s%s" \
            % (target.get_absolute_url(), page.slug)
        is_valid = False
    if target in page.get_descendants():
        errormessage = "Cannot move page to a its own subtree."
        is_valid = False

    if is_valid and request.POST \
            and request.POST.get('confirm', '') == _('Yes'):
        oldpath = page.get_absolute_url()
        page.move(target=target, pos='last-child')
        # reget the page with updated tree-props
        page = Page.objects.get(id=pageid)
        # saving the page will update the urlpath
        page.save()
        # TODO: Move to models.py
        url_changed.send(
            Page,
            id=page.id,
            oldpath=oldpath,
            oldtitle=page.title, #title doesn't change when moving
            newpath=page.get_absolute_url(),
            newtitle=page.title)
        # After moving get the permissions from the parent
        # TODO: *copy* from the parent and *then* propagate to prevent
        # overwriting different settings in the (new) siblings
        page.get_parent().propagate()
        return http.HttpResponseRedirect(page.get_absolute_url())
    if request.is_ajax():
        template = 'finch/ajax.html'
    else:
        template = 'contentmanager/contentmanager_base.html'
    tree = page.get_tree(parent=page)
    context = RequestContext(request, locals())
    return render_to_response('finch/move-confirm.html', context)


@permission_required('finch.delete_page')
def delete_page(request, pageid):
    page = get_object_or_404(Page, id=pageid)
    if request.POST and request.POST.get('confirm', '') == _('Yes'):
        parent = page.get_parent()
        page.delete()
        return http.HttpResponseRedirect(parent.get_absolute_url())
    else:
        if request.is_ajax():
            template = 'finch/ajax.html'
        else:
            template = 'contentmanager/contentmanager_base.html'
        tree = page.get_tree(parent=page)
        context = RequestContext(request, locals())
        return render_to_response('finch/delete.html', context)


@permission_required('finch.change_page')
def sitemap(request):
    tree = Page.get_tree()
    if request.is_ajax():
        template = 'finch/ajax.html'
    else:
        template = 'contentmanager/contentmanager_base.html'
    context = RequestContext(request, locals())
    return render_to_response('finch/finch_sitemap.html', context)


@permission_required('finch.change_page')
def get_link_list(request):
    """ for use with django-tinymce """
    from tinymce.views import render_to_link_list
    all_pages = Page.objects.filter(online=True).order_by('lft')
    link_list = [(page.title, page.get_absolute_url()) for page in all_pages]
    return render_to_link_list(link_list)
