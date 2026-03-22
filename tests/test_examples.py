"""Tests for bundled umbrella examples."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLES_DIR = REPO_ROOT / "examples"


def _run_example(example_name: str, *, tmp_path: Path) -> subprocess.CompletedProcess[str]:
    """Execute one example script in an isolated subprocess."""
    env = os.environ.copy()
    env["PYTHONPATH"] = str(REPO_ROOT / "src")
    env["DESIGN_RESEARCH_WORKSPACE_ROOT"] = str(tmp_path / "missing-workspace")

    return subprocess.run(
        [sys.executable, str(EXAMPLES_DIR / example_name)],
        cwd=tmp_path,
        check=True,
        capture_output=True,
        text=True,
        env=env,
    )


def test_basic_usage_example_executes(tmp_path: Path) -> None:
    """The import-surface smoke example should execute successfully."""
    completed = _run_example("basic_usage.py", tmp_path=tmp_path)
    assert "Submodules: agents, analysis, experiments, problems" in completed.stdout
    assert "Packaged problems:" in completed.stdout


def test_real_stack_interoperability_example_executes(tmp_path: Path) -> None:
    """The portable real-stack example should export artifacts and validate events."""
    completed = _run_example("real_stack_interoperability.py", tmp_path=tmp_path)
    assert "Problem ID: decision_laptop_design_profit_maximization" in completed.stdout
    assert "Run status: success" in completed.stdout
    assert "Event rows valid: True" in completed.stdout


def test_mechanical_design_stack_example_executes(tmp_path: Path) -> None:
    """The mechanical-stack walkthrough should complete with canonical artifacts."""
    completed = _run_example("mechanical_design_stack.py", tmp_path=tmp_path)
    assert "Study problem: treadle_pump_ide_material_min" in completed.stdout
    assert "Runs: 1 (success)" in completed.stdout
    assert "Event rows valid: True" in completed.stdout


def test_prompt_framing_walkthrough_bootstraps_workspace_sources() -> None:
    """The live walkthrough should opt into sibling April workspace bootstrapping."""
    source = (EXAMPLES_DIR / "prompt_framing_study.py").read_text(encoding="utf-8")
    assert "from _workspace_bootstrap import bootstrap_sibling_sources" in source
    assert "bootstrap_sibling_sources()" in source
