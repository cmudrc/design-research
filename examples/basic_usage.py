"""Minimal example usage for the umbrella package."""

from __future__ import annotations

import importlib

from _workspace_bootstrap import bootstrap_sibling_sources

bootstrap_sibling_sources()

dr = importlib.import_module("design_research")


def main() -> None:
    """Print top-level discovery information and one real packaged problem preview."""
    problem_ids = dr.problems.list_problems()
    sample_problem_id = "gmpb_default_dynamic_min"
    sample_problem = dr.problems.get_problem(sample_problem_id)
    sample_metadata = sample_problem.metadata

    print("Submodules:", ", ".join(name for name in dr.__all__ if name != "__version__"))
    print("Agents module:", dr.agents.__name__)
    print("Analysis module:", dr.analysis.__name__)
    print("Experiments module:", dr.experiments.__name__)
    print("Problems module:", dr.problems.__name__)
    print("Packaged problems:", len(problem_ids))
    print(
        "Sample problem:",
        f"{sample_metadata.problem_id} -> {sample_metadata.title} [{sample_metadata.kind.value}]",
    )
    print("Strategy builder available:", hasattr(dr.experiments, "build_strategy_comparison_study"))
    print("Unified-table validator available:", hasattr(dr.analysis, "validate_unified_table"))
    print("Version:", dr.__version__)


if __name__ == "__main__":
    main()
