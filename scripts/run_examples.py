"""Run bundled examples using the shared default-versus-opt-in policy."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

from _example_support import (
    REPO_ROOT,
    discover_examples,
    example_enabled,
    example_path_text,
    opt_in_environment,
    selection_state,
)

RESULTS_PATH = REPO_ROOT / "artifacts" / "examples" / "example_results.json"
type CommandRunner = Callable[..., subprocess.CompletedProcess[Any]]


def _example_env() -> dict[str, str]:
    """Return the subprocess environment for example execution."""
    env = os.environ.copy()
    src_path = str(REPO_ROOT / "src")
    pythonpath_parts = [part for part in env.get("PYTHONPATH", "").split(os.pathsep) if part]
    if src_path not in pythonpath_parts:
        pythonpath_parts.insert(0, src_path)
    env["PYTHONPATH"] = os.pathsep.join(pythonpath_parts)
    return env


def execute_examples(
    examples: tuple[Path, ...],
    *,
    env: dict[str, str],
    command_runner: CommandRunner = subprocess.run,
) -> list[dict[str, object]]:
    """Execute selected examples and return one evidence record per file."""
    results: list[dict[str, object]] = []
    for example in examples:
        example_path = example_path_text(example)
        if not example_enabled(example):
            selection_environment = opt_in_environment(example)
            print(
                f"Skipping {example_path} "
                f"(set {selection_environment}=1 to select this live example)",
                flush=True,
            )
            results.append(
                {
                    "path": example_path,
                    "status": "skipped",
                    "reason": f"{selection_environment}=1 was not selected",
                }
            )
            continue
        print(f"Running {example_path}", flush=True)
        command = _example_command(example)
        completed = command_runner(
            command,
            cwd=REPO_ROOT,
            check=False,
            env=env,
        )
        returncode = int(completed.returncode)
        results.append(
            {
                "path": example_path,
                "status": "passed" if returncode == 0 else "failed",
                "returncode": returncode,
            }
        )
    return results


def write_results(results: list[dict[str, object]]) -> None:
    """Write the current example execution evidence artifact."""
    payload = {
        "schema_version": 1,
        "selection": selection_state(),
        "results": results,
    }
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {RESULTS_PATH}", flush=True)


def main() -> int:
    """Run bundled examples and persist their pass/fail/skip evidence."""
    results = execute_examples(
        discover_examples(),
        env=_example_env(),
    )
    write_results(results)
    return 1 if any(result["status"] == "failed" for result in results) else 0


def _example_command(example: Path) -> list[str]:
    """Return the interpreter command for one script or notebook example."""
    if example.suffix == ".ipynb":
        return [
            sys.executable,
            str(REPO_ROOT / "scripts" / "run_notebooks.py"),
            str(example),
        ]
    return [sys.executable, str(example)]


if __name__ == "__main__":
    raise SystemExit(main())
