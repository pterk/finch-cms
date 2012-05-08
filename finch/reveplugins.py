from django import forms
from django.core.urlresolvers import reverse
from django.template import Template, Context, RequestContext
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _

from contentmanager import registry
from contentmanager.plugins import BasePlugin, BaseModelPlugin

from tinymce.widgets import TinyMCE

from finch.models import Page, Paragraph


class BackToTop(BasePlugin):
    def render(self, request):
        return render_to_string("finch/backtotop.html")


class ParagraphForm(forms.ModelForm):
    text = forms.CharField(widget=TinyMCE(
            mce_attrs={'external_link_list_url': reverse('finch_link_list')}))

    class Meta:
        model = Paragraph


class ParagraphPlugin(BaseModelPlugin):
    form = ParagraphForm
    model = Paragraph
    verbose_name = 'Paragraph'

    def get_obj(self):
        pk = self.params.get("pk", None)
        # this bit below is (tempararily) needed for backwards
        # compatibility. It will save as 'pk'
        if not pk:
            pk = self.params.get("id", None)
        if pk:
            return self.model.objects.get(pk=pk)
        return None

    def render(self, request):
        obj = self.get_obj()
        if not obj:
            return "%s no longer exists." % (self.verbose_name)
        return render_to_string('finch/paragraph.html',
                                {'title': obj.title,
                                 'text': obj.text})


class LoremForm(forms.Form):
    show = forms.IntegerField(
        help_text=_("How many paragraphs do you want to show?"),
        initial=3,
        min_value=1,
        max_value=5,
        required=True)


class LoremGenerator(BasePlugin):
    form = LoremForm
    verbose_name = "Lorem ipsum"

    def render(self, request):
        show = self.params['show']
        template = "{% load webdesign %}{% lorem "+str(show)+" p %}"
        return Template(template).render(Context({}))


class HTMLForm(forms.Form):
    html = forms.CharField(widget=forms.Textarea())


class HTML(BasePlugin):
    form = HTMLForm
    verbose_name = "Html"
    help = _("You can enter raw html here. Be aware that incorrect HTML can make you site misbehave!")

    def render(self, request):
        return self.params['html']


class Sitemap(BasePlugin):
    cacheable = False

    def render(self, request):
        user = request.user
        if user.has_module_perms('finch'):
            tree = Page.get_tree()
        else:
            tree = Page.get_tree().filter(online=True)
        template = 'finch/dummy.html'
        return render_to_string('finch/sitemap.html', 
                                RequestContext(request, {'tree': tree, 
                                                         'template': template}))



## registry ##
registry.register(ParagraphPlugin)
registry.register(BackToTop)
registry.register(LoremGenerator)
registry.register(HTML)
registry.register(Sitemap)
