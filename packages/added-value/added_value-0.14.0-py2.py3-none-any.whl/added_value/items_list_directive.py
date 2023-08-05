from __future__ import division

import csv
import re
from collections.abc import Mapping, Sequence

import natsort
from docutils import nodes
from docutils.parsers.rst.states import Body

from docutils.parsers.rst import Directive, directives
from docutils.parsers.rst.directives import unchanged_required, unchanged
from six import StringIO
from sphinx.ext.autosummary import import_by_name

from added_value import common_options
from added_value.common_options import NAME_OPTION, CLASS_OPTION
from added_value.grammatical_conjunctions import list_conjunction
from added_value.multisort import asc, dec, as_is
from added_value.non_string_iterable import NonStringIterable

ASCENDING = "asc"
DECENDING = "dec"
AS_IS = "as-is"

BULLET_LIST_TYPE = "bullet"
ENUMERATED_LIST_TYPE = "enumerated"
DEFINITION_LIST_TYPE = "definition"

LIST_TYPES_OPTION = "list-types"
KEY_FORMATS_OPTION = "key-formats"
SORT_ORDERS_OPTION = "sort-orders"
INTERNAL_FORMATS_OPTION = "internal-formats"
LEAF_FORMAT_OPTION = "leaf-format"
ORDINAL_BASES_OPTION = "ordinal-bases"

_natural = natsort.natsort_keygen()

ENUMERATOR_PATTERN = Body.patterns["enumerator"]

TEXT_SORT_ORDERS = {ASCENDING: asc(_natural), DECENDING: dec(_natural), AS_IS: as_is()}

SORT_ORDERS = {ASCENDING: asc(), DECENDING: dec(), AS_IS: as_is()}

DEFAULT_KEY_FORMATS = {
    BULLET_LIST_TYPE: "*",
    ENUMERATED_LIST_TYPE: "1.",
    DEFINITION_LIST_TYPE: "{k}",
}

DEFAULT_INTERNAL_FORMAT = object()

DEFAULT_INTERNAL_FORMATS = {
    BULLET_LIST_TYPE: DEFAULT_INTERNAL_FORMAT,
    ENUMERATED_LIST_TYPE: DEFAULT_INTERNAL_FORMAT,
    DEFINITION_LIST_TYPE: DEFAULT_INTERNAL_FORMAT,
}

DEFAULT_SORT_ORDERS = {
    BULLET_LIST_TYPE: AS_IS,
    ENUMERATED_LIST_TYPE: AS_IS,
    DEFINITION_LIST_TYPE: AS_IS,
}

DEFAULT_ORDINAL_BASE = 1


