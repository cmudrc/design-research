"""Verify a workshop participant environment independently of activities."""

from __future__ import annotations

import importlib
import sys
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from tempfile import TemporaryDirectory

EXPECTED_VERSIONS = {
    "design-research": "0.4.0",
    "design-research-agents": "0.6.0",
    "design-research-analysis": "0.3.1",
    "design-research-experiments": "0.3.0",
    "design-research-problems": "0.4.0",
}
REQUIRED_IMPORTS = (
    "anthropic",
    "design_research",
    "design_research_agents",
    "design_research_analysis",
    "design_research_experiments",
    "design_research_problems",
    "google.genai",
    "groq",
    "hmmlearn",
    "ipykernel",
    "matplotlib",
    "nbclient",
    "nbformat",
    "networkx",
    "nevergrad",
    "numpy",
    "openai",
    "pandas",
    "pyDOE3",
    "pymoo",
    "scipy",
    "sklearn",
    "statsmodels",
    "trussme",
)


def run_stack_smoke_check() -> None:
    """Exercise the public stack through one deterministic offline study."""
    import design_research as dr

    problem_id = "decision_laptop_design_profit_maximization"
    agent_id = "SeededRandomBaselineAgent"
    problem = dr.problems.get_problem(problem_id)
    if not problem.metadata.title:
        raise RuntimeError("The packaged problem did not load correctly.")

    with TemporaryDirectory(prefix="workshop-preflight-") as directory:
        output_dir = Path(directory)
        study = dr.experiments.build_strategy_comparison_study(
            dr.experiments.StrategyComparisonConfig(
                study_id="workshop-preflight",
                title="Workshop Preflight",
                description="Verify the installed Design Research stack.",
                bundle=dr.experiments.BenchmarkBundle(
                    bundle_id="workshop-preflight",
                    name="Workshop Preflight",
                    description="One packaged problem and deterministic baseline agent.",
                    problem_ids=(problem_id,),
                    agent_specs=(agent_id,),
                ),
                run_budget=dr.experiments.RunBudget(
                    replicates=1,
                    parallelism=1,
                    max_runs=1,
                ),
                output_dir=output_dir,
            )
        )
        conditions = dr.experiments.build_design(study)
        results = dr.experiments.run_study(
            study,
            conditions=conditions,
            checkpoint=False,
            show_progress=False,
        )
        artifacts = dr.experiments.export_analysis_tables(
            study,
            conditions=conditions,
            run_results=results,
            output_dir=output_dir / "analysis",
            validate_with_analysis_package=True,
        )
        report = dr.analysis.validate_experiment_events(artifacts["events.csv"])

    if len(conditions) != 1 or len(results) != 1:
        raise RuntimeError("The stack smoke study did not produce one result.")
    if results[0].status.value != "success":
        raise RuntimeError(f"The stack smoke study failed: {results[0].error_info}")
    if not report.is_valid:
        raise RuntimeError("The stack smoke study produced invalid analysis artifacts.")


def main() -> int:
    """Print environment evidence and return zero only when every check passes."""
    errors: list[str] = []
    print(f"Python: {sys.version.split()[0]}")
    print(f"Interpreter: {sys.executable}")

    if sys.version_info < (3, 12):
        errors.append("Python 3.12 or newer is required.")
    elif sys.version_info[:2] != (3, 12):
        print("Note: Python 3.12 is recommended for the workshop.")

    if ".venv" not in Path(sys.executable).parts:
        errors.append("The preflight must be run with the workshop .venv interpreter.")

    for module_name in REQUIRED_IMPORTS:
        try:
            importlib.import_module(module_name)
        except Exception as exc:
            errors.append(f"Could not import {module_name}: {type(exc).__name__}: {exc}")
        else:
            print(f"Import: {module_name} [ok]")

    for package_name, expected_version in EXPECTED_VERSIONS.items():
        try:
            installed_version = version(package_name)
        except PackageNotFoundError:
            errors.append(f"Package metadata is missing for {package_name}.")
            continue
        status = "ok" if installed_version == expected_version else "mismatch"
        print(f"Version: {package_name}=={installed_version} [{status}]")
        if installed_version != expected_version:
            errors.append(
                f"Expected {package_name}=={expected_version}; found {installed_version}."
            )

    if not errors:
        try:
            run_stack_smoke_check()
        except Exception as exc:
            errors.append(f"Stack smoke check failed: {type(exc).__name__}: {exc}")
        else:
            print("Stack: problems -> agents -> experiments -> analysis [ok]")

    if errors:
        print("\nPreflight failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("\nPreflight passed. You are ready for the workshop.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
