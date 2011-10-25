import sys

import haystack

import contentmanager

# A bit of a hack but it seems to work for my use-cases
if len(sys.argv)>1 \
        and sys.argv[1] in ('clear_index', 'rebuild_index', 'update_index'):
    contentmanager.autodiscover()

haystack.autodiscover()
