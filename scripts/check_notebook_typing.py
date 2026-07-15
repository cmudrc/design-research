"""Type-check the Python source embedded in first-party tutorial notebooks."""

from __future__ import annotations

import tempfile
from pathlib import Path

import nbformat
from mypy import api as mypy_api

REPO_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_ROOT = REPO_ROOT / "examples" / "tutorials"


def notebook_source(path: Path) -> str:
    """Return code cells from one notebook as a Python module."""
    notebook = nbformat.read(path, as_version=4)
    code_cells = [
        str(cell.source)
        for cell in notebook.cells
        if cell.cell_type == "code" and str(cell.source).strip()
    ]
    return "from __future__ import annotations\n\n" + "\n\n".join(code_cells) + "\n"


def main() -> int:
    """Extract and strictly type-check every focused tutorial notebook."""
    notebooks = tuple(sorted(NOTEBOOK_ROOT.glob("*.ipynb")))
    if not notebooks:
        raise RuntimeError(f"No notebooks found under {NOTEBOOK_ROOT}.")

    with tempfile.TemporaryDirectory(prefix="design-research-notebooks-") as temp_dir:
        source_paths: list[str] = []
        for notebook in notebooks:
            source_path = Path(temp_dir) / f"{notebook.stem}.py"
            source_path.write_text(notebook_source(notebook), encoding="utf-8")
            source_paths.append(str(source_path))

        stdout, stderr, status = mypy_api.run(
            [
                "--strict",
                "--no-incremental",
                "--disable-error-code=import-untyped",
                *source_paths,
            ]
        )
    if stdout:
        print(stdout, end="")
    if stderr:
        print(stderr, end="")
    return status


if __name__ == "__main__":
    raise SystemExit(main())
