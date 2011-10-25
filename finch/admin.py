from django.contrib import admin

from finch.models import Page, Paragraph


class PageAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'urlpath', 'online', 'template', 'updated', 'updated_by'
        )


admin.site.register(Page, PageAdmin)
admin.site.register(Paragraph)
