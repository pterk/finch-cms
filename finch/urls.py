from django.conf.urls.defaults import *

urlpatterns = patterns(
    'finch.views',
    url(r'^(\d*)/create/$', 'create_page', name='create_page'),
    url(r'^(\d*)/delete/$', 'delete_page', name='delete_page'),
    url(r'^(\d*)/edit/$', 'edit_page', name='edit_page'),
    url(r'^(\d*)/order/$', 'order_pages', name='order_pages'),
    url(r'^(\d*)/move/$', 'move_page', name='move_page'),
    url(r'^(\d*)/move/(\d*)/$', 'move_confirm', name='move_confirm'),
    url(r'^sitemap/$', 'sitemap', name='sitemap'),
    url(r'^link_list/$', 'get_link_list', name='sitemanager_link_list'),
    )
