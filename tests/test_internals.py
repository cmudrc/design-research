"""Unit tests for internal helper behavior and coverage-critical paths."""

from __future__ import annotations

import importlib
import importlib.metadata

import pytest

from design_research import _lazy


def test_module_dir_includes_public_and_existing_names() -> None:
    """module_dir should merge globals and public names without duplicates."""
    names = _lazy.module_dir({"alpha": object(), "beta": object()}, ["beta", "gamma"])
    assert names == ["alpha", "beta", "gamma"]


def test_resolve_lazy_export_raises_attribute_error_for_unknown_name() -> None:
    """Unknown export names should raise an AttributeError."""
    with pytest.raises(AttributeError):
        _lazy.resolve_lazy_export("design_research.problems", {}, "missing")


def test_wrapper_dir_exposes_lazy_exports() -> None:
    """Wrapper modules should expose deferred exports through __dir__."""
    import design_research.agents as agents
    import design_research.analysis as analysis
    import design_research.experiments as experiments
    import design_research.problems as problems

    assert "MultiStepAgent" in dir(agents)
    assert "LlamaCppServerLLMClient" in dir(agents)
    assert "ModelStep" in dir(agents)
    assert "validate_unified_table" in dir(analysis)
    assert "run_study" in dir(experiments)
    assert "list_problems" in dir(problems)


def test_version_module_success_path(monkeypatch: pytest.MonkeyPatch) -> None:
    """Version module should use package metadata when available."""
    monkeypatch.setattr(importlib.metadata, "version", lambda name: "9.9.9")
    module = importlib.reload(importlib.import_module("design_research._version"))
    assert module.__version__ == "9.9.9"


def test_version_module_fallback_path(monkeypatch: pytest.MonkeyPatch) -> None:
    """Version module should fall back when distribution metadata is missing."""

    def _raise(_: str) -> str:
        raise importlib.metadata.PackageNotFoundError

    monkeypatch.setattr(importlib.metadata, "version", _raise)
    module = importlib.reload(importlib.import_module("design_research._version"))
    assert module.__version__ == "0+unknown"
