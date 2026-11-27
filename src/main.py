"""
CS1005 - Discrete Structures (Fall 2026) Course Project
Finding Network Motifs in an Email Network

Group Parameters:
- Group Number (R): 1533
- Pair Number (R mod 190): 13 -> Top-20 indices (0, 14)
- Department A: 14
- Department B: 5
- Number of Random Networks (20 + R mod 31): 34
- Swap Attempts Multiplier (5 + R mod 6): 8
- Random Seed: 1533
"""

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
from src.visualization import plot_z_scores


# Project parameter
R = 1533

# Locate the data files relative to the project directory.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DEPARTMENT_FILE = PROJECT_ROOT / "data" / "email-Eu-core-department-labels.txt"
EDGE_FILE = PROJECT_ROOT / "data" / "email-Eu-core.txt"
CHART_FILE = PROJECT_ROOT / "results" / f"motif_zscores_R{R}.png"


def classify_z_score(score):
    if score > 2:
        return "Motif"
    if score < -2:
        return "Anti-motif"
    return "Neither"


def main():

    # T1: Load and clean the dataset.
    departments = load_departments(DEPARTMENT_FILE)
    edges = load_edges(EDGE_FILE)
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
    pair_number = parameters["pair_number"]
    number_of_networks = parameters["number_of_networks"]
    attempts_multiplier = parameters["attempts_multiplier"]
    seed = parameters["random_seed"]

    print("\nT1: PROJECT PARAMETERS")
    print("----------------------")
    print("R:", R)
    print("Pair number:", pair_number)
    print("Department A:", department_A)
    print("Department B:", department_B)
    print("Random networks:", number_of_networks)
    print("Attempts multiplier:", attempts_multiplier)
    print("Random seed:", seed)

    # T2: Extract and display the induced subgraphs.
    nodes_A, edges_A = subgraph(department_A, departments, edges)
    nodes_B, edges_B = subgraph(department_B, departments, edges)

    print("\nT2: DEPARTMENT SUBGRAPHS")
    print("------------------------")
    print(f"Department A (ID {department_A}): {len(nodes_A)} nodes, {len(edges_A)} edges")
    print(f"Department B (ID {department_B}): {len(nodes_B)} nodes, {len(edges_B)} edges")

    # T4 & T6: Analyze Department A and Department B.
    counts_A, z_scores_A = analyze_department(
        nodes_A,
        edges_A,
        number_of_networks,
        attempts_multiplier,
        seed
    )

    counts_B, z_scores_B = analyze_department(
        nodes_B,
        edges_B,
        number_of_networks,
        attempts_multiplier,
        seed
    )

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

    # T6: Classify each triad according to the assignment thresholds.
    print("\nT6: MOTIF CLASSIFICATION")
    print("=" * 55)
    print(f"{'Class':<12}{'Department A':>18}{'Department B':>18}")
    print("-" * 55)

    for i in range(13):
        print(
            f"{i + 1:<12}"
            f"{classify_z_score(z_scores_A[i]):>18}"
            f"{classify_z_score(z_scores_B[i]):>18}"
        )

    # T7: Generate grouped bar chart.
    plot_z_scores(
        z_scores_A,
        z_scores_B,
        department_A,
        department_B,
        R,
        CHART_FILE
    )


if __name__ == "__main__":
    main()