from datetime import datetime

from django.core.management.base import NoArgsCommand


class Command(NoArgsCommand):
    help = "Will create a homepage for this projects default Site."

    def handle_noargs(self, **options):
        from django.conf import settings
        from django.contrib.sites.models import Site
        from django.utils.translation import ugettext as _

        from finch.models import Page
        from finch.settings import TEMPLATE_CHOICES

        home = Page.add_root(site_id=settings.SITE_ID,
                             # default to the same as site_id, *could*
                             # be different though...
                             tree_id=settings.SITE_ID,
                             title=_("Home"),
                             slug="", 
                             created=datetime.now(), 
                             updated=datetime.now(),
                             template=TEMPLATE_CHOICES[0][0],
                             online=True)

        print _("Created a homepage")
