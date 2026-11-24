
from pathlib import Path

from src.graph_utils import (
    load_departments,
    load_edges,
    clean_edges,
    count_internal_edges,
    rank_top_departments,
    derive_parameters,
    subgraph
)

from src.significance import analyze_department


# Project parameter
R = 1533

# Locate the data files relative to the project directory.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DEPARTMENT_FILE = PROJECT_ROOT / "data" / "email-Eu-core-department-labels.txt"
EDGE_FILE = PROJECT_ROOT / "data" / "email-Eu-core.txt"


def main():

    # T1: Load the dataset.
    departments = load_departments(DEPARTMENT_FILE)
    edges = load_edges(EDGE_FILE)

    # Clean the original edge list.
    edges = clean_edges(edges)

    # Identify the top 20 departments.
    internal_counts = count_internal_edges(edges, departments)
    top20 = rank_top_departments(internal_counts)

    top20_department_ids = [
        department_id for department_id, count in top20
    ]

    # Derive the assigned departments and parameters.
    parameters = derive_parameters(R, top20_department_ids)

    department_A = parameters["department_A"]
    department_B = parameters["department_B"]

    number_of_networks = parameters["number_of_networks"]
    attempts_multiplier = parameters["attempts_multiplier"]
    seed = parameters["random_seed"]

    print("\nPROJECT PARAMETERS")
    print("------------------")
    print("R:", R)
    print("Department A:", department_A)
    print("Department B:", department_B)
    print("Random networks:", number_of_networks)
    print("Attempts multiplier:", attempts_multiplier)
    print("Random seed:", seed)

    # Extract the original subgraphs.
    nodes_A, edges_A = subgraph(department_A, departments, edges)
    nodes_B, edges_B = subgraph(department_B, departments, edges)

    # T6: Analyze Department A.
    counts_A, z_scores_A = analyze_department(
        nodes_A,
        edges_A,
        number_of_networks,
        attempts_multiplier,
        seed
    )

    # T6: Analyze Department B.
    counts_B, z_scores_B = analyze_department(
        nodes_B,
        edges_B,
        number_of_networks,
        attempts_multiplier,
        seed
    )

    # Display Department A results.
    # T4: Display the actual triad counts for both departments.
    print("\nT4: TRIAD CENSUS")
    print("=" * 55)
    print(f"{'Class':<12}{'Department A':>18}{'Department B':>18}")
    print("-" * 55)

    for i in range(13):
        print(
            f"{i + 1:<12}"
            f"{counts_A[i]:>18}"
            f"{counts_B[i]:>18}"
        )

    # T6: Display Z-scores for both departments.
    print("\nT6: TRIAD Z-SCORES")
    print("=" * 55)
    print(f"{'Class':<12}{'Department A':>18}{'Department B':>18}")
    print("-" * 55)

    for i in range(13):
        print(
            f"{i + 1:<12}"
            f"{z_scores_A[i]:>18.4f}"
            f"{z_scores_B[i]:>18.4f}"
        )

    # Classify each triad according to the assignment thresholds.
    print("\nT6: MOTIF CLASSIFICATION")
    print("=" * 55)
    print(f"{'Class':<12}{'Department A':>18}{'Department B':>18}")
    print("-" * 55)

    for i in range(13):
        def classify(score):
            if score > 2:
                return "Motif"
            elif score < -2:
                return "Anti-motif"
            return "Neither"

        print(
            f"{i + 1:<12}"
            f"{classify(z_scores_A[i]):>18}"
            f"{classify(z_scores_B[i]):>18}"
        )
if __name__ == "__main__":
    main()
