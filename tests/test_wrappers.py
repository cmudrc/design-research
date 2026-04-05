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
    problems_integration = ModuleType("design_research_problems.integration")
    problems.integration = problems_integration
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
        "integration",
    ]

    agents = ModuleType("design_research_agents")
    for symbol in [
        "__version__",
        "DirectLLMCall",
        "MultiStepAgent",
        "SkillsConfig",
        "SeededRandomBaselineAgent",
        "PromptWorkflowAgent",
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
        "NominalTeamPattern",
        "RouterDelegatePattern",
        "RoundBasedCoordinationPattern",
        "BlackboardPattern",
        "TreeSearchPattern",
        "RAGPattern",
    ]:
        setattr(agents, symbol, type(symbol, (), {}))
    agents_integration = ModuleType("design_research_agents.integration")
    agents.integration = agents_integration
    agents.__all__ = [
        "__version__",
        "DirectLLMCall",
        "MultiStepAgent",
        "SkillsConfig",
        "SeededRandomBaselineAgent",
        "PromptWorkflowAgent",
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
        "NominalTeamPattern",
        "RouterDelegatePattern",
        "RoundBasedCoordinationPattern",
        "BlackboardPattern",
        "TreeSearchPattern",
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
        "integration",
    ]

    experiments = ModuleType("design_research_experiments")
    for symbol in [
        "AgentArchitectureComparisonConfig",
        "OutcomeSpec",
        "AnalysisPlan",
        "BenchmarkBundle",
        "BivariateComparisonConfig",
        "ComparisonStudyConfig",
        "Study",
        "Hypothesis",
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
        "StrategyComparisonConfig",
        "UnivariateComparisonConfig",
    ]:
        setattr(experiments, symbol, type(symbol, (), {}))
    for symbol in [
        "build_agent_architecture_comparison_study",
        "build_bivariate_comparison_study",
        "build_diversity_and_exploration_study",
        "build_grammar_scaffold_study",
        "build_human_vs_agent_process_study",
        "build_optimization_benchmark_study",
        "build_prompt_framing_study",
        "build_strategy_comparison_study",
        "build_univariate_comparison_study",
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
    experiments.resolve_problem = _fn("resolve_problem")
    experiments.run_study = _fn("run_study")
    experiments.resume_study = _fn("resume_study")
    experiments.validate_study = _fn("validate_study")
    experiments.export_analysis_tables = _fn("export_analysis_tables")
    experiments.__all__ = [
        "AgentArchitectureComparisonConfig",
        "AnalysisPlan",
        "BenchmarkBundle",
        "BivariateComparisonConfig",
        "Block",
        "ComparisonStudyConfig",
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
        "StrategyComparisonConfig",
        "Study",
        "UnivariateComparisonConfig",
        "build_agent_architecture_comparison_study",
        "build_bivariate_comparison_study",
        "build_design",
        "build_diversity_and_exploration_study",
        "build_grammar_scaffold_study",
        "build_human_vs_agent_process_study",
        "build_optimization_benchmark_study",
        "build_prompt_framing_study",
        "build_strategy_comparison_study",
        "build_univariate_comparison_study",
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
        "resolve_problem",
        "resume_study",
        "run_study",
        "validate_study",
        "write_markdown_report",
    ]

    analysis = ModuleType("design_research_analysis")
    analysis_dataset = ModuleType("design_research_analysis.dataset")
    analysis_embedding_maps = ModuleType("design_research_analysis.embedding_maps")
    analysis_integration = ModuleType("design_research_analysis.integration")
    analysis_language = ModuleType("design_research_analysis.language")
    analysis_runtime = ModuleType("design_research_analysis.runtime")
    analysis_sequence = ModuleType("design_research_analysis.sequence")
    analysis_stats = ModuleType("design_research_analysis.stats")
    analysis_visualization = ModuleType("design_research_analysis.visualization")
    for symbol in [
        "ComparisonResult",
        "DecodeResult",
        "DiscreteHMMResult",
        "EmbeddingMapResult",
        "EmbeddingResult",
        "GaussianHMMResult",
        "MarkovChainResult",
        "UnifiedTableConfig",
        "UnifiedTableValidationReport",
    ]:
        setattr(analysis, symbol, type(symbol, (), {}))
    analysis.__version__ = "0.1.1"
    analysis.dataset = analysis_dataset
    analysis.embedding_maps = analysis_embedding_maps
    analysis.integration = analysis_integration
    analysis.language = analysis_language
    analysis.runtime = analysis_runtime
    analysis.sequence = analysis_sequence
    analysis.stats = analysis_stats
    analysis.visualization = analysis_visualization
    for symbol in [
        "attach_provenance",
        "bootstrap_ci",
        "build_condition_metric_table",
        "build_embedding_map",
        "capture_run_context",
        "cluster_embedding_map",
        "coerce_unified_table",
        "compare_condition_pairs",
        "compare_embedding_maps",
        "derive_columns",
        "compare_groups",
        "compute_design_space_coverage",
        "compute_divergence_convergence",
        "compute_idea_space_trajectory",
        "compute_language_convergence",
        "compute_semantic_distance_trajectory",
        "decode_hmm",
        "embed_records",
        "estimate_sample_size",
        "fit_discrete_hmm_from_table",
        "fit_markov_chain_from_table",
        "fit_regression",
        "fit_mixed_effects",
        "fit_text_gaussian_hmm_from_table",
        "fit_topic_model",
        "generate_codebook",
        "is_google_colab",
        "is_notebook",
        "minimum_detectable_effect",
        "permutation_test",
        "plot_convergence_curve",
        "plot_design_process_timeline",
        "plot_embedding_map",
        "plot_embedding_map_grid",
        "plot_idea_trajectory",
        "plot_state_graph",
        "plot_transition_matrix",
        "power_curve",
        "profile_dataframe",
        "rank_tests_one_stop",
        "score_sentiment",
        "validate_dataframe",
        "validate_unified_table",
        "write_run_manifest",
    ]:
        setattr(analysis, symbol, _fn(symbol))
    analysis.__all__ = [
        "ComparisonResult",
        "DecodeResult",
        "DiscreteHMMResult",
        "EmbeddingMapResult",
        "EmbeddingResult",
        "GaussianHMMResult",
        "MarkovChainResult",
        "UnifiedTableConfig",
        "UnifiedTableValidationReport",
        "__version__",
        "attach_provenance",
        "bootstrap_ci",
        "build_condition_metric_table",
        "build_embedding_map",
        "capture_run_context",
        "cluster_embedding_map",
        "coerce_unified_table",
        "compare_condition_pairs",
        "compare_embedding_maps",
        "compare_groups",
        "compute_design_space_coverage",
        "compute_divergence_convergence",
        "compute_idea_space_trajectory",
        "compute_language_convergence",
        "compute_semantic_distance_trajectory",
        "dataset",
        "decode_hmm",
        "derive_columns",
        "embed_records",
        "embedding_maps",
        "estimate_sample_size",
        "fit_discrete_hmm_from_table",
        "fit_markov_chain_from_table",
        "fit_mixed_effects",
        "fit_regression",
        "fit_text_gaussian_hmm_from_table",
        "fit_topic_model",
        "generate_codebook",
        "integration",
        "is_google_colab",
        "is_notebook",
        "language",
        "minimum_detectable_effect",
        "permutation_test",
        "plot_convergence_curve",
        "plot_design_process_timeline",
        "plot_embedding_map",
        "plot_embedding_map_grid",
        "plot_idea_trajectory",
        "plot_state_graph",
        "plot_transition_matrix",
        "power_curve",
        "profile_dataframe",
        "rank_tests_one_stop",
        "runtime",
        "score_sentiment",
        "sequence",
        "stats",
        "validate_dataframe",
        "validate_unified_table",
        "visualization",
        "write_run_manifest",
    ]

    stubs = {
        "design_research_problems": problems,
        "design_research_problems.integration": problems_integration,
        "design_research_agents": agents,
        "design_research_agents.integration": agents_integration,
        "design_research_experiments": experiments,
        "design_research_analysis": analysis,
        "design_research_analysis.dataset": analysis_dataset,
        "design_research_analysis.embedding_maps": analysis_embedding_maps,
        "design_research_analysis.integration": analysis_integration,
        "design_research_analysis.language": analysis_language,
        "design_research_analysis.runtime": analysis_runtime,
        "design_research_analysis.sequence": analysis_sequence,
        "design_research_analysis.stats": analysis_stats,
        "design_research_analysis.visualization": analysis_visualization,
    }
    sys.modules.update(stubs)
    return stubs


def test_wrapper_re_exports_are_reachable_via_stubs(monkeypatch: Any) -> None:
    """Resolve representative symbols through each wrapper module."""
    stubs = _install_dependency_stubs()
    for name, module in stubs.items():
        monkeypatch.setitem(sys.modules, name, module)
    for module_name in (
        "design_research.problems",
        "design_research.agents",
        "design_research.experiments",
        "design_research.analysis",
    ):
        sys.modules.pop(module_name, None)

    problems = importlib.import_module("design_research.problems")
    agents = importlib.import_module("design_research.agents")
    experiments = importlib.import_module("design_research.experiments")
    analysis = importlib.import_module("design_research.analysis")

    assert problems.get_problem()[0] == "get_problem"
    assert problems.list_problems()[0] == "list_problems"
    assert problems.integration.__name__ == "design_research_problems.integration"
    assert agents.MultiStepAgent.__name__ == "MultiStepAgent"
    assert agents.integration.__name__ == "design_research_agents.integration"
    assert agents.CompiledExecution.__name__ == "CompiledExecution"
    assert agents.LlamaCppServerLLMClient.__name__ == "LlamaCppServerLLMClient"
    assert agents.ModelStep.__name__ == "ModelStep"
    assert agents.CallableToolConfig.__name__ == "CallableToolConfig"
    assert agents.OpenAICompatibleHTTPLLMClient.__name__ == "OpenAICompatibleHTTPLLMClient"
    assert agents.OpenAIServiceLLMClient.__name__ == "OpenAIServiceLLMClient"
    assert agents.PromptWorkflowAgent.__name__ == "PromptWorkflowAgent"
    assert agents.PlanExecutePattern.__name__ == "PlanExecutePattern"
    assert agents.TreeSearchPattern.__name__ == "TreeSearchPattern"
    assert problems.Citation.__name__ == "Citation"
    assert experiments.resolve_problem()[0] == "resolve_problem"
    assert experiments.run_study()[0] == "run_study"
    assert experiments.build_prompt_framing_study()[0] == "build_prompt_framing_study"
    assert experiments.build_strategy_comparison_study()[0] == "build_strategy_comparison_study"
    assert experiments.render_significance_brief()[0] == "render_significance_brief"
    assert experiments.RunBudget.__name__ == "RunBudget"
    assert experiments.StrategyComparisonConfig.__name__ == "StrategyComparisonConfig"
    assert experiments.Study.__name__ == "Study"
    assert analysis.__version__ == "0.1.1"
    assert analysis.build_condition_metric_table()[0] == "build_condition_metric_table"
    assert analysis.compare_condition_pairs()[0] == "compare_condition_pairs"
    assert analysis.ComparisonResult.__name__ == "ComparisonResult"
    assert analysis.EmbeddingMapResult.__name__ == "EmbeddingMapResult"
    assert analysis.embedding_maps.__name__ == "design_research_analysis.embedding_maps"
    assert analysis.permutation_test()[0] == "permutation_test"
    assert analysis.estimate_sample_size()[0] == "estimate_sample_size"
    assert analysis.integration.__name__ == "design_research_analysis.integration"
    assert analysis.visualization.__name__ == "design_research_analysis.visualization"
    assert analysis.validate_unified_table()[0] == "validate_unified_table"
    assert analysis.UnifiedTableConfig.__name__ == "UnifiedTableConfig"

    assert problems.__all__ == stubs["design_research_problems"].__all__
    assert agents.__all__ == stubs["design_research_agents"].__all__
    assert experiments.__all__ == stubs["design_research_experiments"].__all__
    assert analysis.__all__ == stubs["design_research_analysis"].__all__

    assert "permutation_test" in analysis.__all__
    assert "compare_condition_pairs" in analysis.__all__
    assert "visualization" in analysis.__all__
    assert "build_prompt_framing_study" in experiments.__all__
    assert "build_strategy_comparison_study" in experiments.__all__
    assert "CallableToolConfig" in agents.__all__
    assert "Citation" in problems.__all__
