"""Unit tests for internal helper behavior and coverage-critical paths."""

from __future__ import annotations

import importlib
import importlib.metadata
from types import SimpleNamespace

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
    assert "CallableToolConfig" in dir(agents)
    assert "RunBudget" in dir(experiments)
    assert "build_prompt_framing_study" in dir(experiments)
    assert "render_significance_brief" in dir(experiments)
    assert "validate_unified_table" in dir(analysis)
    assert "permutation_test" in dir(analysis)
    assert "run_study" in dir(experiments)
    assert "list_problems" in dir(problems)
    assert "Citation" in dir(problems)


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


def test_experiments_compat_resolve_problem_uses_library_helper_when_needed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Compatibility resolver should defer to the sibling helper when no packaged problem loads."""
    from design_research import _experiments_compat as compat

    sentinel = object()
    monkeypatch.setattr(compat, "_load_packaged_problem", lambda _problem_id: None)
    experiments_module = SimpleNamespace(resolve_problem=lambda _problem_id: sentinel)
    assert compat.resolve_problem(experiments_module, problem_id="demo_problem") is sentinel


def test_experiments_compat_resolve_problem_falls_back_to_problem_packet(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Compatibility resolver should synthesize a packet when no helper exists."""
    from design_research import _experiments_compat as compat

    class _ProblemPacket:
        def __init__(self, **kwargs: object) -> None:
            self.__dict__.update(kwargs)

    monkeypatch.setattr(compat, "_load_packaged_problem", lambda _problem_id: None)
    experiments_module = SimpleNamespace(ProblemPacket=_ProblemPacket)

    packet = compat.resolve_problem(experiments_module, problem_id="demo_problem")

    assert packet.problem_id == "demo_problem"
    assert packet.family == "unknown"
    assert packet.brief == "demo_problem"
    assert packet.payload == {"problem_id": "demo_problem"}
    assert packet.metadata == {}


def test_experiments_compat_normalizes_packaged_problem_evaluations(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Packaged problems should become experiment packets with canonical evaluator rows."""
    from design_research import _experiments_compat as compat

    class _ProblemPacket:
        def __init__(self, **kwargs: object) -> None:
            self.__dict__.update(kwargs)

    metadata = SimpleNamespace(
        problem_id="demo_problem",
        kind=SimpleNamespace(value="decision"),
        title="Demo Problem",
        summary="A packaged demo problem.",
        capabilities=("tradeoff_reasoning",),
        study_suitability=("agent",),
    )

    class _Problem:
        option_factors = (SimpleNamespace(key="choice", levels=(1, 2, 3)),)

        def render_brief(self, include_citation: bool = False) -> str:
            assert include_citation is False
            return "Choose one allowed factor level."

        def evaluate(self, _candidate: object) -> object:
            return SimpleNamespace(
                objective_metric="score",
                objective_value=0.75,
                higher_is_better=True,
                expected_demand_units=12,
                utility=0.5,
            )

    _Problem.metadata = metadata

    monkeypatch.setattr(
        compat, "problems", SimpleNamespace(get_problem=lambda _problem_id: _Problem())
    )
    packet = compat.resolve_problem(
        SimpleNamespace(ProblemPacket=_ProblemPacket),
        problem_id="demo_problem",
    )

    rows = packet.evaluator({"candidate": {"choice": 2}})

    assert packet.problem_id == "demo_problem"
    assert packet.family == "decision"
    assert packet.brief == "Choose one allowed factor level."
    assert packet.metadata["title"] == "Demo Problem"
    assert rows[0]["metric_name"] == "score"
    assert rows[0]["notes_json"] == {"higher_is_better": True}
    assert rows[1]["metric_name"] == "expected_demand_units"
    assert rows[2]["metric_name"] == "utility"


def test_experiments_compat_problem_brief_family_and_row_normalization_fallbacks() -> None:
    """Internal helpers should cover the remaining brief, family, and row-shape fallbacks."""
    from design_research import _experiments_compat as compat

    class _RenderWithoutKwargs:
        def render_brief(self) -> str:
            return "Rendered without keyword args."

    assert compat._problem_brief(_RenderWithoutKwargs(), fallback="fallback") == (
        "Rendered without keyword args."
    )
    assert (
        compat._problem_brief(
            SimpleNamespace(statement_markdown="Statement markdown"), fallback="fallback"
        )
        == "Statement markdown"
    )
    assert compat._problem_brief(SimpleNamespace(statement_markdown=""), fallback="fallback") == (
        "fallback"
    )

    assert (
        compat._problem_family(
            SimpleNamespace(family="optimization"),
            metadata=SimpleNamespace(kind=None),
        )
        == "optimization"
    )
    assert (
        compat._problem_family(
            SimpleNamespace(),
            metadata=SimpleNamespace(kind=None),
        )
        == "unknown"
    )

    single_row = compat._normalize_evaluation_rows(
        {"objective_metric": "quality", "objective_value": 2.5, "notes_json": "bad"}
    )
    sequence_rows = compat._normalize_evaluation_rows(
        [
            {"metric_name": "loss", "metric_value": 0.1, "notes_json": {"alpha": 1}},
            "skip-me",
        ]
    )

    assert single_row == [
        {
            "evaluator_id": "packaged_problem_evaluator",
            "metric_name": "quality",
            "metric_value": 2.5,
            "metric_unit": "unitless",
            "aggregation_level": "run",
            "notes_json": {},
        }
    ]
    assert sequence_rows == [
        {
            "evaluator_id": "packaged_problem_evaluator",
            "metric_name": "loss",
            "metric_value": 0.1,
            "metric_unit": "unitless",
            "aggregation_level": "run",
            "notes_json": {"alpha": 1},
        }
    ]


def test_experiments_compat_seeded_random_baseline_paths() -> None:
    """Seeded baseline helpers should support library, bounds, and error paths."""
    from design_research import _experiments_compat as compat

    sentinel = {"library": "factories"}
    experiments_module = SimpleNamespace(
        make_seeded_random_baseline_factories=lambda: sentinel,
    )
    assert compat.make_seeded_random_baseline_factories(experiments_module) is sentinel

    fallback_factories = compat.make_seeded_random_baseline_factories(SimpleNamespace())
    assert compat.SEEDED_RANDOM_BASELINE_AGENT_ID in fallback_factories

    bounds_problem = SimpleNamespace(bounds=SimpleNamespace(lb=[0.0, 1.0], ub=[1.0, 2.0]))
    problem_packet = SimpleNamespace(
        problem_id="bounded_problem",
        payload={"problem_object": bounds_problem},
    )
    run_spec = SimpleNamespace(run_id="run-123")
    baseline = fallback_factories[compat.SEEDED_RANDOM_BASELINE_AGENT_ID](object())
    result = baseline(problem_packet=problem_packet, run_spec=run_spec, seed=11)

    assert result["metadata"]["request_id"] == "run-123"
    assert len(result["output"]["candidate"]) == 2
    assert 0.0 <= result["output"]["candidate"][0] <= 1.0
    assert 1.0 <= result["output"]["candidate"][1] <= 2.0

    with pytest.raises(RuntimeError):
        compat._fallback_seeded_random_baseline(
            problem_packet=SimpleNamespace(problem_id="bad_problem", payload={}),
            run_spec=run_spec,
            seed=11,
        )

    with pytest.raises(RuntimeError):
        compat._sample_candidate(SimpleNamespace(), seed=11)
