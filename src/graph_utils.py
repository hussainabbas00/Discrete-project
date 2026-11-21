def load_departments(file_path):
    departments = {}

    with open(file_path, "r") as file:
        for line in file:
            parts = line.split()

            if not parts:
                continue

            node, department = map(int, parts)
            departments[node] = department

    return departments


def load_edges(file_path):
    edges = []

    with open(file_path, "r") as file:
        for line in file:
            parts = line.split()

            if not parts:
                continue

            u, v = map(int, parts)
            edges.append((u, v))

    return edges

def clean_edges(edges):
    cleaned_edges = []
    seen_edges = set()

    self_loops = 0
    duplicates = 0

    for u, v in edges:

        # Remove self-loops
        if u == v:
            self_loops += 1
            continue

        # Remove duplicate edges
        if (u, v) in seen_edges:
            duplicates += 1
            continue

        seen_edges.add((u, v))
        cleaned_edges.append((u, v))

    print("Original edges:", len(edges))
    print("Self-loops removed:", self_loops)
    print("Duplicate edges removed:", duplicates)
    print("Cleaned edges:", len(cleaned_edges))

    return cleaned_edges

def count_internal_edges(edges, departments):
    internal_counts = {}

    # Initialize the count for every department
    for department in departments.values():
        internal_counts[department] = 0

    # Count edges whose endpoints belong to the same department
    for u, v in edges:
        department_u = departments[u]
        department_v = departments[v]

        if department_u == department_v:
            internal_counts[department_u] += 1

    return internal_counts


def rank_top_departments(internal_counts):
    ranked = sorted(
        internal_counts.items(),
        key=lambda item: (-item[1], item[0])
    )

    return ranked[:20]

def derive_parameters(R, top20_department_ids):

    # Generate all 190 pairs in lexicographic order
    pairs = [
        (i, j)
        for i in range(20)
        for j in range(i + 1, 20)
    ]

    # Find our assigned pair
    pair_number = R % 190
    i, j = pairs[pair_number]

    # Find the actual department IDs
    department_A = top20_department_ids[i]
    department_B = top20_department_ids[j]

    # Calculate randomization settings
    number_of_networks = 20 + (R % 31)
    attempts_multiplier = 5 + (R % 6)

    return {
        "R": R,
        "pair_number": pair_number,
        "department_A": department_A,
        "department_B": department_B,
        "number_of_networks": number_of_networks,
        "attempts_multiplier": attempts_multiplier,
        "random_seed": R
    }

def subgraph(department_id, departments, edges):

    # Get all nodes belonging to this department
    department_nodes = {
        node
        for node, department in departments.items()
        if department == department_id
    }

    # Keep only edges with both endpoints in this department
    department_edges = [
        (u, v)
        for u, v in edges
        if u in department_nodes and v in department_nodes
    ]

    return department_nodes, department_edges