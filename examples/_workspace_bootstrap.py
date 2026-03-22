"""Helpers for running umbrella examples against sibling workspace checkouts."""

from __future__ import annotations

import os
import sys
from pathlib import Path


def bootstrap_sibling_sources() -> tuple[str, ...]:
    """Add sibling repository `src/` directories to `sys.path` when present."""
    workspace_root = Path(
        os.getenv("DESIGN_RESEARCH_WORKSPACE_ROOT", Path(__file__).resolve().parents[2])
    )
    candidate_paths = (
        workspace_root / "design-research-agents-april-merge75" / "src",
        workspace_root / "design-research-agents" / "src",
        workspace_root / "design-research-experiments" / "src",
        workspace_root / "design-research-problems" / "src",
        workspace_root / "design-research-analysis" / "src",
    )

    inserted: list[str] = []
    for path in candidate_paths:
        path_text = str(path)
        if not path.exists() or path_text in sys.path:
            continue
        sys.path.insert(0, path_text)
        inserted.append(path_text)
    return tuple(inserted)


__all__ = ["bootstrap_sibling_sources"]
