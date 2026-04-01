"""Unit tests for internal helper behavior and coverage-critical paths."""

from __future__ import annotations

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
    assert __version__ == "0.2.0"
