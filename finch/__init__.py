import os

from finch.project_settings import tinymce, haystack, installed_apps


def monkeypatch_settings(settings):
    project_dir = os.path.abspath(os.path.dirname(settings['__file__'])) 
    haystack['HAYSTACK_WHOOSH_PATH'] = os.path.join(
        project_dir, 'whoosh_index')
    settings.update(haystack)
    settings.update(tinymce)
    settings['ADMIN_MEDIA_PREFIX'] = os.path.join(
        settings.get('STATIC_URL', '/static/'),
        'grappelli/')
    settings['INSTALLED_APPS'] = installed_apps + \
        list(settings.get('INSTALLED_APPS', []))
