import copy

from django import template
from django.db.models import Q
from django.template import Node, NodeList, Variable

from finch.models import Page

register = template.Library()


class FinchCMS(template.Node):
    """ The 'menubar' that shows what actions are available

    """
    def render(self, context):
        return template.loader.render_to_string('finch/finch-cms.html', context)


def finch_cms(parser, token):
    return FinchCMS()


def menu_pages(page):
    """ 
    Returns the childpages of <page> that have menu == True

    Usage: page|menu_pages

    For example:

    Homepage (online=True)
     \- PageA1 (menu=True, online=True)
          \- PageA2 (menu=True, online=True)
     \- PageB1 (inmenu=True, online=True)
          \- PageB2 (menu=True, online=True)

    A simple menu can be created like this:

    {% load finchtags %}
    {% with page|currentmenu:2 as selectedmenu %}    
    <ul id="nav">
      <li><a href="/"{% if page.is_root %} class="current"{% endif %}>{{ page.get_root.title }}</a></li>
        {% for p in page.get_root|menu_pages %}<li>
        <a href="{{ p.get_absolute_url }}"{% ifequal p selectedmenu %}class="current"{% endifequal %}>{{ p.title }}</a>
      </li>
      {% endfor %}
    </ul>
    {% endwith %}

    There are a lot of variations on this theme in the various
    menu-types but most can be accomplished with similar incantations.

    """
    if not page:
        page = Page.objects.get(urlpath='/')
    return page.get_children().filter(online=True, menu=True)


def currentmenu(page, depth):
    """
    Returns the (ancestral) page with inmenu=True and online=True
    at <depth>. Root is depth 1.

    You can use this to highlight 'current' items in a menu for
    example. See menu_pages for a demo.
    
    """
    if not page:
        page = Page.objects.get(urlpath='/')
    if type(page) != Page:
        return None
    if page.depth == depth:
        return page
    menu = page.get_ancestors().filter(online=True, menu=True, depth=depth)
    if menu:
        return menu[0]


# This code is a (simplefied?) version of the same functionality in
# django-mptt for which we are eternally grateful
def tree_info(values):
    """
    Given a list of tree items, produces doubles of a tree item and a
    ``dict`` containing information about the tree structure around the
    item, with the following contents:
    
       new_level
          ``True`` if the current item is the start of a new level in
          the tree, ``False`` otherwise.

       closed_levels
          A list of levels which end after the current item. This will
          be an empty list if the next item is at the same level as the
          current item.

    Using this filter with unpacking in a ``{% for %}`` tag, you should
    have enough information about the tree structure to create a
    hierarchical representation of the tree.

    Example::

       {% for genre,structure in genres|tree_info %}
       {% if structure.new_level %}<ul><li>{% else %}</li><li>{% endif %}
       {{ genre.name }}
       {% for level in structure.closed_levels %}</li></ul>{% endfor %}
       {% endfor %}

    """
    structure = {}
    n = len(values)
    previous = None
    for i in range(n):
        # Get previous, current and next
        if i>0: previous = values[i-1]
        current = values[i]
        if i+1<n: 
            next = values[i+1]
        else:
            next = None

        if previous:
            structure['new_level'] = previous.depth < current.depth
        else:
            structure['new_level'] = True
        if next:
            structure['closed_levels'] = range(current.depth, next.depth, -1)
        else:
            structure['closed_levels'] = range(current.depth, 0, -1)
        yield current, copy.deepcopy(structure)


def user_pages(user):
    """ Returns a treestructure containing only the pages the user can see. """
    if user.has_module_perms('finch'):
        tree = Page.get_tree()
    else:
        tree = Page.get_tree().filter(online=True).distinct()
    return tree_info(tree)


def get_page_title(path):
    chopat = path.find('#')
    if chopat>-1:
        path = path[:chopat]
    try:
        return Page.objects.get(urlpath=path).title
    except Page.DoesNotExist:
        return path


register.tag('finch_cms', finch_cms)
register.filter('menu_pages', menu_pages)
register.filter('currentmenu', currentmenu)
register.filter('tree_info', tree_info)
register.filter('get_page_title', get_page_title)
