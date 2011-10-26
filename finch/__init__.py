import os

from finch.project_settings import tinymce, haystack, installed_apps

DEBUG_MIDDLEWARE = 'debug_toolbar.middleware.DebugToolbarMiddleware'
FINCH_MIDDELWARE = 'finch.middleware.FinchMiddleware'


def monkeypatch_settings(settings):
    project_dir = os.path.abspath(os.path.dirname(settings['__file__'])) 
    haystack['HAYSTACK_WHOOSH_PATH'] = os.path.join(
        project_dir, 'whoosh_index')
    settings.update(haystack)
    settings.update(tinymce)
    middleware_classes = list(settings.get('MIDDLEWARE_CLASSES', []))
    if DEBUG_MIDDLEWARE in middleware_classes:
        middleware_classes.insert(
            middleware_classes.index(DEBUG_MIDDLEWARE),
            FINCH_MIDDELWARE)
    else:
        middleware_classes.append(FINCH_MIDDELWARE)
    settings['MIDDLEWARE_CLASSES'] = middleware_classes
    settings['ADMIN_MEDIA_PREFIX'] = os.path.join(
        settings.get('STATIC_URL', '/static/'),
        'grappelli/')
    settings['INSTALLED_APPS'] = installed_apps + \
        list(settings.get('INSTALLED_APPS', []))
