"""Tests for the curated top-level umbrella API."""

from __future__ import annotations

import json
import subprocess
import sys

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
    assert dr.__version__ == "0.4.0"


def test_root_import_defers_component_and_sibling_modules() -> None:
    """Keep a root import isolated until one component is requested."""
    source = """
import json
import sys

import design_research as dr

before = sorted(
    name
    for name in sys.modules
    if name.startswith("design_research_")
    or name in {
        "design_research.agents",
        "design_research.analysis",
        "design_research.experiments",
        "design_research.problems",
    }
)
root_dir = dir(dr)
from design_research import problems
after = sorted(
    name
    for name in sys.modules
    if name.startswith("design_research_")
    or name in {
        "design_research.agents",
        "design_research.analysis",
        "design_research.experiments",
        "design_research.problems",
    }
)
print(json.dumps({"before": before, "after": after, "root_dir": root_dir}))
"""
    completed = subprocess.run(
        [sys.executable, "-c", source],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(completed.stdout)

    assert payload["before"] == []
    assert "problems" in payload["root_dir"]
    assert "design_research.problems" in payload["after"]
    assert "design_research_problems" in payload["after"]
    assert "design_research.agents" not in payload["after"]
    assert "design_research_agents" not in payload["after"]
