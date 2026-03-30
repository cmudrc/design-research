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


def test_prompt_framing_walkthrough_uses_public_prompt_workflow_agent() -> None:
    """The live walkthrough should use the sibling-owned prompt workflow agent."""
    source = (EXAMPLES_DIR / "prompt_framing_study.py").read_text(encoding="utf-8")
    assert "_future_stack" not in source
    assert "_workspace_bootstrap" not in source
    assert "PromptWorkflowAgent" in source
    assert "agent_bindings" in source
