"""Execute tutorial notebooks reproducibly with the active Python kernel."""

from __future__ import annotations

import argparse
from pathlib import Path

import nbformat
from nbclient import NotebookClient

from _example_support import active_examples
from _notebook_freshness import read_notebook, stamp_notebook, validate_notebook

REPO_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_ROOT = REPO_ROOT / "examples" / "tutorials"


def discover_notebooks(*, include_live: bool = False) -> tuple[Path, ...]:
    """Return tutorial notebooks in deterministic path order."""
    notebooks = tuple(sorted(NOTEBOOK_ROOT.glob("*.ipynb")))
    return notebooks if include_live else active_examples(notebooks)


def check_notebook(path: Path) -> None:
    """Reject a notebook whose committed outputs do not match its freshness stamp."""
    errors = validate_notebook(read_notebook(str(path)))
    if errors:
        details = "; ".join(errors)
        raise ValueError(f"Stale notebook outputs in {path.relative_to(REPO_ROOT)}: {details}")
    print(f"Fresh {path.relative_to(REPO_ROOT)}", flush=True)


def execute_notebook(path: Path, *, in_place: bool = False) -> None:
    """Execute one notebook and optionally persist its refreshed outputs."""
    if not in_place:
        check_notebook(path)
    notebook = read_notebook(str(path))
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
        stamp_notebook(notebook)
        nbformat.write(notebook, path)
    print(f"Executed {path.relative_to(REPO_ROOT)}", flush=True)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("notebooks", nargs="*", type=Path)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--in-place",
        action="store_true",
        help="Save refreshed cell outputs back to each notebook.",
    )
    mode.add_argument(
        "--check",
        action="store_true",
        help="Validate committed source/output freshness without executing notebooks.",
    )
    return parser.parse_args()


def main() -> int:
    """Execute selected notebooks or the complete focused tutorial set."""
    args = parse_args()
    paths = tuple(path.resolve() for path in args.notebooks) or discover_notebooks(
        include_live=args.check
    )
    if not paths:
        raise RuntimeError(f"No notebooks found under {NOTEBOOK_ROOT}.")
    for path in paths:
        if args.check:
            check_notebook(path)
        else:
            execute_notebook(path, in_place=args.in_place)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
