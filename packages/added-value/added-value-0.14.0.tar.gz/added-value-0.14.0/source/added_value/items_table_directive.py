from __future__ import division

import csv

import natsort

from docutils.parsers.rst import Directive, directives
from docutils.parsers.rst.directives import unchanged_required, unchanged
from docutils.parsers.rst.directives.tables import align
from docutils.statemachine import StringList
from six import StringIO
from sphinx.ext.autosummary import import_by_name

from added_value.common_options import CLASS_OPTION, ALIGN_OPTION, NAME_OPTION
from added_value.grammatical_conjunctions import list_conjunction
from added_value.util import run_length_encode
from added_value.multisort import asc, dec, as_is
from added_value.non_string_iterable import NonStringIterable
from added_value.tabulator import tabulate, is_rectangular, size

CELL_FORMATS_OPTION = "cell-formats"
HEADER_OPTION = "header"
STUB_COLUMNS_OPTION = "stub-columns"
HEADER_ROWS_OPTION = "header-rows"
WIDTHS_OPTION = "widths"
TITLE_OPTION = "title"
H_LEVEL_TITLES_OPTION = "h-level-titles"
V_LEVEL_TITLES_OPTION = "v-level-titles"
V_LEVEL_SORT_ORDERS_OPTION = "v-level-sort-orders"
H_LEVEL_SORT_ORDERS_OPTION = "h-level-sort-orders"
V_LEVEL_VISIBILITY_OPTION = "v-level-visibility"
H_LEVEL_VISIBILITY_OPTION = "h-level-visibility"
V_LEVEL_INDEXES_OPTION = "v-level-indexes"
H_LEVEL_INDEXES_OPTION = "h-level-indexes"


_natural = natsort.natsort_keygen()

SORT_ORDERS = {"asc": asc(_natural), "dec": dec(_natural), "as-is": as_is()}

VISIBILITIES = {"show": True, "hide": False}


