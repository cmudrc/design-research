"""Shared fresh-process and LaTeX helpers for paper-draft examples."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


def run_fresh_phases(
    script: Path,
    output_dir: Path,
    *,
    require_tectonic: bool = False,
) -> None:
    """Run study execution and draft assembly in consecutive fresh interpreters."""
    destination = output_dir.expanduser().absolute()
    for phase in ("run", "draft"):
        command = [
            sys.executable,
            str(script.resolve()),
            "--phase",
            phase,
            "--output-dir",
            str(destination),
        ]
        if phase == "draft" and require_tectonic:
            command.append("--require-tectonic")
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=120,
        )
        if completed.returncode != 0:
            raise RuntimeError(
                f"Fresh {phase!r} phase failed:\n{completed.stdout}{completed.stderr}"
            )
        print(completed.stdout, end="")


def compile_paper_draft(draft_dir: Path, *, require_tectonic: bool = False) -> bool:
    """Compile ``main.tex`` when Tectonic is available."""
    tectonic = shutil.which("tectonic")
    if tectonic is None:
        if require_tectonic:
            raise RuntimeError("Tectonic is required for this acceptance run.")
        return False
    completed = subprocess.run(
        [tectonic, "main.tex"],
        cwd=draft_dir,
        check=False,
        capture_output=True,
        text=True,
        timeout=90,
    )
    if completed.returncode != 0:
        raise RuntimeError(f"Paper draft did not compile:\n{completed.stdout}{completed.stderr}")
    return True
