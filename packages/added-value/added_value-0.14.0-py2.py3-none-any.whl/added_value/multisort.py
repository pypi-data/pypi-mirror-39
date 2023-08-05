from natsort import natsort_keygen


class Key(object):
    def __init__(self, func, reverse=False):
        self._func = func
        self._reverse = reverse

    @property
    def func(self):
        return self._func

    @property
    def reverse(self):
        return self._reverse


def identity(x):
    return x


def asc(func=identity):
    """Obtain a key for ascending sort."""
    return Key(func, reverse=False)


def dec(func=identity):
    """Obtain a key for descending sort."""
    return Key(func, reverse=True)


# Returns the same key value for all x, so
# stable sort will maintain order.
_as_is = Key(func=lambda x: 0)


def as_is():
    """Obtain a key for a neutral sort."""
    return _as_is


def multisorted(items, *keys):
    """Sort by multiple attributes.

    Args:
        items: An iterable series to be sorted.
        *keys: Key objects which extract key values from the items.
            The first key will be the most significant, and the
            last key the least significant. If no key functions
            are provided, the items will be sorted in ascending
            natural order.
    Returns:
        A list of items sorted according to keys.
    """
    if len(keys) == 0:
        keys = [asc()]
    for key in reversed(keys):
        items = sorted(items, key=key.func, reverse=key.reverse)
    return items


def tuplesorted(items, *keys):
    """Sort by tuples with a different key for each item.

    Args:
        items: An iterable series of sequences (typically tuples)

        *keys: Key objects which transform individual elements of
           each tuple into sort keys. The zeroth object
           transforms the zeroth element of each tuple, the first
           key object transforms the first element of each tuple,
           and so on.
    Returns:
        A list of items sorted according to keys.
    """
    # Transform the keys so each works on one item of the tuple
    tuple_keys = [
        Key(func=lambda t, i=index, k=key: k.func(t[i]), reverse=key.reverse)
        for index, key in enumerate(keys)
    ]
    return multisorted(items, *tuple_keys)
