"""finch signal(s)

Usage example:

from finch.signals import url_changed
from finch.models import Page

def urlchange_listener(sender, **kwargs):
    print sender, kwargs

url_changed.connect(urlchange_listener, sender=Page)


"""
from django import dispatch


# A signal to send when a page's path/url is changed so anything that
# care's to listen can act accordingly
url_changed = dispatch.Signal(
    providing_args=["oldpath,", "newpath", "oldtitle", "newtitle", "id"])
