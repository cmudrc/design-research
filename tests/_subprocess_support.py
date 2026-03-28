"""Shared subprocess helpers for example and tooling tests."""

from __future__ import annotations

import os
import subprocess
import sys
from collections.abc import Mapping
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def subprocess_env(
    *,
    workspace_root: Path | None = None,
    updates: Mapping[str, str | None] | None = None,
) -> dict[str, str]:
    """Build a subprocess environment for repo-local test commands."""
    env = os.environ.copy()
    env["PYTHONPATH"] = str(REPO_ROOT / "src")
    if workspace_root is not None:
        env["DESIGN_RESEARCH_WORKSPACE_ROOT"] = str(workspace_root)
    for key, value in (updates or {}).items():
        if value is None:
            env.pop(key, None)
        else:
            env[key] = value
    return env


def run_python_script(
    script_path: Path,
    *,
    cwd: Path,
    env: Mapping[str, str],
) -> subprocess.CompletedProcess[str]:
    """Execute one Python script with captured output."""
    return subprocess.run(
        [sys.executable, str(script_path)],
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
        env=dict(env),
    )
