from collections import Mapping, deque
from itertools import product, chain, repeat

from added_value.items_table_directive import NonStringIterable
from added_value.multisort import tuplesorted
from added_value.sorted_frozen_set import SortedFrozenSet
from added_value.toposet import TopoSet
from added_value.util import unchain, empty_iterable

depth_marker = object()
ROOT = object()
LEAF = object()

_UNSET = object()


def breadth_first(obj, leaves=False):
    queue = deque()
    queue.append(obj)
    queue.append(None)
    level_keys = []
    current_level_keys = TopoSet()
    while len(queue) > 0:
        node = queue.popleft()
        if node is None:
            level_keys.append(current_level_keys)
            current_level_keys = TopoSet()
            queue.append(None)
            if queue[0] is None:
                break
            else:
                continue
        if isinstance(node, Mapping):
            current_level_keys.update(node.keys())
            for value in node.values():
                queue.append(value)
        elif isinstance(node, NonStringIterable):
            current_level_keys.update(range(len(node)))
            for value in node:
                queue.append(value)
        else:
            if leaves:
                current_level_keys.add(node)

    return [
        list(s) for s in level_keys[:-1]
    ]  # Why the slice? Remove leaves? Is the last always empty?


class Missing(object):
    def __str__(self):
        return ""

    def __repr__(self):
        return self.__class__.__name__


MISSING = Missing()


def tabulate_body(
    obj,
    level_keys,
    v_level_indexes,
    h_level_indexes,
    v_level_sort_keys=None,
    h_level_sort_keys=None,
):
    """
    Args:
        v_level_indexes: A sequence of level indexes.
        h_level_indexes: A sequence of level indexes.
    """
    v_key_sorted = make_sorter(v_level_sort_keys, v_level_indexes)
    h_key_sorted = make_sorter(h_level_sort_keys, h_level_indexes)

    h_level_keys = [level_keys[level] for level in h_level_indexes]
    v_level_keys = [level_keys[level] for level in v_level_indexes]

    h_key_tuples = h_key_sorted(product(*h_level_keys))
    v_key_tuples = v_key_sorted(product(*v_level_keys))

    h_size = len(h_key_tuples)
    v_size = len(v_key_tuples)

    table = [[MISSING for _ in range(h_size)] for _ in range(v_size)]

    for h_index, h_keys in enumerate(h_key_tuples):
        for v_index, v_keys in enumerate(v_key_tuples):
            key_path = [None] * len(level_keys)
            merge_into_by_index(key_path, h_level_indexes, h_keys)
            merge_into_by_index(key_path, v_level_indexes, v_keys)
            for v_level, v_key in zip(v_level_indexes, v_keys):
                key_path[v_level] = v_key

            item = obj
            for key in key_path:
                try:
                    item = item[key]
                except (IndexError, KeyError):
                    break
            else:  # no-break
                table[v_index][h_index] = item

    return table, v_key_tuples, h_key_tuples


def make_sorter(level_sort_keys, level_indexes):
    if level_sort_keys is not None:
        if len(level_sort_keys) != len(level_indexes):
            raise ValueError(
                "level_sort_keys with length {} does not correspond to level_indexes with length {}".format(
                    len(level_sort_keys), len(level_indexes)
                )
            )

        def key_sorted(level_keys):
            return tuplesorted(level_keys, *level_sort_keys)

    else:
        key_sorted = list
    return key_sorted


def strip_missing_rows(table, row_keys):
    stripped_table = []
    stripped_v_key_tuples = []
    for row, v_key_tuple in zip(table, row_keys):
        if any(cell is not MISSING for cell in row):
            stripped_table.append(list(row))
            stripped_v_key_tuples.append(v_key_tuple)
    return stripped_table, stripped_v_key_tuples


def strip_missing_columns(table, h_key_tuples):
    transposed_table = transpose(table)
    stripped_transposed_table, stripped_h_key_tuples = strip_missing_rows(
        transposed_table, h_key_tuples
    )
    stripped_table = transpose(stripped_transposed_table)
    return stripped_table, stripped_h_key_tuples


def merge_into_by_index(sequence, indexes, values):
    for index, value in zip(indexes, values):
        sequence[index] = value


def is_rectangular(seq_of_seqs):
    return len(set(map(len, seq_of_seqs))) <= 1


def size_h(rows_of_columns):
    try:
        first_row = rows_of_columns[0]
    except IndexError:
        return 0
    else:
        return len(first_row)


def size_v(rows_of_columns):
    return sum(1 for row in rows_of_columns if len(row) != 0)


def size(rows_of_columns):
    return size_v(rows_of_columns), size_h(rows_of_columns)


def transpose(rows_of_columns):
    return list(map(list, zip(*rows_of_columns)))


