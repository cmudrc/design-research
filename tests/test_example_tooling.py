"""Tests for example inventory and metrics tooling."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
METRICS_SCRIPT = REPO_ROOT / "scripts" / "generate_examples_metrics.py"
METRICS_PATH = REPO_ROOT / "artifacts" / "examples" / "examples_metrics.json"


def _run_metrics(*, run_live_example: bool) -> dict[str, object]:
    """Generate example metrics and return the parsed artifact."""
    env = os.environ.copy()
    if run_live_example:
        env["RUN_LIVE_EXAMPLE"] = "1"
    else:
        env.pop("RUN_LIVE_EXAMPLE", None)

    subprocess.run(
        [sys.executable, str(METRICS_SCRIPT)],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
        env=env,
    )
    return json.loads(METRICS_PATH.read_text(encoding="utf-8"))


def test_generate_examples_metrics_matches_default_execution_policy() -> None:
    """Default metrics should reflect the deterministic example tier."""
    metrics = _run_metrics(run_live_example=False)

    examples = metrics["examples"]
    inventory = metrics["inventory"]
    public_api = metrics["public_api"]

    assert examples["passed"] == 2
    assert examples["total"] == 2
    assert examples["available"] == 3
    assert examples["skipped"] == 1
    assert examples["run_live_example_enabled"] is False
    assert inventory["example_file_count"] == 3
    assert inventory["default_example_count"] == 2
    assert inventory["opt_in_example_count"] == 1
    assert inventory["opt_in_examples"] == ["examples/prompt_framing_study.py"]
    assert public_api["covered_exports"] == 4
    assert public_api["total_exports"] == 4
    assert public_api["coverage_percent"] == 100.0


def test_generate_examples_metrics_includes_live_walkthrough_when_enabled() -> None:
    """Opting into the live walkthrough should update the active example count."""
    metrics = _run_metrics(run_live_example=True)

    examples = metrics["examples"]
    inventory = metrics["inventory"]

    assert examples["passed"] == 3
    assert examples["total"] == 3
    assert examples["available"] == 3
    assert examples["skipped"] == 0
    assert examples["run_live_example_enabled"] is True
    assert inventory["default_example_count"] == 2
    assert inventory["opt_in_example_count"] == 1
