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
        "__version__",
        "Problem",
        "ComputableProblem",
        "ProblemKind",
        "ProblemMetadata",
        "ProblemTaxonomy",
        "Citation",
        "ProblemAsset",
        "TextProblem",
        "DecisionEvaluation",
        "DecisionProblem",
        "OptimizationProblem",
        "OptimizationEvaluation",
        "GrammarProblem",
        "GrammarTransition",
        "MCPProblem",
        "ProblemRegistry",
        "MissingOptionalDependencyError",
        "ProblemEvaluationError",
        "EvidenceTier",
        "IdeationPromptRecord",
        "IdeationPromptVariant",
        "IdeationPromptFamily",
        "IdeationStudy",
        "IdeationCatalog",
    ]:
        setattr(problems, symbol, type(symbol, (), {}))
    problems.get_problem = _fn("get_problem")
    problems.get_problem_as = _fn("get_problem_as")
    problems.list_problems = _fn("list_problems")
    problems.get_ideation_catalog = _fn("get_ideation_catalog")
    problems.__all__ = [
        "__version__",
        "Problem",
        "ComputableProblem",
        "ProblemKind",
        "ProblemMetadata",
        "ProblemTaxonomy",
        "Citation",
        "ProblemAsset",
        "TextProblem",
        "DecisionEvaluation",
        "DecisionProblem",
        "OptimizationProblem",
        "OptimizationEvaluation",
        "GrammarProblem",
        "GrammarTransition",
        "MCPProblem",
        "ProblemRegistry",
        "MissingOptionalDependencyError",
        "ProblemEvaluationError",
        "EvidenceTier",
        "IdeationPromptRecord",
        "IdeationPromptVariant",
        "IdeationPromptFamily",
        "IdeationStudy",
        "IdeationCatalog",
        "get_problem",
        "get_problem_as",
        "list_problems",
        "get_ideation_catalog",
    ]

    agents = ModuleType("design_research_agents")
    for symbol in [
        "__version__",
        "DirectLLMCall",
        "MultiStepAgent",
        "Toolbox",
        "CallableToolConfig",
        "ScriptToolConfig",
        "MCPServerConfig",
        "LogicStep",
        "ToolStep",
        "DelegateStep",
        "Workflow",
        "ModelStep",
        "DelegateBatchStep",
        "LoopStep",
        "MemoryReadStep",
        "MemoryWriteStep",
        "ExecutionResult",
        "LLMRequest",
        "LLMMessage",
        "LLMResponse",
        "ToolResult",
        "LlamaCppServerLLMClient",
        "AnthropicServiceLLMClient",
        "AzureOpenAIServiceLLMClient",
        "GeminiServiceLLMClient",
        "GroqServiceLLMClient",
        "OpenAIServiceLLMClient",
        "OpenAICompatibleHTTPLLMClient",
        "TransformersLocalLLMClient",
        "MLXLocalLLMClient",
        "VLLMServerLLMClient",
        "OllamaLLMClient",
        "SGLangServerLLMClient",
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
    agents.__all__ = [
        "__version__",
        "DirectLLMCall",
        "MultiStepAgent",
        "Toolbox",
        "CallableToolConfig",
        "ScriptToolConfig",
        "MCPServerConfig",
        "LogicStep",
        "ToolStep",
        "DelegateStep",
        "ModelStep",
        "DelegateBatchStep",
        "LoopStep",
        "MemoryReadStep",
        "MemoryWriteStep",
        "ExecutionResult",
        "LLMRequest",
        "LLMMessage",
        "LLMResponse",
        "ToolResult",
        "Workflow",
        "CompiledExecution",
        "TwoSpeakerConversationPattern",
        "DebatePattern",
        "PlanExecutePattern",
        "ProposeCriticPattern",
        "RouterDelegatePattern",
        "RoundBasedCoordinationPattern",
        "BlackboardPattern",
        "BeamSearchPattern",
        "RAGPattern",
        "AnthropicServiceLLMClient",
        "AzureOpenAIServiceLLMClient",
        "GeminiServiceLLMClient",
        "GroqServiceLLMClient",
        "LlamaCppServerLLMClient",
        "OpenAIServiceLLMClient",
        "OpenAICompatibleHTTPLLMClient",
        "TransformersLocalLLMClient",
        "MLXLocalLLMClient",
        "VLLMServerLLMClient",
        "OllamaLLMClient",
        "SGLangServerLLMClient",
        "ModelSelector",
        "Tracer",
    ]

    experiments = ModuleType("design_research_experiments")
    for symbol in [
        "AgentArchitectureComparisonConfig",
        "Study",
        "Hypothesis",
        "OutcomeSpec",
        "AnalysisPlan",
        "BenchmarkBundle",
        "RunBudget",
        "SeedPolicy",
        "Factor",
        "FactorKind",
        "Level",
        "Condition",
        "Constraint",
        "Block",
        "DiversityAndExplorationConfig",
        "GrammarScaffoldConfig",
        "HumanVsAgentProcessConfig",
        "OptimizationBenchmarkConfig",
        "ProblemPacket",
        "PromptFramingConfig",
        "RecipeStudyConfig",
        "RunResult",
        "RunSpec",
    ]:
        setattr(experiments, symbol, type(symbol, (), {}))
    for symbol in [
        "build_agent_architecture_comparison_study",
        "build_diversity_and_exploration_study",
        "build_grammar_scaffold_study",
        "build_human_vs_agent_process_study",
        "build_optimization_benchmark_study",
        "build_prompt_framing_study",
        "grammar_problem_bundle",
        "human_vs_agent_bundle",
        "ideation_bundle",
        "optimization_bundle",
        "render_codebook",
        "render_markdown_summary",
        "render_methods_scaffold",
        "render_significance_brief",
        "write_markdown_report",
    ]:
        setattr(experiments, symbol, _fn(symbol))
    experiments.build_design = _fn("build_design")
    experiments.generate_doe = _fn("generate_doe")
    experiments.materialize_conditions = _fn("materialize_conditions")
    experiments.run_study = _fn("run_study")
    experiments.resume_study = _fn("resume_study")
    experiments.validate_study = _fn("validate_study")
    experiments.export_analysis_tables = _fn("export_analysis_tables")
    experiments.__all__ = [
        "AgentArchitectureComparisonConfig",
        "AnalysisPlan",
        "BenchmarkBundle",
        "Block",
        "Condition",
        "Constraint",
        "DiversityAndExplorationConfig",
        "Factor",
        "FactorKind",
        "GrammarScaffoldConfig",
        "HumanVsAgentProcessConfig",
        "Hypothesis",
        "Level",
        "OptimizationBenchmarkConfig",
        "OutcomeSpec",
        "ProblemPacket",
        "PromptFramingConfig",
        "RecipeStudyConfig",
        "RunBudget",
        "RunResult",
        "RunSpec",
        "SeedPolicy",
        "Study",
        "build_agent_architecture_comparison_study",
        "build_design",
        "build_diversity_and_exploration_study",
        "build_grammar_scaffold_study",
        "build_human_vs_agent_process_study",
        "build_optimization_benchmark_study",
        "build_prompt_framing_study",
        "export_analysis_tables",
        "generate_doe",
        "grammar_problem_bundle",
        "human_vs_agent_bundle",
        "ideation_bundle",
        "materialize_conditions",
        "optimization_bundle",
        "render_codebook",
        "render_markdown_summary",
        "render_methods_scaffold",
        "render_significance_brief",
        "resume_study",
        "run_study",
        "validate_study",
        "write_markdown_report",
    ]

    analysis = ModuleType("design_research_analysis")
    for symbol in [
        "DecodeResult",
        "DiscreteHMMResult",
        "GaussianHMMResult",
        "MarkovChainResult",
        "UnifiedTableConfig",
        "UnifiedTableValidationReport",
    ]:
        setattr(analysis, symbol, type(symbol, (), {}))
    for symbol in [
        "attach_provenance",
        "bootstrap_ci",
        "capture_run_context",
        "cluster_projection",
        "coerce_unified_table",
        "derive_columns",
        "validate_unified_table",
        "dataset",
        "decode_hmm",
        "dimred",
        "embed_records",
        "estimate_sample_size",
        "profile_dataframe",
        "validate_dataframe",
        "generate_codebook",
        "fit_markov_chain_from_table",
        "fit_discrete_hmm_from_table",
        "compute_language_convergence",
        "compute_semantic_distance_trajectory",
        "reduce_dimensions",
        "compare_groups",
        "fit_regression",
        "fit_mixed_effects",
        "fit_text_gaussian_hmm_from_table",
        "fit_topic_model",
        "is_google_colab",
        "is_notebook",
        "language",
        "minimum_detectable_effect",
        "permutation_test",
        "plot_state_graph",
        "plot_transition_matrix",
        "power_curve",
        "rank_tests_one_stop",
        "runtime",
        "score_sentiment",
        "sequence",
        "stats",
        "write_run_manifest",
    ]:
        setattr(analysis, symbol, _fn(symbol))
    analysis.__all__ = [
        "DecodeResult",
        "DiscreteHMMResult",
        "GaussianHMMResult",
        "MarkovChainResult",
        "UnifiedTableConfig",
        "UnifiedTableValidationReport",
        "attach_provenance",
        "bootstrap_ci",
        "capture_run_context",
        "cluster_projection",
        "coerce_unified_table",
        "compare_groups",
        "compute_language_convergence",
        "compute_semantic_distance_trajectory",
        "dataset",
        "decode_hmm",
        "derive_columns",
        "dimred",
        "embed_records",
        "estimate_sample_size",
        "fit_discrete_hmm_from_table",
        "fit_markov_chain_from_table",
        "fit_mixed_effects",
        "fit_regression",
        "fit_text_gaussian_hmm_from_table",
        "fit_topic_model",
        "generate_codebook",
        "is_google_colab",
        "is_notebook",
        "language",
        "minimum_detectable_effect",
        "permutation_test",
        "plot_state_graph",
        "plot_transition_matrix",
        "power_curve",
        "profile_dataframe",
        "rank_tests_one_stop",
        "reduce_dimensions",
        "runtime",
        "score_sentiment",
        "sequence",
        "stats",
        "validate_dataframe",
        "validate_unified_table",
        "write_run_manifest",
    ]

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
    assert agents.CallableToolConfig.__name__ == "CallableToolConfig"
    assert agents.OpenAICompatibleHTTPLLMClient.__name__ == "OpenAICompatibleHTTPLLMClient"
    assert agents.OpenAIServiceLLMClient.__name__ == "OpenAIServiceLLMClient"
    assert agents.PlanExecutePattern.__name__ == "PlanExecutePattern"
    assert problems.Citation.__name__ == "Citation"
    assert experiments.run_study()[0] == "run_study"
    assert experiments.build_prompt_framing_study()[0] == "build_prompt_framing_study"
    assert experiments.render_significance_brief()[0] == "render_significance_brief"
    assert experiments.RunBudget.__name__ == "RunBudget"
    assert experiments.Study.__name__ == "Study"
    assert analysis.permutation_test()[0] == "permutation_test"
    assert analysis.estimate_sample_size()[0] == "estimate_sample_size"
    assert analysis.validate_unified_table()[0] == "validate_unified_table"
    assert analysis.UnifiedTableConfig.__name__ == "UnifiedTableConfig"

    assert problems.__all__ == stubs["design_research_problems"].__all__
    assert agents.__all__ == stubs["design_research_agents"].__all__
    assert experiments.__all__ == stubs["design_research_experiments"].__all__
    assert analysis.__all__ == stubs["design_research_analysis"].__all__

    assert "permutation_test" in analysis.__all__
    assert "build_prompt_framing_study" in experiments.__all__
    assert "CallableToolConfig" in agents.__all__
    assert "Citation" in problems.__all__
