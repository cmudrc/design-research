"""Shared subprocess helpers for example and tooling tests."""

from __future__ import annotations

import os
import subprocess
import sys
from collections.abc import Mapping
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SIBLING_REPOS = (
    "design-research-problems",
    "design-research-agents",
    "design-research-experiments",
    "design-research-analysis",
)


def subprocess_env(
    *,
    workspace_root: Path | None = None,
    updates: Mapping[str, str | None] | None = None,
) -> dict[str, str]:
    """Build a subprocess environment for repo-local test commands."""
    env = os.environ.copy()
    pythonpath_entries = [str(REPO_ROOT / "src")]
    if workspace_root is not None:
        env["DESIGN_RESEARCH_WORKSPACE_ROOT"] = str(workspace_root)
        for repo_name in SIBLING_REPOS:
            src_path = workspace_root / repo_name / "src"
            if src_path.exists():
                pythonpath_entries.append(str(src_path))
    if existing_pythonpath := env.get("PYTHONPATH"):
        pythonpath_entries.append(existing_pythonpath)
    env["PYTHONPATH"] = os.pathsep.join(pythonpath_entries)
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
