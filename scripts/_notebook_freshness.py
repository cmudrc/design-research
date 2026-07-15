"""Hash and verify committed notebook source and output evidence."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping

import nbformat
from nbformat import NotebookNode

METADATA_KEY = "design_research_freshness"
SCHEMA_VERSION = 1


def _digest(payload: object) -> str:
    """Return a stable SHA-256 digest for one JSON-compatible payload."""
    serialized = json.dumps(
        payload,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    )
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def source_digest(notebook: NotebookNode) -> str:
    """Return a digest of ordered notebook cell types, ids, and sources."""
    return _digest(
        [
            {
                "cell_type": cell.get("cell_type"),
                "id": cell.get("id"),
                "source": cell.get("source", ""),
            }
            for cell in notebook.cells
        ]
    )


def output_digest(notebook: NotebookNode) -> str:
    """Return a digest of execution counts and outputs for all code cells."""
    return _digest(
        [
            {
                "id": cell.get("id"),
                "execution_count": cell.get("execution_count"),
                "outputs": cell.get("outputs", []),
            }
            for cell in notebook.cells
            if cell.get("cell_type") == "code"
        ]
    )


def stamp_notebook(notebook: NotebookNode) -> None:
    """Record current source and output digests in notebook metadata."""
    notebook.metadata[METADATA_KEY] = {
        "schema_version": SCHEMA_VERSION,
        "source_sha256": source_digest(notebook),
        "output_sha256": output_digest(notebook),
    }


def validate_notebook(notebook: NotebookNode) -> list[str]:
    """Return freshness errors for one loaded notebook."""
    metadata = notebook.metadata.get(METADATA_KEY)
    if not isinstance(metadata, Mapping):
        return [f"missing metadata.{METADATA_KEY}"]
    errors: list[str] = []
    if metadata.get("schema_version") != SCHEMA_VERSION:
        errors.append("unsupported freshness schema version")
    if metadata.get("source_sha256") != source_digest(notebook):
        errors.append("source changed after the saved outputs were recorded")
    if metadata.get("output_sha256") != output_digest(notebook):
        errors.append("saved outputs changed after freshness metadata was recorded")
    return errors


def read_notebook(path: str) -> NotebookNode:
    """Load one notebook using the current nbformat schema."""
    return nbformat.read(path, as_version=4)
