import os

from finch.project_settings import tinymce, haystack, installed_apps

VERSION = (0, 8, 3)
__version__ = '.'.join(map(str, VERSION))

DEBUG_MIDDLEWARE = 'debug_toolbar.middleware.DebugToolbarMiddleware'
FINCH_MIDDELWARE = 'finch.middleware.FinchMiddleware'

REQUESTCONTEXTPROCESSOR = "django.core.context_processors.request"


def monkeypatch_settings(settings):
    # haystack
    project_dir = os.path.abspath(os.path.dirname(settings['__file__'])) 
    haystack['HAYSTACK_WHOOSH_PATH'] = os.path.join(
        project_dir, 'whoosh_index')
    settings.update(haystack)
    # tinymce
    settings.update(tinymce)
    # make sure there is always a requestcontext
    context_processors = list(settings.get('TEMPLATE_CONTEXT_PROCESSORS', []))
    if context_processors == []:
        from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
        context_processors = list(TEMPLATE_CONTEXT_PROCESSORS)
    if REQUESTCONTEXTPROCESSOR not in context_processors:
        context_processors.append(REQUESTCONTEXTPROCESSOR)
    settings['TEMPLATE_CONTEXT_PROCESSORS'] = context_processors
    # Add finch middleware, taking debug toolbar into account
    middleware_classes = list(settings.get('MIDDLEWARE_CLASSES', []))
    if middleware_classes == []:
        from django.conf.global_settings import MIDDLEWARE_CLASSES
        middleware_classes = MIDDLEWARE_CLASSES
    if DEBUG_MIDDLEWARE in middleware_classes:
        middleware_classes.insert(
            middleware_classes.index(DEBUG_MIDDLEWARE),
            FINCH_MIDDELWARE)
    else:
        middleware_classes.append(FINCH_MIDDELWARE)
    settings['MIDDLEWARE_CLASSES'] = middleware_classes
    # grappelli ... because of the filebrowser |-(
    settings['ADMIN_MEDIA_PREFIX'] = os.path.join(
        settings.get('STATIC_URL', '/static/'),
        'grappelli/')
    # Inject apps. Note that the urls for (some of) these apps are
    # included in finch.urls
    settings['INSTALLED_APPS'] = installed_apps + \
        list(settings.get('INSTALLED_APPS', []))
