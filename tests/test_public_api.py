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

def test_top_level_namespace_does_not_flatten_wrapper_symbols() -> None:
    """Keep root imports narrow so wrapper submodules own the stable APIs."""
    assert "Study" not in dr.__all__
    assert "Problem" not in dr.__all__
    assert "MultiStepAgent" not in dr.__all__
    assert "validate_unified_table" not in dr.__all__
    assert not hasattr(dr, "Study")
    assert not hasattr(dr, "Problem")
    assert not hasattr(dr, "MultiStepAgent")
    assert not hasattr(dr, "validate_unified_table")


def test_package_version_is_exposed_from_the_top_level() -> None:
    """Expose package metadata without requiring installed distribution metadata."""
    assert dr.__version__ == "0.2.0"
