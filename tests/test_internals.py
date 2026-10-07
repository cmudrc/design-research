"""Unit tests for internal helper behavior and coverage-critical paths."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from design_research import _lazy
from design_research._version import __version__


def test_module_dir_includes_public_and_existing_names() -> None:
    """module_dir should merge globals and public names without duplicates."""
    names = _lazy.module_dir({"alpha": object(), "beta": object()}, ["beta", "gamma"])
    assert names == ["alpha", "beta", "gamma"]


def test_resolve_lazy_export_raises_attribute_error_for_unknown_name() -> None:
    """Unknown export names should raise an AttributeError."""
    with pytest.raises(AttributeError):
        _lazy.resolve_lazy_export("design_research.problems", {}, "missing")


def test_public_module_exports_requires_explicit_all(monkeypatch: pytest.MonkeyPatch) -> None:
    """Sibling wrappers should fail instead of broadening an accidental API."""
    monkeypatch.setattr(_lazy, "import_module", lambda _name: SimpleNamespace())

    with pytest.raises(AttributeError, match="must define an explicit __all__"):
        _lazy.public_module_exports("example")


@pytest.mark.parametrize("public_names", ["name", ["valid", 3], ["duplicate", "duplicate"]])
def test_public_module_exports_rejects_invalid_all(
    public_names: object,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Require a unique sequence of non-empty string export names."""
    monkeypatch.setattr(
        _lazy,
        "import_module",
        lambda _name: SimpleNamespace(__all__=public_names),
    )

    with pytest.raises((TypeError, ValueError)):
        _lazy.public_module_exports("example")


def test_wrapper_dir_exposes_lazy_exports() -> None:
    """Wrapper modules should expose deferred exports through __dir__."""
    import design_research.agents as agents
    import design_research.analysis as analysis
    import design_research.experiments as experiments
    import design_research.problems as problems

    assert "MultiStepAgent" in dir(agents)
    assert "LlamaCppServerLLMClient" in dir(agents)
    assert "ModelStep" in dir(agents)
    assert "CallableToolConfig" in dir(agents)
    assert "CompiledExecution" in dir(agents)
    assert "RunBudget" in dir(experiments)
    assert "build_prompt_framing_study" in dir(experiments)
    assert "render_significance_brief" in dir(experiments)
    assert "resolve_problem" in dir(experiments)
    assert "integration" in dir(analysis)
    assert "validate_unified_table" in dir(analysis)
    assert "permutation_test" in dir(analysis)
    assert "run_study" in dir(experiments)
    assert "list_problems" in dir(problems)
    assert "Citation" in dir(problems)


def test_version_module_exposes_single_source_of_truth() -> None:
    """Version module should expose the next release version directly."""
    assert __version__ == "0.5.0"
