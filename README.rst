Finch CMS
=========

Finch CMS is a simple to use but flexible CMS for django. It is also
very simple to install and integrate into your django project.

First make sure you have a django project, preferably in a virtual
environment. If you need help with that, check out the django
tutorial_.

To install the latest version from pypi::

  $ pip install finch-cms

  ...

Edit settings.py. The easiest option is to include the following lines
at the bottom::

  from finch import monkeypatch_settings
  monkeypatch_settings(locals())

If you prefer to update the settings manually look at
finch.project_settings and the monkeypatch_settings function
(finch/__init__.py).

Also add the following in your urls.py::


  urlpatterns = patterns(
      ...
      url(r'^finch/', include('finch.urls')),
  )

Finally run the following commands::

  $ ./manage.py syncdb
  $ ./manage.py make_homepage
  $ ./manage.py runserver


.. _tutorial: https://docs.djangoproject.com/en/1.3/intro/tutorial01/#creating-a-project
