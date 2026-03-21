"""Smoke tests for lazy wrapper re-exports."""

from __future__ import annotations

import importlib
import sys
from types import ModuleType
from typing import Any


def _install_dependency_stubs() -> dict[str, ModuleType]:
    """Install lightweight stub modules for sibling package imports."""

    def _fn(name: str) -> Any:
        def _inner(
            *args: object, **kwargs: object
        ) -> tuple[str, tuple[object, ...], dict[str, object]]:
            return name, args, kwargs

        return _inner

    problems = ModuleType("design_research_problems")
    for symbol in [
        "Problem",
        "ComputableProblem",
        "ProblemKind",
        "ProblemMetadata",
        "ProblemTaxonomy",
        "ProblemRegistry",
    ]:
        setattr(problems, symbol, type(symbol, (), {}))
    problems.get_problem = _fn("get_problem")
    problems.get_problem_as = _fn("get_problem_as")
    problems.list_problems = _fn("list_problems")
    problems.get_ideation_catalog = _fn("get_ideation_catalog")

    agents = ModuleType("design_research_agents")
    for symbol in [
        "DirectLLMCall",
        "MultiStepAgent",
        "Toolbox",
        "Workflow",
        "ModelStep",
        "LLMRequest",
        "LLMMessage",
        "LlamaCppServerLLMClient",
        "OpenAIServiceLLMClient",
        "OllamaLLMClient",
        "CompiledExecution",
        "ModelSelector",
        "Tracer",
        "TwoSpeakerConversationPattern",
        "DebatePattern",
        "PlanExecutePattern",
        "ProposeCriticPattern",
        "RouterDelegatePattern",
        "RoundBasedCoordinationPattern",
        "BlackboardPattern",
        "BeamSearchPattern",
        "RAGPattern",
    ]:
        setattr(agents, symbol, type(symbol, (), {}))

    experiments = ModuleType("design_research_experiments")
    for symbol in [
        "Study",
        "Hypothesis",
        "OutcomeSpec",
        "AnalysisPlan",
        "Factor",
        "Level",
        "Condition",
        "Constraint",
        "Block",
    ]:
        setattr(experiments, symbol, type(symbol, (), {}))
    experiments.build_design = _fn("build_design")
    experiments.generate_doe = _fn("generate_doe")
    experiments.materialize_conditions = _fn("materialize_conditions")
    experiments.run_study = _fn("run_study")
    experiments.resume_study = _fn("resume_study")
    experiments.validate_study = _fn("validate_study")
    experiments.export_analysis_tables = _fn("export_analysis_tables")

    analysis = ModuleType("design_research_analysis")
    for symbol in ["UnifiedTableConfig", "UnifiedTableValidationReport"]:
        setattr(analysis, symbol, type(symbol, (), {}))
    for symbol in [
        "coerce_unified_table",
        "derive_columns",
        "validate_unified_table",
        "profile_dataframe",
        "validate_dataframe",
        "generate_codebook",
        "fit_markov_chain_from_table",
        "fit_discrete_hmm_from_table",
        "compute_language_convergence",
        "reduce_dimensions",
        "compare_groups",
        "fit_regression",
        "fit_mixed_effects",
    ]:
        setattr(analysis, symbol, _fn(symbol))

    stubs = {
        "design_research_problems": problems,
        "design_research_agents": agents,
        "design_research_experiments": experiments,
        "design_research_analysis": analysis,
    }
    sys.modules.update(stubs)
    return stubs


def test_wrapper_re_exports_are_reachable_via_stubs(monkeypatch: Any) -> None:
    """Resolve representative symbols through each wrapper module."""
    stubs = _install_dependency_stubs()
    for name, module in stubs.items():
        monkeypatch.setitem(sys.modules, name, module)

    problems = importlib.reload(importlib.import_module("design_research.problems"))
    agents = importlib.reload(importlib.import_module("design_research.agents"))
    experiments = importlib.reload(importlib.import_module("design_research.experiments"))
    analysis = importlib.reload(importlib.import_module("design_research.analysis"))

    assert problems.get_problem()[0] == "get_problem"
    assert problems.list_problems()[0] == "list_problems"
    assert agents.MultiStepAgent.__name__ == "MultiStepAgent"
    assert agents.LlamaCppServerLLMClient.__name__ == "LlamaCppServerLLMClient"
    assert agents.ModelStep.__name__ == "ModelStep"
    assert agents.OpenAIServiceLLMClient.__name__ == "OpenAIServiceLLMClient"
    assert agents.PlanExecutePattern.__name__ == "PlanExecutePattern"
    assert experiments.run_study()[0] == "run_study"
    assert experiments.Study.__name__ == "Study"
    assert analysis.validate_unified_table()[0] == "validate_unified_table"
    assert analysis.UnifiedTableConfig.__name__ == "UnifiedTableConfig"
