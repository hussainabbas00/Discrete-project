
import networkx as nx

from src.graph_utils import (
    load_departments,
    load_edges,
    clean_edges,
    subgraph
)
from src.motifs import census, TRIAD_CODES


# Fixed bit order from the project statement.
BIT_EDGES = [
    (0, 1), (0, 2), (1, 0),
    (1, 2), (2, 0), (2, 1)
]


# Map our 13 classes to NetworkX triad names.
networkx_types = []

for code in TRIAD_CODES:
    graph = nx.DiGraph()
    graph.add_nodes_from([0, 1, 2])

    for bit, edge in enumerate(BIT_EDGES):
        if code & (1 << bit):
            graph.add_edge(*edge)

    result = nx.triadic_census(graph)

    triad_name = next(
        name for name, count in result.items()
        if count == 1
    )

    networkx_types.append(triad_name)


# Load the actual dataset.
departments = load_departments(
    "data/email-Eu-core-department-labels.txt"
)

edges = clean_edges(
    load_edges("data/email-Eu-core.txt")
)


# Verify Departments 14 and 5.
for department_id in [14, 5]:

    nodes, department_edges = subgraph(
        department_id, departments, edges
    )

    # Our implementation.
    our_counts = census(nodes, department_edges)

    # NetworkX verification.
    graph = nx.DiGraph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from(department_edges)

    nx_counts = nx.triadic_census(graph)

    verified_counts = [
        nx_counts[name] for name in networkx_types
    ]

    print(f"\nDepartment {department_id}")
    print("Our counts:       ", our_counts)
    print("NetworkX counts:  ", verified_counts)
    print("Match:", our_counts == verified_counts)

    assert our_counts == verified_counts

print("\nAll verification checks passed!")
