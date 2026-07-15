"""Discover packaged problems and inspect their executable contracts."""

from __future__ import annotations

import design_research_problems as problems


def main() -> None:
    """Select one decision problem and inspect one optimization problem."""
    matches = problems.search_problem_summaries(
        text="laptop",
        kind=problems.ProblemKind.DECISION,
    )
    selected = matches[0]
    decision_problem = problems.get_problem_as(
        selected.problem_id,
        problems.DecisionProblem,
    )
    best = decision_problem.best_evaluation()

    optimization_problem = problems.get_problem_as(
        "planar_truss_span_mass_min",
        problems.OptimizationProblem,
    )
    hints = optimization_problem.solver_hints()

    print("Catalog entries:", len(problems.list_problems()))
    print("Selected problem:", selected.problem_id)
    print("Problem kind:", selected.kind.value)
    print("Best candidate:", best.candidate_label)
    print("Best market-share proxy:", f"{best.objective_value:.4f}")
    print("Optimization problem:", hints["problem_id"])
    print("Decision variables:", hints["variable_count"])
    print("Recommended solver:", hints["recommended_solver_family"])


if __name__ == "__main__":
    main()
