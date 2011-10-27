from django import forms
from django.template.defaultfilters import slugify

from finch.models import Page


class PageForm(forms.ModelForm):
    # Only need the hidden field when inserting a new page to figure
    # out the parentpage's urlpath. Unique urlpaths are enforced at
    # db-level but this allows us to present a friendly warning iso a
    # http 500
    parent_page_id = forms.IntegerField(required=False,
                                        widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super(PageForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

        if instance and instance.pk:
            parent = instance.get_parent()
        else:
            # You'd think I'm doing it wrong here...
            # This is before data is POSTED
            if self.initial:
                parentid = self.initial['parent_page_id']
            else:
                # Now it should be POSTED and therefor in self.data
                parentid = self.data['parent_page_id']
            parent = Page.objects.get(pk=parentid)
        if parent and not parent.online:
            self.fields['online'].widget.attrs['readonly'] = True
            self.fields['online'].help_text = "Disabled because 'parentpage' is offline"
            self.fields['online'].value = False

    class Meta:
        model = Page
        fields = ["title", "slug", "template", "menu", "online"]

    def clean_slug(self):
        slug = self.cleaned_data["slug"]
        # A page (instance) that is already saved in the tree has a
        # lft value...only then does it have an is_root method...
        # Normal rules do not apply for a rootnode
        if self.instance.lft and self.instance.is_root():
            return ""
        if slug!=slugify(slug):
            raise forms.ValidationError("Slug is invalid")
        if slug == "":
            raise forms.ValidationError("A slug is required")
        if self.instance.lft:
            # already know the parent
            parent = self.instance.get_parent()
        else:
            parent_page_id = int(self.data['parent_page_id'])
            parent = Page.objects.get(id=parent_page_id)
        newpath = "%s%s/" % (parent.urlpath, slug)
        exists = Page.objects.filter(urlpath=newpath).exclude(id=self.instance.id)
        if exists:
            raise forms.ValidationError(
                "A page with that address (%s) already exists" % (newpath)
                )
        return slug