class ItemsListDirective(Directive):
    """Format a data structure as nested lists.
    """

    required_arguments = 1
    has_content = False
    option_spec = {
        LIST_TYPES_OPTION: unchanged_required,
        SORT_ORDERS_OPTION: unchanged,
        KEY_FORMATS_OPTION: unchanged,
        INTERNAL_FORMATS_OPTION: unchanged,
        LEAF_FORMAT_OPTION: unchanged,
        ORDINAL_BASES_OPTION: unchanged,
        CLASS_OPTION: directives.class_option,
        NAME_OPTION: unchanged,
    }

    @property
    def key_formats(self):
        if KEY_FORMATS_OPTION not in self.options:
            return None
        formats = self.options[KEY_FORMATS_OPTION]
        formats_stream = StringIO(formats)
        reader = csv.reader(
            formats_stream, delimiter=",", quotechar='"', skipinitialspace=True, doublequote=True
        )
        formats_row = next(reader)
        stripped_formats = [cell.strip() for cell in formats_row]
        return stripped_formats

    @property
    def internal_formats(self):
        if INTERNAL_FORMATS_OPTION not in self.options:
            return None
        formats = self.options[INTERNAL_FORMATS_OPTION]
        formats_stream = StringIO(formats)
        reader = csv.reader(
            formats_stream, delimiter=",", quotechar='"', skipinitialspace=True, doublequote=True
        )
        formats_row = next(reader)
        stripped_formats = [cell.strip() for cell in formats_row]
        return stripped_formats

    @property
    def leaf_format(self):
        return self.options.get(LEAF_FORMAT_OPTION, "{v}")

    @property
    def list_types(self):
        text = self.options.get(LIST_TYPES_OPTION, "bullet")
        try:
            types = list(map(lambda s: s.strip().lower(), filter(None, text.split(","))))
        except ValueError:
            raise self.error("Could not interpret option {} {!r}".format(LIST_TYPES_OPTION, text))
        if not types:
            return None

        for type in types:
            if type not in self.LIST_TYPES:
                raise self.error(
                    "Could not interpret option {} {!r}. Items must each be one of {}".format(
                        LIST_TYPES_OPTION,
                        text,
                        list_conjunction([repr(k) for k in self.LIST_TYPES.keys()], "or"),
                    )
                )
        return types

    @property
    def sort_orders(self):
        if SORT_ORDERS_OPTION not in self.options:
            return None
        text = self.options[SORT_ORDERS_OPTION]
        try:
            orders = list(map(lambda s: s.strip(), filter(None, text.split(","))))
        except ValueError:
            raise self.error("Could not interpret option {} {!r}".format(SORT_ORDERS_OPTION, text))

        for order in orders:
            if order not in TEXT_SORT_ORDERS:
                raise self.error(
                    "Could not interpret option {} {!r}. Items must each be one of {}".format(
                        SORT_ORDERS_OPTION,
                        text,
                        list_conjunction([repr(k) for k in TEXT_SORT_ORDERS.keys()], "or"),
                    )
                )
        return orders

    @property
    def ordinal_bases(self):
        if ORDINAL_BASES_OPTION not in self.options:
            return None
        text = self.options[ORDINAL_BASES_OPTION]
        try:
            ordinals = list(map(lambda s: int(s.strip()), filter(None, text.split(","))))
        except ValueError:
            raise self.error(
                "Could not interpret option {} {!r}".format(ORDINAL_BASES_OPTION, text)
            )
        return ordinals

    @staticmethod
    def is_leaf_list(inner_list_types):
        return len(inner_list_types) == 0

    def render_child_nodes(
        self,
        obj,
        sort_order,
        ordinal_base,
        inner_list_types,
        inner_key_formats,
        inner_internal_formats,
        inner_sort_orders,
        inner_ordinal_bases,
    ):
        if self.is_leaf_list(inner_list_types):
            child_ordinals, child_keys, child_values, child_nodes = self.render_leaves(
                obj, sort_order, ordinal_base
            )
        else:
            child_ordinals, child_keys, child_values, child_nodes = self.render_nested_list(
                obj,
                sort_order,
                ordinal_base,
                inner_list_types,
                inner_key_formats,
                inner_internal_formats,
                inner_sort_orders,
                inner_ordinal_bases,
            )
        return list(child_ordinals), list(child_keys), list(child_values), list(child_nodes)

    def render_nested_list(
        self,
        obj,
        sort_order,
        ordinal_base,
        inner_list_types,
        inner_key_formats,
        inner_internal_formats,
        inner_sort_orders,
        inner_ordinal_bases,
    ):
        sort_key = SORT_ORDERS[sort_order]

        if isinstance(obj, Mapping):
            # TODO: Consider doing something different here!
            sorted_keys = sorted(obj.keys(), key=sort_key.func, reverse=sort_key.reverse)
            sorted_values = [obj[key] for key in sorted_keys]
        else:

            sorted_items = sorted(
                enumerate(obj, start=0),  # Original position
                key=lambda item: sort_key.func(item[1]),
                reverse=sort_key.reverse,
            )
            sorted_keys, sorted_values = zip(*sorted_items)

        item_nodes = [
            (
                ordinal,
                key,
                value,
                self.render_list(
                    value,
                    inner_list_types,
                    inner_key_formats,
                    inner_internal_formats,
                    inner_sort_orders,
                    inner_ordinal_bases,
                ),
            )
            for ordinal, (key, value) in enumerate(
                zip(sorted_keys, sorted_values), start=ordinal_base
            )
        ]
        return zip(*item_nodes)

    def render_leaves(self, obj, sort_order, ordinal_base):
        if isinstance(obj, Mapping):
            key_value_pairs = obj.items()
        elif isinstance(obj, Sequence):
            key_value_pairs = enumerate(obj, start=0)
        else:
            key_value_pairs = enumerate(list(obj), start=0)

        sort_key = TEXT_SORT_ORDERS[sort_order]

        # TODO: Allow specification of the sort key
        sorted_items = sorted(
            key_value_pairs, key=lambda item: sort_key.func(item[1]), reverse=sort_key.reverse
        )

        item_nodes = [
            (
                ordinal,
                key,
                value,
                nodes.paragraph(text=self.leaf_format.format(o=ordinal, k=key, v=value)),
            )
            for ordinal, (key, value) in enumerate(sorted_items, start=ordinal_base)
        ]
        return zip(*item_nodes)

    def add_global_attributes(self, list_node):
        list_node["classes"] += self.options.get("class", [])
        if "align" in self.options:
            list_node["align"] = self.options.get("align")
        self.add_name(list_node)

    def render_list(
        self, obj, list_types, key_formats, internal_formats, sort_orders, ordinal_bases
    ):
        if not isinstance(obj, NonStringIterable):
            raise self.error("Cannot make a list from object {!r}".format(obj))

        list_type, *inner_list_types = list_types
        key_format, *inner_key_formats = key_formats
        internal_format, *inner_internal_formats = internal_formats
        sort_order, *inner_sort_orders = sort_orders
        ordinal_base, *inner_ordinal_bases = ordinal_bases

        if internal_format is DEFAULT_INTERNAL_FORMAT:
            internal_format = "{k}" if isinstance(obj, Mapping) else ""

        list_renderer = self.LIST_TYPES[list_type]

        list_node = list_renderer(
            self,
            obj,
            key_format,
            internal_format,
            sort_order,
            ordinal_base,
            inner_list_types,
            inner_key_formats,
            inner_internal_formats,
            inner_sort_orders,
            inner_ordinal_bases,
        )

        self.add_global_attributes(list_node)
        return list_node

    def render_bullet_list(
        self,
        obj,
        key_format,
        internal_format,
        sort_order,
        ordinal_base,
        inner_list_types,
        inner_key_formats,
        inner_internal_formats,
        inner_sort_orders,
        inner_ordinal_bases,
    ):
        if key_format not in {"*", "+", "-", "•", "‣", "⁃"}:
            raise self.error(
                "Invalid {} {} for {}".format(KEY_FORMATS_OPTION, key_format, BULLET_LIST_TYPE)
            )

        list_node = nodes.bullet_list()
        list_node["bullet"] = key_format

        child_ordinals, child_keys, child_values, child_nodes = self.render_child_nodes(
            obj,
            sort_order,
            ordinal_base,
            inner_list_types,
            inner_key_formats,
            inner_internal_formats,
            inner_sort_orders,
            inner_ordinal_bases,
        )

        for ordinal, key, value, child_node in zip(
            child_ordinals, child_keys, child_values, child_nodes
        ):
            list_item_node = nodes.list_item()

            header_text = internal_format.format(o=ordinal, k=key, v=value)
            if header_text and not header_text.isspace():
                list_item_node += nodes.paragraph(text=header_text)

            list_node += list_item_node
            list_item_node += child_node
        return list_node

    def render_enumerated_list(
        self,
        obj,
        key_format,
        internal_format,
        sort_order,
        ordinal_base,
        inner_list_types,
        inner_key_formats,
        inner_internal_formats,
        inner_sort_orders,
        inner_ordinal_bases,
    ):
        m = re.match(ENUMERATOR_PATTERN, key_format)
        if m is None:
            raise self.error(
                "Invalid {} {} for {}".format(KEY_FORMATS_OPTION, key_format, "bullet")
            )

        # We instantiate this docutils state-machine state just so we leverage methods defined on it
        # which allows us to maintain consistency with the core docutils behaviour
        body = Body(None)

        fmt, sequence, text, start = body.parse_enumerator(m)

        list_node = nodes.enumerated_list()

        if sequence == "#":
            list_node["enumtype"] = "arabic"
        else:
            list_node["enumtype"] = sequence

        list_node["prefix"] = body.enum.formatinfo[fmt].prefix
        list_node["suffix"] = body.enum.formatinfo[fmt].suffix

        if start != 1:
            list_node["start"] = start

        child_ordinals, child_keys, child_values, child_nodes = self.render_child_nodes(
            obj,
            sort_order,
            ordinal_base,
            inner_list_types,
            inner_key_formats,
            inner_internal_formats,
            inner_sort_orders,
            inner_ordinal_bases,
        )

        list_node["bullet"] = key_format
        for ordinal, key, value, child_node in zip(
            child_ordinals, child_keys, child_values, child_nodes
        ):
            list_item_node = nodes.list_item()

            header_text = internal_format.format(o=ordinal, k=key, v=value)
            if header_text and not header_text.isspace():
                list_item_node += nodes.paragraph(text=header_text)

            list_node += list_item_node
            list_item_node += child_node
        return list_node

    def render_definition_list(
        self,
        obj,
        key_format,
        internal_format,
        sort_order,
        ordinal_base,
        inner_list_types,
        inner_key_formats,
        inner_internal_format,
        inner_sort_orders,
        inner_ordinal_bases,
    ):
        if not isinstance(obj, Mapping):
            raise self.error(
                "List with {} {!r} cannot represent object of type {!r} because it is not a {!r}.".format(
                    LIST_TYPES_OPTION, DEFINITION_LIST_TYPE, type(obj).__name__, Mapping.__name__
                )
            )

        child_ordinals, child_keys, child_values, child_nodes = self.render_child_nodes(
            obj,
            sort_order,
            ordinal_base,
            inner_list_types,
            inner_key_formats,
            inner_internal_format,
            inner_sort_orders,
            inner_ordinal_bases,
        )

        term_nodes = [
            nodes.term("", "", nodes.Text(key_format.format(o=ordinal, k=key, v=value)))
            for ordinal, key, value in zip(child_ordinals, child_keys, child_values)
        ]

        list_node = nodes.definition_list()
        for term_node, child_node in zip(term_nodes, child_nodes):
            definition_node = nodes.definition()
            definition_node += child_node

            item_node = nodes.definition_list_item("", term_node, definition_node)
            list_node += item_node
        return list_node

    LIST_TYPES = {
        BULLET_LIST_TYPE: render_bullet_list,
        ENUMERATED_LIST_TYPE: render_enumerated_list,
        DEFINITION_LIST_TYPE: render_definition_list,
    }

    def run(self):

        obj_name = self.arguments[0]

        try:
            prefixed_name, obj, parent, modname = import_by_name(obj_name)
        except ImportError:
            raise self.error(
                "Could not locate Python object {} ({} directive).".format(obj_name, self.name)
            )

        list_types = self.list_types

        key_formats = self.key_formats or [
            DEFAULT_KEY_FORMATS[list_type] for list_type in self.list_types
        ]
        internal_formats = self.internal_formats or [
            DEFAULT_INTERNAL_FORMATS[list_type] for list_type in self.list_types
        ]
        sort_orders = self.sort_orders or [
            DEFAULT_SORT_ORDERS[list_type] for list_type in self.list_types
        ]
        ordinal_bases = self.ordinal_bases or [
            DEFAULT_ORDINAL_BASE for list_type in self.list_types
        ]
        if not (len(self.list_types) == len(key_formats) == len(sort_orders) == len(ordinal_bases)):
            raise self.error(
                "{}, {}, {}, and {} do not all have the same number of items ({} directive)".format(
                    LIST_TYPES_OPTION,
                    KEY_FORMATS_OPTION,
                    SORT_ORDERS_OPTION,
                    ORDINAL_BASES_OPTION,
                    self.name,
                )
            )

        list_node = self.render_list(
            obj, list_types, key_formats, internal_formats, sort_orders, ordinal_bases
        )

        return [list_node]