def assemble_table(
    table_body, v_key_tuples, h_key_tuples, v_level_titles=None, h_level_titles=None, empty=""
):
    if not is_rectangular(table_body):
        raise ValueError("table_body {} is not rectangular".format(table_body))
    if not is_rectangular(v_key_tuples):
        raise ValueError("v_key_tuples {} is not rectangular".format(v_key_tuples))
    if not is_rectangular(h_key_tuples):
        raise ValueError("h_key_tuples {} is not rectangular".format(h_key_tuples))
    if size_v(v_key_tuples) > 0 and (size_v(table_body) != size_v(v_key_tuples)):
        raise ValueError("table body and v_key_tuples have incompatible dimensions")
    h_key_tuples_transposed = transpose(h_key_tuples)
    if size_h(h_key_tuples_transposed) > 0 and (
        size_h(table_body) != size_h(h_key_tuples_transposed)
    ):
        raise ValueError("table body and h_key_tuples have incompatible dimensions")

    if (v_level_titles is not None) and (len(v_level_titles) != size_h(v_key_tuples)):
        raise ValueError("v_level_titles and v_key_tuples have incompatible dimensions")

    if (h_level_titles is not None) and (len(h_level_titles) != size_v(h_key_tuples_transposed)):
        raise ValueError("h_level_titles and h_key_tuples have incompatible dimensions")

    boxed_h_level_titles = (
        unchain(h_level_titles)
        if (h_level_titles is not None)
        else repeat(empty_iterable(), size_v(h_key_tuples_transposed))
    )

    num_h_level_title_columns = int(bool(h_level_titles))
    num_stub_columns = max(size_h(v_key_tuples), num_h_level_title_columns)
    table = []

    num_empty_columns = num_stub_columns - num_h_level_title_columns
    for boxed_h_level_title, h_key_row in zip(boxed_h_level_titles, h_key_tuples_transposed):
        row = list(chain(repeat(" ", num_empty_columns), boxed_h_level_title, h_key_row))
        table.append(row)

    if v_level_titles is not None:
        v_level_titles_row = v_level_titles + [empty] * size_h(table_body)
        table.append(v_level_titles_row)

    for v_key_row, table_row in zip(v_key_tuples, table_body):
        row = list(v_key_row)
        row.extend(table_row)
        table.append(row)

    assert is_rectangular(table)
    return table


def tabulate(
    obj,
    v_level_indexes=None,
    h_level_indexes=None,
    v_level_visibility=None,
    h_level_visibility=None,
    v_level_sort_keys=None,
    h_level_sort_keys=None,
    v_level_titles=None,
    h_level_titles=None,
    empty="",
):
    """Render a nested data structure into a two-dimensional table.

    Args:
        obj: The indexable data structure to be rendered, which can
            either be a non-string sequence or a mapping containing other
            sequences and mappings nested to arbitrarily many levels,
            with all the leaf items (which are neither sequences nor
            mappings, excluding strings).

        v_level_indexes: An iterable of the zero-based indexes of
            the levels for which the keys/indexes will be displayed
            along the vertical axis of the table. Taken together
            with the levels in h_levels these must represent the
            complete set of levels in the obj data structure. No
            level index should appear in both v_level_indexes and
            h_level_indexes, but all level indexes must appear in
            either v_level_indexes or h_level_indexes. If None,
            the levels not used in h_level_indexes will be used.
            If both v_level_indexes and h_level_indexes are not
            alternate indexes will be used as v_level and h_level
            indexes.

        h_level_indexes: An iterable of the zero-based indexes of
            the levels for which the keys/indexes will be displayed
            along the horizontal axis of the table. Taken together
            with the levels in v_levels these must represent the
            complete set of levels in the obj data structure. No
            level index should appear in both h_level_indexes and
            v_level_indexes, but all level indexes must appear in
            either h_level_indexes or v_level_indexes. If None,
            the levels not used in v_level_indexes will be used.
            If both v_level_indexes and h_level_indexes are not
            alternate indexes will be used as v_level and h_level
            indexes.

        v_level_visibility: An optional iterable of booleans, where each
            item corresponds to a level in v_level_indexes, and
            controls whether than level of index is included in
            the table stub columns. This iterable must contain
            the same number of items as v_level_indexes.

        h_level_visibility: An optional iterable of booleans, where each
            item corresponds to a level in h_level_indexes, and
            controls whether than level of index is included in
            the table header rows. This iterable must contain
            the same number of items as h_level_indexes.

        v_level_sort_keys: An optional iterable of Keys, where each
            key corresponds to a level in v_level_indexes, and
            controls how that key is sorted. If None, keys are sorted
            as-is.

        h_level_sort_keys: An optional iterable of Keys, where each
            key corresponds to a level in v_level_indexes, and
            controls how that key is sorted. If None, keys are sorted
            as-is.

        v_level_titles: An optional iterable of strings, where each
            string is a title which corresponds to a level in v_level_indexes,
            and which will be displayed against the row keys for that level.
            If None, no titles will be included.

        h_level_titles: An optional iterable of strings, where each
            string is a title which corresponds to a level in h_level_indexes,
            and which will be displayed against the column keys for that level.
            If None, no titles will be included.

        empty: An optional string value to use for empty cells.

    Returns:
        A list of lists representing the rows of cells.

    Example:

        tabulate(dict_of_dicts, [0, 1], [])

    """
    level_keys = breadth_first(obj)

    v_level_indexes, h_level_indexes = validate_level_indexes(
        len(level_keys), v_level_indexes, h_level_indexes
    )

    if v_level_visibility is None:
        v_level_visibility = [True] * len(v_level_indexes)
    if h_level_visibility is None:
        h_level_visibility = [True] * len(h_level_indexes)

    table, v_key_tuples, h_key_tuples = tabulate_body(
        obj, level_keys, v_level_indexes, h_level_indexes, v_level_sort_keys, h_level_sort_keys
    )

    table, v_key_tuples = strip_missing_rows(table, v_key_tuples)
    table, h_key_tuples = strip_missing_columns(table, h_key_tuples)
    v_key_tuples = strip_hidden(v_key_tuples, v_level_visibility)
    h_key_tuples = strip_hidden(h_key_tuples, h_level_visibility)
    return assemble_table(
        table, v_key_tuples, h_key_tuples, v_level_titles, h_level_titles, empty=empty
    )


