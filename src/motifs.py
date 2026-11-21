
from itertools import permutations


# Canonical codes for the 13 connected triad classes.
TRIAD_CODES = [
    3, 6, 7, 10, 11, 15, 21,
    23, 25, 27, 30, 31, 63
]


def triad_class(a, b, c, edges):
    """
    Classify the directed triad formed by nodes a, b, and c.

    Returns:
        1 to 13 for a connected triad.
        None if the triad is disconnected.
    """

    nodes = [a, b, c]
    edge_set = set(edges)

    possible_edges = [
        (0, 1),
        (0, 2),
        (1, 0),
        (1, 2),
        (2, 0),
        (2, 1)
    ]

    codes = []

    # Try all six possible node orderings.
    for ordering in permutations(nodes):

        code = 0

        # Check each of the six possible directed edges.
        for bit, (source, target) in enumerate(possible_edges):

            actual_edge = (
                ordering[source],
                ordering[target]
            )

            if actual_edge in edge_set:
                code += 2 ** bit

        codes.append(code)

    # Smallest code is the canonical code.
    canonical_code = min(codes)

    # Find its class number.
    if canonical_code in TRIAD_CODES:
        return TRIAD_CODES.index(canonical_code) + 1

    return None


from itertools import combinations


def census(nodes, edges):
    """
    Count all 13 connected triad classes in a directed graph.

    Returns a list containing the counts for classes 1 to 13.
    """

    edge_set = set(edges)

    # Step 1: Create an empty neighbour set for every node.
    neighbours = {node: set() for node in nodes}

    # Step 2: Add neighbours in BOTH directions.
    for u, v in edge_set:
        neighbours[u].add(v)
        neighbours[v].add(u)

    # Step 3: Find every distinct connected triple.
    unique_triples = set()

    for v in nodes:
        neighbour_list = sorted(neighbours[v])

        for x, y in combinations(neighbour_list, 2):
            triple = tuple(sorted((v, x, y)))
            unique_triples.add(triple)

    # Step 4: Count the 13 classes.
    counts = [0] * 13

    for a, b, c in unique_triples:
        class_number = triad_class(a, b, c, edge_set)

        if class_number is None:
            raise AssertionError("A disconnected triple was found!")

        counts[class_number - 1] += 1

    # Step 5: Sanity check.
    assert sum(counts) == len(unique_triples)

    return counts
