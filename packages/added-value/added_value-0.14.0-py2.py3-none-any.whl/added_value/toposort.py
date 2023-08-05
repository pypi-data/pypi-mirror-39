from collections import defaultdict, namedtuple

Results = namedtuple("Results", ["sorted", "cyclic"])


def topological_sort(dependency_pairs):
    "Sort values subject to dependency constraints"
    num_heads = defaultdict(int)  # num arrows pointing in
    tails = defaultdict(list)  # list of arrows going out
    heads = []  # unique list of heads in order first seen
    for h, t in dependency_pairs:
        num_heads[t] += 1
        if h in tails:
            tails[h].append(t)
        else:
            tails[h] = [t]
            heads.append(h)

    ordered = [h for h in heads if h not in num_heads]
    for h in ordered:
        for t in tails[h]:
            num_heads[t] -= 1
            if not num_heads[t]:
                ordered.append(t)
    cyclic = [n for n, heads in num_heads.items() if heads]
    return Results(ordered, cyclic)