class ItemsTableDirective(Directive):
    """Format a data structure as a table.

    If the items of the sequence are themselves sequences, they will formatted as rows.
    """

    required_arguments = 1
    has_content = False
    option_spec = {
        TITLE_OPTION: unchanged_required,
        HEADER_ROWS_OPTION: directives.nonnegative_int,
        STUB_COLUMNS_OPTION: directives.nonnegative_int,
        HEADER_OPTION: unchanged,
        H_LEVEL_TITLES_OPTION: unchanged,
        V_LEVEL_TITLES_OPTION: unchanged,
        H_LEVEL_INDEXES_OPTION: unchanged_required,
        V_LEVEL_INDEXES_OPTION: unchanged_required,
        H_LEVEL_VISIBILITY_OPTION: unchanged,
        V_LEVEL_VISIBILITY_OPTION: unchanged,
        H_LEVEL_SORT_ORDERS_OPTION: unchanged,
        V_LEVEL_SORT_ORDERS_OPTION: unchanged,
        CELL_FORMATS_OPTION: unchanged_required,
        WIDTHS_OPTION: directives.value_or(("auto", "grid"), directives.positive_int_list),
        CLASS_OPTION: directives.class_option,
        ALIGN_OPTION: align,
        NAME_OPTION: unchanged,
    }

    @property
    def widths(self):
        return self.options.get(WIDTHS_OPTION, "")

    @property
    def header_rows(self):
        return self.options.get(HEADER_ROWS_OPTION, 0)

    @property
    def stub_columns(self):
        return self.options.get(STUB_COLUMNS_OPTION, 0)

    @property
    def v_level_titles(self):
        if V_LEVEL_TITLES_OPTION not in self.options:
            return None
        titles = self.options[V_LEVEL_TITLES_OPTION]
        titles_stream = StringIO(titles)
        reader = csv.reader(titles_stream, delimiter=",", quotechar='"', skipinitialspace=True, doublequote=True)
        titles_row = next(reader)
        stripped_titles = [cell.strip() for cell in titles_row]
        return stripped_titles

    @property
    def h_level_titles(self):
        if H_LEVEL_TITLES_OPTION not in self.options:
            return None
        titles = self.options[H_LEVEL_TITLES_OPTION]
        titles_stream = StringIO(titles)
        reader = csv.reader(titles_stream, delimiter=",", quotechar='"', skipinitialspace=True, doublequote=True)
        titles_row = next(reader)
        stripped_titles = [cell.strip() for cell in titles_row]
        return stripped_titles

    @property
    def v_level_indexes(self):
        text = self.options.get(V_LEVEL_INDEXES_OPTION, "")
        try:
            items = list(map(int, filter(None, text.split(","))))
        except ValueError:
            raise self.error(
                "Could not interpret option {} {!r}".format(V_LEVEL_INDEXES_OPTION, text)
            )
        return items or None

    @property
    def h_level_indexes(self):
        text = self.options.get(H_LEVEL_INDEXES_OPTION, "")
        try:
            items = list(map(int, filter(None, text.split(","))))
        except ValueError:
            raise self.error(
                "Could not interpret option {} {!r}".format(H_LEVEL_INDEXES_OPTION, text)
            )
        return items or None

    @property
    def v_level_visibility(self):
        text = self.options.get(V_LEVEL_VISIBILITY_OPTION, "")
        try:
            visibilities = list(map(lambda s: s.strip().lower(), filter(None, text.split(","))))
        except ValueError:
            raise self.error(
                "Could not interpret option {} {!r}".format(V_LEVEL_VISIBILITY_OPTION, text)
            )
        if not visibilities:
            return None
        try:
            return [VISIBILITIES[visibility] for visibility in visibilities]
        except KeyError:
            raise self.error(
                "Could not interpret option {} {!r}. Items must each be one of {}".format(
                    V_LEVEL_VISIBILITY_OPTION,
                    text,
                    list_conjunction(list(map(repr, VISIBILITIES.keys())), "or"),
                )
            )

    @property
    def h_level_visibility(self):
        text = self.options.get(H_LEVEL_VISIBILITY_OPTION, "")
        try:
            visibilities = list(map(lambda s: s.strip().lower(), filter(None, text.split(","))))
        except ValueError:
            raise self.error(
                "Could not interpret option {} {!r}".format(H_LEVEL_VISIBILITY_OPTION, text)
            )
        if not visibilities:
            return None
        try:
            return [VISIBILITIES[visibility] for visibility in visibilities]
        except KeyError:
            raise self.error(
                "Could not interpret option {} {!r}. Items must each be one of {}".format(
                    H_LEVEL_VISIBILITY_OPTION,
                    text,
                    list_conjunction(list(map(repr, VISIBILITIES.keys())), "or"),
                )
            )

    @property
    def v_level_sort_orders(self):
        text = self.options.get(V_LEVEL_SORT_ORDERS_OPTION, "")
        try:
            orders = list(map(lambda s: s.strip(), filter(None, text.split(","))))
        except ValueError:
            raise self.error(
                "Could not interpret option {} {!r}".format(V_LEVEL_SORT_ORDERS_OPTION, text)
            )
        if not orders:
            return None
        try:
            return [SORT_ORDERS[order] for order in orders]
        except KeyError:
            raise self.error(
                "Could not interpret option {} {!r}. Items must each be one of {}".format(
                    V_LEVEL_SORT_ORDERS_OPTION, text, ", ".join(SORT_ORDERS.keys())
                )
            )

    @property
    def h_level_sort_orders(self):
        text = self.options.get(H_LEVEL_SORT_ORDERS_OPTION, "")
        try:
            orders = list(map(lambda s: s.strip(), filter(None, text.split(","))))
        except ValueError:
            raise self.error(
                "Could not interpret option {} {!r}".format(H_LEVEL_SORT_ORDERS_OPTION, text)
            )
        if not orders:
            return None
        try:
            return [SORT_ORDERS[order] for order in orders]
        except KeyError:
            raise self.error(
                "Could not interpret option {} {!r}. Items must each be one of {}".format(
                    H_LEVEL_SORT_ORDERS_OPTION, text, ", ".join(SORT_ORDERS.keys())
                )
            )

    def get_column_widths(self, max_cols):
        if isinstance(self.widths, list):
            if len(self.widths) != max_cols:
                raise self.error(
                    "{!s} widths tabulate not match the number of columns {!s} in table. ({} directive).".format(
                        self.widths, max_cols, self.name
                    )
                )
            col_widths = self.widths
        elif max_cols:
            col_widths = [100.0 / max_cols] * max_cols
        else:
            raise self.error(
                "Something went wrong calculating column widths. ({} directive).".format(self.name)
            )
        return col_widths

    def process_header_option(self):
        table_head = []
        max_header_cols = 0
        if HEADER_OPTION in self.options:
            # TODO: Have the option for this to be a Python object too.
            header = self.options[HEADER_OPTION]
            header_stream = StringIO(header)
            reader = csv.reader(header_stream, delimiter=",", quotechar='"')
            header_row = next(reader)
            stripped_header_row = [cell.strip() for cell in header_row]
            table_head.append(stripped_header_row)
            max_header_cols = len(header_row)
        return table_head, max_header_cols

    def interpret_obj(
        self,
        obj,
        v_level_indexes,
        h_level_indexes,
        v_level_visibility,
        h_level_visibility,
        v_level_sort_keys,
        h_level_sort_keys,
        v_level_titles,
        h_level_titles,
    ):
        """Interpret the given Python object as a table.

        Args:
            obj: A sequence (later a mapping, too)

        Returns:
            A list of lists represents rows of cells.

        Raises:
            TypeError: If the type couldn't be interpreted as a table.
        """
        if not isinstance(obj, NonStringIterable):
            raise self.error("Cannot make a table from object {!r}".format(obj))

        rectangular_rows = tabulate(
            obj,
            v_level_indexes=v_level_indexes,
            h_level_indexes=h_level_indexes,
            v_level_visibility=v_level_visibility,
            h_level_visibility=h_level_visibility,
            v_level_sort_keys=v_level_sort_keys,
            h_level_sort_keys=h_level_sort_keys,
            v_level_titles=v_level_titles,
            h_level_titles=h_level_titles,
        )
        assert is_rectangular(rectangular_rows)
        num_rows, num_cols = size(rectangular_rows)
        return rectangular_rows, num_cols

    def augment_cells(self, rows, source, *, span):
        return self.augment_cells_span(rows, source) if span else self.augment_cells_no_span(rows, source)

    def augment_cells_span(self, rows, source):
        # TODO: Hardwired str transform.
        # 4-tuple: morerows, morecols, offset, cellblock
        # - morerows: The number of additional rows this cells spans
        # - morecols: The number of additional columns this cell spans
        # - offset: Offset from the line-number at the start of the table
        # - cellblock: The contents of the cell
        return [
            [(0, span - 1, 0, StringList(str(cell).splitlines(), source=source))
             for cell, span in run_length_encode(row)]
            for row in rows
        ]

    def augment_cells_no_span(self, rows, source):
        """Convert each cell into a tuple suitable for consumption by build_table.
        """
        # TODO: Hardwired str transform.
        # 4-tuple: morerows, morecols, offset, cellblock
        # - morerows: The number of additional rows this cells spans
        # - morecols: The number of additional columns this cell spans
        # - offset: Offset from the line-number at the start of the table
        # - cellblock: The contents of the cell
        return [
            [(0, 0, 0, StringList(str(cell).splitlines(), source=source)) for cell in row]
            for row in rows
        ]


    def run(self):

        obj_name = self.arguments[0]

        try:
            prefixed_name, obj, parent, modname = import_by_name(obj_name)
        except ImportError:
            raise self.error(
                "Could not locate Python object {} ({} directive).".format(obj_name, self.name)
            )
        table_head, max_header_cols = self.process_header_option()
        rows, max_cols = self.interpret_obj(
            obj,
            self.v_level_indexes,
            self.h_level_indexes,
            self.v_level_visibility,
            self.h_level_visibility,
            self.v_level_sort_orders,
            self.h_level_sort_orders,
            self.v_level_titles,
            self.h_level_titles,
        )
        max_cols = max(max_cols, max_header_cols)
        col_widths = self.get_column_widths(max_cols)
        table_head.extend(rows[: self.header_rows])
        table_body = rows[self.header_rows :]

        table_head = self.augment_cells(table_head, source=prefixed_name, span=True)
        table_body = self.augment_cells(table_body, source=prefixed_name, span=False)

        table = (col_widths, table_head, table_body)
        table_node = self.state.build_table(
            table, self.content_offset, self.stub_columns, widths=self.widths
        )
        table_node["classes"] += self.options.get("class", [])
        if "align" in self.options:
            table_node["align"] = self.options.get("align")
        self.add_name(table_node)

        return [table_node]
