
import random


def randomize(edges, attempts, seed):
    """
    Generate one randomized directed graph using double-edge swaps.

    Rejected swaps still count as attempts.
    The original graph is never modified.
    """

    rng = random.Random(seed)

    randomized_edges = list(edges)
    edge_set = set(randomized_edges)

    # Calculate original in-degree and out-degree.
    nodes = set()

    for u, v in edges:
        nodes.add(u)
        nodes.add(v)

    original_in = {node: 0 for node in nodes}
    original_out = {node: 0 for node in nodes}

    for u, v in edges:
        original_out[u] += 1
        original_in[v] += 1

    # Perform swap attempts.
    for _ in range(attempts):

        if len(randomized_edges) < 2:
            break

        # Select two distinct edges uniformly.
        i, j = rng.sample(range(len(randomized_edges)), 2)

        a, b = randomized_edges[i]
        c, d = randomized_edges[j]

        new_edge_1 = (a, d)
        new_edge_2 = (c, b)

        # Reject self-loops.
        if a == d or c == b:
            continue

        # Reject edges that already exist.
        if new_edge_1 in edge_set or new_edge_2 in edge_set:
            continue

        # Remove old edges.
        edge_set.remove((a, b))
        edge_set.remove((c, d))

        # Add new edges.
        edge_set.add(new_edge_1)
        edge_set.add(new_edge_2)

        randomized_edges[i] = new_edge_1
        randomized_edges[j] = new_edge_2

    # Verify degree preservation.
    randomized_in = {node: 0 for node in nodes}
    randomized_out = {node: 0 for node in nodes}

    for u, v in randomized_edges:
        randomized_out[u] += 1
        randomized_in[v] += 1

    assert original_in == randomized_in, "In-degrees changed!"
    assert original_out == randomized_out, "Out-degrees changed!"

    return randomized_edges


def generate_random_networks(edges, attempts, count, seed):
    """
    Generate multiple independent randomized graphs.

    The seed is used as the base seed.
    Each network receives a different, reproducible seed.
    """

    networks = []

    for i in range(count):
        network = randomize(edges, attempts, seed + i)
        networks.append(network)

    return networks
