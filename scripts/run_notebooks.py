"""Execute tutorial notebooks reproducibly with the active Python kernel."""

from __future__ import annotations

import argparse
from pathlib import Path

import nbformat
from nbclient import NotebookClient

from _example_support import active_examples

REPO_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_ROOT = REPO_ROOT / "examples" / "tutorials"


def discover_notebooks() -> tuple[Path, ...]:
    """Return tutorial notebooks in deterministic path order."""
    return active_examples(tuple(sorted(NOTEBOOK_ROOT.glob("*.ipynb"))))


def execute_notebook(path: Path, *, in_place: bool = False) -> None:
    """Execute one notebook and optionally persist its refreshed outputs."""
    notebook = nbformat.read(path, as_version=4)
    client = NotebookClient(
        notebook,
        timeout=180,
        kernel_name="python3",
        allow_errors=False,
        record_timing=False,
        resources={"metadata": {"path": str(REPO_ROOT)}},
    )
    client.execute()
    if in_place:
        nbformat.write(notebook, path)
    print(f"Executed {path.relative_to(REPO_ROOT)}", flush=True)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("notebooks", nargs="*", type=Path)
    parser.add_argument(
        "--in-place",
        action="store_true",
        help="Save refreshed cell outputs back to each notebook.",
    )
    return parser.parse_args()


def main() -> int:
    """Execute selected notebooks or the complete focused tutorial set."""
    args = parse_args()
    paths = tuple(path.resolve() for path in args.notebooks) or discover_notebooks()
    if not paths:
        raise RuntimeError(f"No notebooks found under {NOTEBOOK_ROOT}.")
    for path in paths:
        execute_notebook(path, in_place=args.in_place)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
