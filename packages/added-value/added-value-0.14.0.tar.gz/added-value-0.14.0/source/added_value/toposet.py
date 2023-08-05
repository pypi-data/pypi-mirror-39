from collections import MutableSet
from itertools import product

from added_value.toposort import topological_sort, Results
from added_value.util import pairwise_longest

_FILL = object()


class TopoSet(MutableSet):
    """A topologically sorted set."""

    def __init__(self, iterable=None):
        self._results = None
        self._edges = []
        self._discarded = set()
        if iterable is not None:
            self.update(iterable)

    def __len__(self):
        return len(self._topo_sorted.sorted) + len(self._topo_sorted.cyclic)

    def __contains__(self, item):
        for pair in self._edges:
            if item in pair:
                return True
        return False

    @property
    def _topo_sorted(self):
        if self._discarded:
            self._do_discard()
            self._results = None
        if self._results is None:
            sorted, cyclic = topological_sort(self._edges)
            self._results = Results(
                sorted=[item for item in sorted if item is not _FILL],
                cyclic=[item for item in cyclic if item is not _FILL],
            )
        return self._results

    def update(self, iterable):
        """Update with an ordered iterable of items.

        Args:
            iterable: An ordered iterable of items. The relative
               order of the items in this iterable will be respected
               in the TopoSet (in the absence of cycles).
        """
        for pair in pairwise_longest(iterable, fillvalue=_FILL):
            self._edges.append(pair)
            self._results = None

    def add(self, value):
        self.update([value])

    def discard(self, value):
        self._discarded.add(value)
        if len(self._discarded) > len(self._edges):
            self._do_discard()

    def _do_discard(self):
        for value in self._discarded:
            sources = [source for source, target in self._edges if target == value]
            targets = [target for source, target in self._edges if source == value]
            if sources or targets:
                self._edges = list(filter(lambda pair: value not in pair, self._edges))
                self._edges.extend(product(sources, targets))

    def has_cycles(self):
        return bool(self._topo_sorted.cyclic)

    def __iter__(self):
        for item in self._topo_sorted.sorted:
            yield item
        for item in self._topo_sorted.cyclic:
            yield item

    @property
    def sorted(self):
        return self._topo_sorted.sorted

    @property
    def cyclic(self):
        return self._topo_sorted.cyclic

    def __repr__(self):
        name = type(self).__name__
        iterable = ", ".join(map(repr, self)) if len(self) > 0 else ""
        return "{}([{}])".format(name, iterable)
