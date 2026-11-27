from pathlib import Path
import matplotlib.pyplot as plt


def plot_z_scores(z_scores_A, z_scores_B, dept_A, dept_B, R, output_path):
    """
    T7: Plot grouped bar chart of Z-scores for classes 1-13
    with dashed significance threshold lines at +2 and -2.
    """

    classes = list(range(1, 14))
    bar_width = 0.38

    x_A = [c - bar_width / 2 for c in classes]
    x_B = [c + bar_width / 2 for c in classes]

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.bar(
        x_A,
        z_scores_A,
        width=bar_width,
        label=f"Department A (ID {dept_A})",
        color="#2b6cb0"
    )
    ax.bar(
        x_B,
        z_scores_B,
        width=bar_width,
        label=f"Department B (ID {dept_B})",
        color="#dd6b20"
    )

    ax.axhline(2, color="red", linestyle="--", linewidth=1.2, label="Motif threshold (+2)")
    ax.axhline(-2, color="green", linestyle="--", linewidth=1.2, label="Anti-motif threshold (-2)")
    ax.axhline(0, color="black", linewidth=0.8)

    ax.set_title(
        f"Triad Motif Z-Score Profile: Dept {dept_A} vs Dept {dept_B} (R = {R})",
        fontsize=13,
        fontweight="bold"
    )
    ax.set_xlabel("Triad Class (1-13)", fontsize=11)
    ax.set_ylabel("Z-Score", fontsize=11)
    ax.set_xticks(classes)
    ax.grid(axis="y", linestyle=":", alpha=0.6)
    ax.legend()

    plt.tight_layout()

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_file, dpi=300)
    plt.close(fig)

    print(f"\nT7: Chart saved to {output_file}")