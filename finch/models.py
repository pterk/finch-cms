from datetime import datetime
from django.db import models
from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.auth.models import AnonymousUser, User
from django.utils.translation import ugettext as _

from treebeard.ns_tree import NS_Node

from contentmanager import blockpath_rename

from finch.managers import NS_NodeManager
from finch.signals import url_changed
from finch import settings as finch_settings


class Page(NS_Node):
    """
    The Page-mode  only provides site-structure. Managing
    the content is handed of to another application (the
    contentmanager) via the template.

    It uses the NestedSet implementation from django-treebeard to
    model a tree.

    The site-structure is build up by adding childpages to the
    'current' page. A 'root' is created by using them management
    command `make_homepage`:

    ./manage.py make_homepage

    The title is provided by the editors and is used to make a
    slugfield. The slugfield can be edited by editors as well but the
    result is checked to comply with django's builtin slugfield. The
    exception is the homepage of a site (the root) which is the only
    page with an empty slugfield.

    The urlpath is automatically created by combining the parent's
    urlpath + this page's slugfield (and adding a slash).

    When the `menu` checkbox is checked the page is available in the
    menu_pages template_tag (if the page is online and the current
    user has access).

    Pages can either be online or not. When a request (by non-editors)
    is made to an offline pages the sitemanager returns an Http404
    Exception to prevent information 'leaking'.

    An online page is accesible to anyone unless access is restricted.
    """
    title      = models.CharField(max_length=255)
    slug       = models.CharField(max_length=255, blank=True, db_index=True)
    urlpath    = models.CharField(max_length=255, blank=True, db_index=True)
    template   = models.CharField(max_length=255,
                                  choices=finch_settings.TEMPLATE_CHOICES,
                                  default=finch_settings.TEMPLATE_CHOICES[0][0])
    site       = models.ForeignKey(Site, related_name="sitepages", default=settings.SITE_ID)
    menu       = models.BooleanField(_("In Menu"), default=False)
    online     = models.BooleanField(default=False)
    created    = models.DateTimeField()
    created_by = models.ForeignKey(User, related_name="pagecreators", null=True, blank=True)
    updated    = models.DateTimeField()
    updated_by = models.ForeignKey(User, related_name="pageupdaters", null=True, blank=True)

    objects = NS_NodeManager()

    class Meta:
        # From treebeard docs
        #
        # Warning::
        #
        #  Be very careful if you add a Meta class in your
        #  ns_tree.NS_Node subclass. You must add an ordering
        #  attribute with two elements on it:
        #
        # class Meta:
        #     ordering = ['tree_id', 'lft']
        #
        # If you don't, the tree won't work, since ns_tree.NS_Node
        # completely depends on this attribute.
        ordering = ['tree_id', 'lft']
        unique_together = (("urlpath", "site"),)

    def delete(self, *args, **kwargs):
        if self.is_root():
            raise Exception('You cannot delete a root node using the sitemanager')
        super(Page, self).delete(*args, **kwargs) # Call the "real" delete() method

    def save(self, *args, **kwargs):
        self.updated = datetime.now()
        self.urlpath = self._get_urlpath()
        if not self.id:
            self.created = datetime.now()
        super(Page, self).save(*args, **kwargs)
        if self.get_descendant_count()>0:
            self.propagate()
            for child in self.get_children():
                child.save(*args, **kwargs)

    def _get_urlpath(self):
        if self.is_root():
            return "/"
        else:
            parent = self.get_parent(update=True)
            newpath = "%s%s/" % (parent.urlpath, self.slug)
            return newpath

    def get_absolute_url(self):
        return self.urlpath

    def __unicode__(self):
        return self.title

    def propagate(self):
        """ Will set restricted and groups on all descendant pages like <page>
        """
        # Using the ORM here since there's little to be gained if the
        # groups have to be updated
        for p in self.get_descendants():
            p.online = self.online
            p.save()


class Paragraph(models.Model):
    """A simple block of text.
    """
    title = models.CharField(max_length = 255, blank=True)
    text = models.TextField()

    def __unicode__(self):
        return self.title and self.title or 'Paragraph'


def url_change_listener(sender, **kwargs):
    if not sender==Page:
        return
    oldpath = kwargs['oldpath']
    newpath = kwargs['newpath']
    # update related contentmanager blocks
    blockpath_rename(oldpath, newpath)
    # update *content* in paragraphs
    for par in Paragraph.objects.filter(text__contains=oldpath):
        par.text = par.text.replace(oldpath, newpath)
        par.save()


url_changed.connect(url_change_listener, sender=Page)
