from docutils import nodes

from added_value.grammatical_conjunctions import list_conjunction
from added_value.pyobj_role import make_pyobj_role


def make_all_items_node(rawtext, app, prefixed_name, obj, parent, modname, options):
    """Render a Python sequence as a comma-separated list, with an "and" for the final item.

    :param rawtext: Text being replaced with link node.
    :param app: Sphinx application context
    :param prefixed_name: The dotted Python name for obj.
    :param obj: The Python object to be rendered to text.
    :param parent: The parent Python object of obj.
    :param module: The name of the module containing obj.
    :param options: Options dictionary passed to role func.
    """
    text = list_conjunction(obj, "and")
    node = nodes.Text(text, rawsource=rawtext)
    return node


all_items_role = make_pyobj_role(make_all_items_node)
