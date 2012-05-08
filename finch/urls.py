from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns(
    'finch.views',
    url(r'^(\d*)/create/$', 'create_page', name='create_page'),
    url(r'^(\d*)/delete/$', 'delete_page', name='delete_page'),
    url(r'^(\d*)/edit/$', 'edit_page', name='edit_page'),
    url(r'^(\d*)/order/$', 'order_pages', name='order_pages'),
    url(r'^(\d*)/move/$', 'move_page', name='move_page'),
    url(r'^(\d*)/move/(\d*)/$', 'move_confirm', name='move_confirm'),
    url(r'^sitemap/$', 'sitemap', name='sitemap'),
    url(r'^link_list/$', 'get_link_list', name='finch_link_list'),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^filebrowser/', include('filebrowser.urls')),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^contentmanager/', include('contentmanager.urls')),
    url(r'^search/', include('haystack.urls')),
    )

urlpatterns += patterns(
    '',
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='auth_login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name='auth_logout'),
    )

from contentmanager import autodiscover
autodiscover()
