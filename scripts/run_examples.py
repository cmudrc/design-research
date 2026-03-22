"""Run bundled examples using the shared default-versus-opt-in policy."""

from __future__ import annotations

import os
import subprocess
import sys

from _example_support import (
    REPO_ROOT,
    RUN_LIVE_EXAMPLE_ENV,
    active_examples,
    discover_examples,
    example_path_text,
)


def _example_env() -> dict[str, str]:
    """Return the subprocess environment for example execution."""
    env = os.environ.copy()
    src_path = str(REPO_ROOT / "src")
    pythonpath_parts = [part for part in env.get("PYTHONPATH", "").split(os.pathsep) if part]
    if src_path not in pythonpath_parts:
        pythonpath_parts.insert(0, src_path)
    env["PYTHONPATH"] = os.pathsep.join(pythonpath_parts)
    return env


def main() -> int:
    """Run each bundled example that is active in the current mode."""
    examples = discover_examples()
    runnable_examples = set(active_examples(examples))
    env = _example_env()

    for example in examples:
        example_path = example_path_text(example)
        if example not in runnable_examples:
            print(
                f"Skipping {example_path} "
                f"(set {RUN_LIVE_EXAMPLE_ENV}=1 to run opt-in live examples)",
                flush=True,
            )
            continue
        print(f"Running {example_path}", flush=True)
        subprocess.run(
            [sys.executable, str(example)],
            cwd=REPO_ROOT,
            check=True,
            env=env,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
