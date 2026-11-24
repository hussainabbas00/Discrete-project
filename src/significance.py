
import math

from src.motifs import census
from src.randomization import generate_random_networks


def compute_z_scores(real_counts, random_counts):
    """
    Calculate the Z-score for each of the 13 triad classes.

    real_counts: census of the original graph.
    random_counts: list of census results for randomized graphs.

    Returns:
        A list of 13 Z-scores.
    """

    z_scores = []

    # Process each of the 13 triad classes.
    for class_index in range(13):

        # Actual count in the original graph.
        actual = real_counts[class_index]

        # Collect counts for this class from all random graphs.
        values = [
            network[class_index]
            for network in random_counts
        ]

        # Calculate the mean.
        mean = sum(values) / len(values)

        # Calculate population standard deviation.
        variance = sum(
            (value - mean) ** 2
            for value in values
        ) / len(values)

        standard_deviation = math.sqrt(variance)

        # Calculate Z-score.
        if standard_deviation == 0:
            z_score = 0
        else:
            z_score = (actual - mean) / standard_deviation

        z_scores.append(z_score)

    return z_scores


def analyze_department(nodes, edges, number_of_networks, attempts_multiplier, seed):
    """
    Calculate the Z-scores for one department.
    """

    # Count triads in the original department graph.
    real_counts = census(nodes, edges)

    # Calculate the number of swap attempts.
    attempts = attempts_multiplier * len(edges)

    # Generate randomized versions of the original graph.
    random_networks = generate_random_networks(
        edges,
        attempts,
        number_of_networks,
        seed
    )

    # Count triads in every randomized graph.
    random_counts = []

    for network in random_networks:
        counts = census(nodes, network)
        random_counts.append(counts)

    # Calculate the 13 Z-scores.
    z_scores = compute_z_scores(real_counts, random_counts)

    return real_counts, z_scores
