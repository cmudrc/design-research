"""Tests for the curated top-level umbrella API."""

from __future__ import annotations

import design_research as dr


def test_public_exports_match_the_curated_api() -> None:
    """Keep the top-level exports explicit and stable."""
    assert dr.__all__ == ["__version__", "agents", "analysis", "experiments", "problems"]


def test_top_level_submodules_are_importable() -> None:
    """Expose sibling wrapper submodules from the package root."""
    from design_research import agents, analysis, experiments, problems

    assert problems.__name__ == "design_research.problems"
    assert agents.__name__ == "design_research.agents"
    assert experiments.__name__ == "design_research.experiments"
    assert analysis.__name__ == "design_research.analysis"
