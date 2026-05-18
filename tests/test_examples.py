"""Tests for bundled umbrella examples."""

from __future__ import annotations

import subprocess
from pathlib import Path

from tests._subprocess_support import REPO_ROOT, run_python_script, subprocess_env

EXAMPLES_DIR = REPO_ROOT / "examples"


def _run_example(example_name: str, *, tmp_path: Path) -> subprocess.CompletedProcess[str]:
    """Execute one example script in an isolated subprocess."""
    return run_python_script(
        EXAMPLES_DIR / example_name,
        cwd=tmp_path,
        env=subprocess_env(workspace_root=REPO_ROOT.parent),
    )


def test_canonical_artifact_flow_example_executes(tmp_path: Path) -> None:
    """The canonical flow should exercise the full public umbrella handoff."""
    completed = _run_example("canonical_artifact_flow.py", tmp_path=tmp_path)
    assert "Canonical artifact flow: canonical_artifact_flow" in completed.stdout
    assert "Package path: problems -> agents -> experiments -> analysis" in completed.stdout
    assert "Problem: Decision Problem - Student Laptop Design Under Choice-Based Demand" in (
        completed.stdout
    )
    assert "Agent: SeededRandomBaselineAgent" in completed.stdout
    assert "Runs: 2 (2 success)" in completed.stdout
    assert "Mean primary_outcome:" in completed.stdout
    assert "Event rows valid: True" in completed.stdout


def test_student_laptop_design_study_example_executes(tmp_path: Path) -> None:
    """The student laptop study should report real packaged benchmark results."""
    completed = _run_example("student_laptop_design_study.py", tmp_path=tmp_path)
    assert "Study: student_laptop_design_study" in completed.stdout
    assert "Application: Decision Problem - Student Laptop Design Under Choice-Based Demand" in (
        completed.stdout
    )
    assert "Runs: 1 (success)" in completed.stdout
    assert "Observed results:" in completed.stdout
    assert "Event rows valid: True" in completed.stdout


def test_pump_and_battery_design_portfolio_example_executes(tmp_path: Path) -> None:
    """The engineering portfolio example should report real benchmark results."""
    completed = _run_example("pump_and_battery_design_portfolio.py", tmp_path=tmp_path)
    assert "Executed study: pump_and_battery_design_portfolio" in completed.stdout
    assert "Runs: 3 (" in completed.stdout
    assert "Observed benchmark results:" in completed.stdout
    assert "Event rows valid: True" in completed.stdout


def test_long_agent_markov_comparison_example_executes(tmp_path: Path) -> None:
    """The long-process example should compare condition-specific Markov chains."""
    completed = _run_example("long_agent_markov_comparison.py", tmp_path=tmp_path)
    assert "Long agent Markov comparison: long_agent_markov_comparison" in completed.stdout
    assert "Actions per run: 30" in completed.stdout
    assert "Runs: 20" in completed.stdout
    assert "Event rows valid: True" in completed.stdout
    assert "Transition matrix delta:" in completed.stdout


def test_model_size_sweep_regression_example_executes(tmp_path: Path) -> None:
    """The model-size example should regress outcomes from artifacts."""
    completed = _run_example("model_size_sweep_regression.py", tmp_path=tmp_path)
    assert "Model size sweep regression: model_size_sweep_regression" in completed.stdout
    assert "Model class: scripted-open-class" in completed.stdout
    assert "Runs: 20" in completed.stdout
    assert "Regression samples: 20" in completed.stdout
    assert "Coefficient model_size_b:" in completed.stdout


def test_partial_factorial_ideation_regression_example_executes(tmp_path: Path) -> None:
    """The partial-factorial example should fit a linear model from artifacts."""
    completed = _run_example("partial_factorial_ideation_regression.py", tmp_path=tmp_path)
    assert (
        "Partial factorial ideation regression: partial_factorial_ideation_regression"
        in completed.stdout
    )
    assert "Conditions: 12" in completed.stdout
    assert "Runs: 24" in completed.stdout
    assert "Regression samples: 24" in completed.stdout
    assert "Model size coefficient:" in completed.stdout


def test_prompt_framing_walkthrough_uses_public_prompt_workflow_agent() -> None:
    """The live walkthrough should use the sibling-owned prompt workflow agent."""
    source = (EXAMPLES_DIR / "prompt_framing_study.py").read_text(encoding="utf-8")
    assert "_future_stack" not in source
    assert "_workspace_bootstrap" not in source
    assert "build_json_model_workflow" not in source
    assert "read_csv_rows" not in source
    assert "build_json_prompt_workflow" in source
    assert "PromptWorkflowAgent" in source
    assert "agent_bindings" in source