def validate_level_indexes(num_levels, v_level_indexes, h_level_indexes):
    """Ensure that v_level_indexes and h_level_indexes are consistent.

    Args:
        num_levels: The number of levels of keys in the data structure being tabulated.
        v_level_indexes: A sequence of level indexes between zero and num_levels for
            the vertical axis, or None.
        h_level_indexes: A sequence of level indexes between zero and num_levels for for
            the horizontal axis, or None.

    Returns:
        A 2-tuple containing v_level_indexes and h_level_indexes sequences.

    Raises:
        ValueError: If v_level_indexes contains duplicate values.
        ValueError: If h_level_indexes contains duplicate values.
        ValueError: If v_level_indexes contains out of range values.
        ValueError: If h_level_indexes contains out of range values.
        ValueError: If taken together v_level_indexes and h_level_indexes
            do not include all levels from zero to up to, but not including
            num_levels.
        ValueError: If v_level_indexes and h_level_indexes have items in
            common.
    """
    if num_levels < 1:
        raise ValueError("num_levels {} is less than one".format(num_levels))

    all_levels = SortedFrozenSet(range(num_levels))

    if (h_level_indexes is None) and (v_level_indexes is None):
        v_level_indexes = range(0, num_levels, 2)
        h_level_indexes = range(1, num_levels, 2)

    h_level_set = SortedFrozenSet(h_level_indexes)
    v_level_set = SortedFrozenSet(v_level_indexes)

    if h_level_indexes is None:
        h_level_indexes = all_levels - v_level_set
    if v_level_indexes is None:
        v_level_indexes = all_levels - h_level_set

    if len(h_level_indexes) != len(h_level_set):
        raise ValueError("h_level_indexes contains duplicate values")
    if h_level_set and ((h_level_set[0] < 0) or (h_level_set[-1] >= num_levels)):
        raise ValueError("h_level_indexes contains out of range values")
    if len(v_level_indexes) != len(v_level_set):
        raise ValueError("v_level_indexes contains duplicate values")
    if v_level_set and ((v_level_set[0] < 0) or (v_level_set[-1] >= num_levels)):
        raise ValueError("v_level_indexes contains out of range values")

    unmentioned_levels = all_levels - v_level_set - h_level_set
    if len(unmentioned_levels) > 0:
        raise ValueError(
            "v_level_indexes and h_level_indexes do not together include levels {}".format(
                ", ".join(map(str, unmentioned_levels))
            )
        )
    if not h_level_set.isdisjoint(v_level_set):
        raise ValueError("h_level_indexes and v_level_indexes are not disjoint")
    v_level_indexes = list(v_level_indexes)
    h_level_indexes = list(h_level_indexes)
    return v_level_indexes, h_level_indexes


def strip_hidden(key_tuples, visibilities):
    """Filter each tuple according to visibility.

    Args:
        key_tuples: A sequence of tuples of equal length (i.e. rectangular)
        visibilities: A sequence of booleans equal in length to the tuples contained in key_tuples.

    Returns:
        A sequence equal in length to key_tuples where the items are tuples with a length corresponding
        to the number of items in visibility which are True.
    """
    result = []
    for key_tuple in key_tuples:
        if len(key_tuple) != len(visibilities):
            raise ValueError(
                "length of key tuple {} is not equal to length of visibilities {}".format(
                    key_tuple, visibilities
                )
            )
        filtered_tuple = tuple(item for item, visible in zip(key_tuple, visibilities) if visible)
        result.append(filtered_tuple)
    return result


# TODO: Multidimensional arrays. e.g. ndarray
