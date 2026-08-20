"""Verify the IDETC 2026 participant environment and tutorial kit."""

from __future__ import annotations

import importlib
import sys
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

EXPECTED_VERSIONS = {
    "design-research": "0.4.0",
    "design-research-agents": "0.6.0",
    "design-research-analysis": "0.3.1",
    "design-research-experiments": "0.3.0",
    "design-research-problems": "0.4.0",
}
REQUIRED_IMPORTS = (
    "design_research",
    "design_research_agents",
    "design_research_analysis",
    "design_research_experiments",
    "design_research_problems",
    "ipykernel",
    "sklearn",
)
REQUIRED_MATERIALS = (
    "notebooks/problems_text_map.ipynb",
    "notebooks/problems_truss_grammar.ipynb",
    "notebooks/agents_workflow.ipynb",
    "notebooks/experiments_monty_hall.ipynb",
    "notebooks/analysis_reliability.ipynb",
    "scripts/canonical_artifact_flow.py",
    "scripts/long_agent_markov_comparison.py",
    "scripts/partial_factorial_ideation_regression.py",
)


def main() -> int:
    """Print environment evidence and return zero only when every check passes."""
    errors: list[str] = []
    print(f"Python: {sys.version.split()[0]}")
    print(f"Interpreter: {sys.executable}")

    if sys.version_info < (3, 12):
        errors.append("Python 3.12 or newer is required.")
    elif sys.version_info[:2] != (3, 12):
        print("Note: Python 3.12 is recommended for the tutorial.")

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

    kit_root = Path(__file__).resolve().parent
    for relative_path in REQUIRED_MATERIALS:
        if not (kit_root / relative_path).is_file():
            errors.append(f"Tutorial material is missing: {relative_path}")

    if errors:
        print("\nPreflight failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Materials: {len(REQUIRED_MATERIALS)} files [ok]")
    print("\nPreflight passed. You are ready for the tutorial.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
