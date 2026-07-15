"""Estimate agreement among researchers coding design protocols."""

from __future__ import annotations

import design_research_analysis as analysis


def main() -> None:
    """Compute three nominal reliability estimates with seeded intervals."""
    codings = [
        ["problem", "problem", "problem"],
        ["solution", "problem", "problem"],
        ["evaluation", "evaluation", "evaluation"],
        ["solution", "solution", "solution"],
        ["problem", "solution", "solution"],
        ["evaluation", "evaluation", None],
    ]

    for method in ("cohen_kappa", "fleiss_kappa", "krippendorff_alpha"):
        method_codings = [row[:2] for row in codings] if method == "cohen_kappa" else codings
        result = analysis.compute_interrater_reliability(
            method_codings,
            method=method,
            n_bootstrap=100,
            seed=17,
        )
        low, high = result.confidence_interval or (float("nan"), float("nan"))
        print(
            method,
            f"coefficient={result.coefficient:.3f}",
            f"interval=({low:.3f}, {high:.3f})",
            f"items={result.n_items_used}/{result.n_items}",
            f"missing={result.missing_ratings}",
        )


if __name__ == "__main__":
    main()
