from itertools import chain, repeat, islice, zip_longest, tee, groupby


def pad_infinite(iterable, padding=None):
    return chain(iterable, repeat(padding))


def pad(iterable, size, padding=None):
    return islice(pad_infinite(iterable, padding), size)


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def pairwise_longest(iterable, fillvalue=None):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip_longest(a, b, fillvalue=fillvalue)


def is_sorted(iterable, key=lambda x: x):
    return all(a <= b for a, b in pairwise((key(item) for item in iterable)))


# def unchain(iterable):
#     """Convert an iterable into an infinite series of lists of containing zero or one items.
#     """
#     if iterable is not None:
#         for item in iterable:
#             yield [item]
#     while True:
#         yield []


def one(item):
    yield item


def extend(iterable, item_factory=lambda: None):
    return chain(iterable, iter(item_factory, object()))


def unchain(iterable, box=None):
    if box is None:
        box = lambda item: [item]
    return chain(map(box, iterable))


def extended_unchain(iterable, box=list):
    """Convert an iterable into an infinite series of lists of containing zero or one items.
    """
    return extend(unchain(iterable, box), box)


def empty_iterable():
    yield from ()


def run_length_encode(items):
    return ((key, len(list(group))) for key, group in groupby(items))

def key_for_value(d, v):
    return next(key for key, value in d.items() if value == v)