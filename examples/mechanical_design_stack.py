"""Mechanical-design stack overview for the umbrella package.

## Introduction
Trace a lightweight mechanical-design workflow through the umbrella package
using packaged structural and humanitarian-product benchmarks.

## Technical Implementation
1. Resolve the top-level agents, problems, experiments, and analysis modules.
2. Load a few representative mechanical engineering problems from the packaged
   problem catalog.
3. Print the experiment-building and analysis entry points that sit on top of
   those wrapped sibling libraries.

## Expected Results
The script prints the wrapped module names, a short summary for each packaged
mechanical problem, and the recommended experiment/analysis hooks for the next
step in a study.
"""

from __future__ import annotations

import design_research as dr

MECHANICAL_PROBLEM_IDS = (
    "space_truss_span_mass_min",
    "battery_pack_18650_series_parallel",
    "treadle_pump_ide_material_min",
)


def _problem_summary(problem_id: str) -> str:
    """Return one short summary line for a packaged mechanical problem."""
    problem = dr.problems.get_problem(problem_id)
    metadata = getattr(problem, "metadata", None)
    title = getattr(metadata, "title", problem_id)
    kind = getattr(getattr(metadata, "kind", None), "value", "unknown")
    return f"{problem_id}: {title} [{kind}]"


def main() -> None:
    """Print a compact mechanical-design workflow overview."""
    stack = {
        "agents": dr.agents.__name__,
        "analysis": dr.analysis.__name__,
        "experiments": dr.experiments.__name__,
        "problems": dr.problems.__name__,
    }
    for name, module_name in stack.items():
        print(f"{name} -> {module_name}")

    print("Mechanical benchmark shortlist:")
    for problem_id in MECHANICAL_PROBLEM_IDS:
        print(f"- {_problem_summary(problem_id)}")

    print("Suggested next steps:")
    print(f"- build study: {dr.experiments.build_strategy_comparison_study.__name__}")
    print(f"- validate runs: {dr.analysis.compare_condition_pairs.__name__}")


if __name__ == "__main__":
    main()
