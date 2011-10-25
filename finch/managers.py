from django.conf import settings
from django.contrib.sites.managers import CurrentSiteManager

from treebeard.ns_tree import NS_NodeQuerySet


class NS_NodeManager(CurrentSiteManager):
    """ Custom manager for nodes.
    """

    def get_query_set(self):
        """
        Sets the custom queryset as the default.
        """
        return NS_NodeQuerySet(self.model).filter(site=settings.SITE_ID)
