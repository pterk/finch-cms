tinymce = {
    'TINYMCE_COMPRESSOR': True,
    'TINYMCE_DEFAULT_CONFIG': {
        "theme" : "advanced",
        "invalid_elements" : "font",
        "remove_script_host" : True,
        "relative_urls" : False,
        "remove_linebreaks" : False,
        "button_tile_map" : True,
        "auto_cleanup_word" : True,
        "auto_reset_designmode" : True,
        "entity_encoding" : "raw",
        "theme_advanced_toolbar_location" : "top",
        "theme_advanced_toolbar_align" : "left",
        "theme_advanced_statusbar_location": "bottom",
        "theme_advanced_resizing" : True,
        "theme_advanced_buttons1_add" : "separator,removeformat,visualaid",
        "theme_advanced_buttons2_add" : "separator,hr,separator,sub,sup,separator,charmap",
        "theme_advanced_buttons3" : "",
        }
    }

haystack = {
    'HAYSTACK_SITECONF': 'finch.search_sites',
    'HAYSTACK_SEARCH_ENGINE': 'whoosh',
    'HAYSTACK_WHOOSH_PATH': ''
}

installed_apps = [
    'grappelli',
    'filebrowser',
    'django.contrib.webdesign',
    'tinymce',
    'contentmanager',
    'finch',
    'whoosh',
    'haystack',
    ]
