"""Canonical prompt-strategy comparison walkthrough."""

from __future__ import annotations

import csv
import importlib
import importlib.util
import inspect
import json
import os
import random
from collections.abc import Mapping
from pathlib import Path

from _workspace_bootstrap import bootstrap_sibling_sources

bootstrap_sibling_sources()

dr = importlib.import_module("design_research")

PROBLEM_ID = "decision_laptop_design_profit_maximization"
STUDY_ID = "prompt_strategy_comparison_study"
OUTPUT_DIR = Path("artifacts") / "examples" / STUDY_ID
DEFAULT_REPLICATES_PER_CONDITION = 8
SIGNIFICANCE_ALPHA = 0.05
EXACT_PERMUTATION_THRESHOLD = 250_000
MONTE_CARLO_PERMUTATIONS = 20_000
PERMUTATION_TEST_SEED = 17
SUMMARY_REPORT_NAME = "prompt_strategy_summary.md"
STRATEGY_ORDER = ("random_selection", "neutral_prompt", "profit_focus_prompt")
PAIRWISE_COMPARISONS = (
    ("profit_focus_prompt", "neutral_prompt"),
    ("neutral_prompt", "random_selection"),
    ("profit_focus_prompt", "random_selection"),
)
ARTIFACT_NAMES = (
    "study.yaml",
    "manifest.json",
    "hypotheses.json",
    "analysis_plan.json",
    "conditions.csv",
    "runs.csv",
    "events.csv",
    "evaluations.csv",
)


def main() -> None:
    """Run the prompt-strategy comparison walkthrough as one linear script."""
    _require_april_branch_apis()

    packaged_problem = dr.problems.get_problem(PROBLEM_ID)
    problem_title = str(
        getattr(getattr(packaged_problem, "metadata", object()), "title", PROBLEM_ID)
    )
    problem_brief_markdown = _render_problem_brief(packaged_problem)
    problem_brief = problem_brief_markdown.replace("\n", " ").strip()
    if not problem_brief_markdown:
        problem_summary = "Using the packaged problem statement from design_research.problems."
    elif len(problem_brief) <= 220:
        problem_summary = problem_brief
    else:
        problem_summary = f"{problem_brief[:217].rstrip()}..."

    candidate_schema: dict[str, object] = {
        "type": "object",
        "properties": {},
        "required": [],
        "additionalProperties": False,
    }
    factor_levels_by_key: dict[str, tuple[object, ...]] = {}
    factor_lines: list[str] = []
    for factor in getattr(packaged_problem, "option_factors", ()):
        key = getattr(factor, "key", None)
        levels = tuple(getattr(factor, "levels", ()))
        if key is None or not levels:
            continue
        factor_key = str(key)
        factor_levels_by_key[factor_key] = levels
        factor_lines.append(f"- {factor_key}: {', '.join(str(level) for level in levels)}")
        candidate_schema["properties"][factor_key] = {
            "type": "number",
            "enum": list(levels),
        }
        candidate_schema["required"].append(factor_key)

    factor_keys = tuple(candidate_schema["required"])
    if not factor_keys:
        raise RuntimeError("Expected a packaged decision problem with explicit option factors.")

    configured_replicates = int(
        os.getenv("PROMPT_STUDY_REPLICATES", str(DEFAULT_REPLICATES_PER_CONDITION))
    )
    if configured_replicates < 2:
        raise RuntimeError("PROMPT_STUDY_REPLICATES must be at least 2.")

    missing_runtime = [
        module_name
        for module_name in ("llama_cpp", "fastapi", "uvicorn")
        if importlib.util.find_spec(module_name) is None
    ]
    if missing_runtime:
        raise RuntimeError(
            "Install llama-cpp-python[server] before running the strategy comparison walkthrough "
            "(for example: python -m pip install 'llama-cpp-python[server]'). Missing: "
            + ", ".join(sorted(missing_runtime))
        )

    provider_name = "llama-cpp"
    configured_model_source = (
        os.getenv("LLAMA_CPP_MODEL", "Qwen2.5-1.5B-Instruct-Q4_K_M.gguf").strip()
        or "Qwen2.5-1.5B-Instruct-Q4_K_M.gguf"
    )
    configured_model_name = (
        os.getenv("LLAMA_CPP_API_MODEL", "qwen2-1.5b-q4").strip() or "qwen2-1.5b-q4"
    )
    configured_model_repo = (
        os.getenv("LLAMA_CPP_HF_MODEL_REPO_ID", "bartowski/Qwen2.5-1.5B-Instruct-GGUF").strip()
        or None
    )
    configured_host = os.getenv("LLAMA_CPP_HOST", "127.0.0.1").strip() or "127.0.0.1"
    configured_port = int(os.getenv("LLAMA_CPP_PORT", "8001"))
    configured_context_window = int(os.getenv("LLAMA_CPP_CONTEXT_WINDOW", "4096"))
    needs_model_download = (
        configured_model_repo is not None
        and not Path(configured_model_source).expanduser().exists()
    )
    if needs_model_download and importlib.util.find_spec("huggingface_hub") is None:
        raise RuntimeError(
            "Install huggingface-hub or point LLAMA_CPP_MODEL at a local GGUF file before "
            "running the walkthrough."
        )

    base_prompt = "\n".join(
        [
            "You are solving a packaged design-research decision problem.",
            "Read the problem statement and return exactly one JSON object candidate.",
            "Choose one allowed value for each factor key.",
            "",
            f"Problem title: {problem_title}",
            "Problem brief:",
            problem_brief_markdown,
            "",
            "Allowed factor values:",
            *factor_lines,
        ]
    )

    def evaluate_candidate(
        candidate: Mapping[str, object],
    ) -> tuple[list[dict[str, object]], dict[str, float]]:
        """Evaluate a candidate through the packaged problem and normalize rows."""
        evaluation = packaged_problem.evaluate(dict(candidate))
        objective_metric = str(getattr(evaluation, "objective_metric", "market_share_proxy"))
        objective_value = float(getattr(evaluation, "objective_value", 0.0) or 0.0)
        predicted_share = float(getattr(evaluation, "predicted_share", objective_value) or 0.0)
        expected_demand_units = float(getattr(evaluation, "expected_demand_units", 0.0) or 0.0)
        utility = float(getattr(evaluation, "utility", 0.0) or 0.0)
        candidate_label = str(getattr(evaluation, "candidate_label", ""))
        higher_is_better = bool(getattr(evaluation, "higher_is_better", True))

        evaluation_rows = [
            {
                "evaluator_id": "packaged_problem_evaluator",
                "metric_name": objective_metric,
                "metric_value": objective_value,
                "metric_unit": "unitless",
                "aggregation_level": "run",
                "notes_json": {
                    "candidate_label": candidate_label,
                    "higher_is_better": higher_is_better,
                },
            },
            {
                "evaluator_id": "packaged_problem_evaluator",
                "metric_name": "expected_demand_units",
                "metric_value": expected_demand_units,
                "metric_unit": "units",
                "aggregation_level": "run",
                "notes_json": {"candidate_label": candidate_label},
            },
            {
                "evaluator_id": "packaged_problem_evaluator",
                "metric_name": "utility",
                "metric_value": utility,
                "metric_unit": "unitless",
                "aggregation_level": "run",
                "notes_json": {"candidate_label": candidate_label},
            },
        ]
        summary = {
            "market_share_proxy": objective_value,
            objective_metric: objective_value,
            "predicted_share": predicted_share,
            "expected_demand_units": expected_demand_units,
            "utility": utility,
        }
        return evaluation_rows, summary

    def packaged_problem_packet() -> object:
        """Wrap the packaged problem in the experiments adapter shape."""

        def evaluator(output: Mapping[str, object]) -> list[dict[str, object]]:
            candidate = {factor_key: output[factor_key] for factor_key in factor_keys}
            rows, _ = evaluate_candidate(candidate)
            return rows

        return dr.experiments.ProblemPacket(
            problem_id=PROBLEM_ID,
            family=str(getattr(packaged_problem, "family", "optimization")),
            brief=problem_brief_markdown or problem_title,
            payload={"problem_object": packaged_problem, "problem_title": problem_title},
            metadata={"problem_title": problem_title},
            evaluator=evaluator,
        )

    strategy_factor = dr.experiments.Factor(
        name="agent_id",
        description="Candidate-selection strategy under comparison.",
        kind=dr.experiments.FactorKind.MANIPULATED,
        levels=(
            dr.experiments.Level(
                name="random_selection",
                value="random_selection",
                label="Random selection baseline",
                metadata={"role": "baseline", "is_baseline": True},
            ),
            dr.experiments.Level(
                name="neutral_prompt",
                value="neutral_prompt",
                label="Neutral prompt",
                metadata={"role": "treatment", "is_baseline": False},
            ),
            dr.experiments.Level(
                name="profit_focus_prompt",
                value="profit_focus_prompt",
                label="Profit-focused prompt",
                metadata={"role": "treatment", "is_baseline": False},
            ),
        ),
        metadata={"comparison_axis": True},
    )
    analysis_plan = dr.experiments.AnalysisPlan(
        analysis_plan_id="ap1",
        hypothesis_ids=("h1",),
        tests=("difference_in_means", "exact_permutation_test", "sampled_permutation_test"),
        outcomes=("primary_outcome",),
        plots=("condition_means", "replicate_distribution"),
        export_tables=("summary_by_condition", "pairwise_condition_comparisons"),
        multiple_comparison_policy="holm",
        notes=(
            "Use ordered one-sided condition-pair permutation tests on the primary outcome after "
            "export, staying exact for smaller comparisons and falling back to deterministic "
            "Monte Carlo sampling when the permutation count gets large."
        ),
    )
    study = dr.experiments.build_strategy_comparison_study(
        dr.experiments.StrategyComparisonConfig(
            study_id=STUDY_ID,
            title="Prompt Strategy Comparison Study",
            description=(
                "Compare a random baseline, a neutral prompt, and a profit-focused prompt on a "
                "packaged laptop-design decision task."
            ),
            rationale=(
                "Align the umbrella walkthrough with the new comparison-study recipe surfaces "
                "landing across the April release branches."
            ),
            tags=("walkthrough", "comparison", "strategy", "llama-cpp"),
            comparison_factor=strategy_factor,
            analysis_plans=(analysis_plan,),
            run_budget=dr.experiments.RunBudget(replicates=configured_replicates, parallelism=1),
            seed_policy=dr.experiments.SeedPolicy(base_seed=31),
            output_dir=OUTPUT_DIR,
            notes=(
                "Requires the April 2026 recipe/reporting APIs from design-research-experiments "
                "and the condition-comparison helpers from design-research-analysis."
            ),
            problem_ids=(PROBLEM_ID,),
        )
    )

    validation_errors = dr.experiments.validate_study(study)
    if validation_errors:
        raise RuntimeError("Study validation failed:\n- " + "\n- ".join(validation_errors))

    conditions = dr.experiments.build_design(study)
    problem_registry = {PROBLEM_ID: packaged_problem_packet()}

    with dr.agents.LlamaCppServerLLMClient(
        model=configured_model_source,
        hf_model_repo_id=configured_model_repo,
        api_model=configured_model_name,
        host=configured_host,
        port=configured_port,
        context_window=configured_context_window,
    ) as llm_client:

        def build_request(context: dict[str, object]) -> object:
            """Build one structured model request for the workflow step."""
            prompt = str(context.get("prompt", "")).strip()
            if not prompt:
                raise RuntimeError("Expected a non-empty walkthrough prompt.")
            return dr.agents.LLMRequest(
                messages=[
                    dr.agents.LLMMessage(
                        role="system",
                        content=(
                            "You are a careful study participant. Respond with valid JSON only "
                            "and match the requested schema exactly."
                        ),
                    ),
                    dr.agents.LLMMessage(role="user", content=prompt),
                ],
                temperature=0.0,
                max_tokens=400,
                response_schema=candidate_schema,
                metadata={"study_id": STUDY_ID, "problem_id": PROBLEM_ID},
            )

        def parse_response(response: object, context: dict[str, object]) -> dict[str, object]:
            """Parse the workflow model response into the final candidate payload."""
            del context
            response_text = str(getattr(response, "text", "")).strip()
            if response_text.startswith("```"):
                response_lines = response_text.splitlines()
                if response_lines and response_lines[0].startswith("```"):
                    response_lines = response_lines[1:]
                if response_lines and response_lines[-1].startswith("```"):
                    response_lines = response_lines[:-1]
                response_text = "\n".join(response_lines).strip()
            candidate = json.loads(response_text)
            if not isinstance(candidate, dict):
                raise RuntimeError("Expected the model to return a JSON object candidate.")
            return {"final_output": candidate, "model_text": str(getattr(response, "text", ""))}

        agent_workflow = dr.agents.Workflow(
            steps=(
                dr.agents.ModelStep(
                    step_id="select_candidate",
                    llm_client=llm_client,
                    request_builder=build_request,
                    response_parser=parse_response,
                ),
            ),
            output_schema=candidate_schema,
            default_request_id_prefix=STUDY_ID,
        )

        def strategy_runner_factory(strategy_id: str):
            """Build one strategy-specific executable agent."""
            if strategy_id == "profit_focus_prompt":
                strategy_instruction = (
                    "Condition: profit-focus prompt. Prioritize design choices that are likely "
                    "to increase market_share_proxy and expected_demand_units."
                )
            elif strategy_id == "neutral_prompt":
                strategy_instruction = (
                    "Condition: neutral prompt. Select the best overall design candidate using "
                    "the packaged demand and feasibility information."
                )
            else:
                strategy_instruction = (
                    "Condition: random selection baseline. Ignore the language model and sample "
                    "one admissible value per factor uniformly at random using the run seed."
                )

            def run(
                *,
                problem_packet: object,
                run_spec: object,
                condition: object,
            ) -> dict[str, object]:
                """Execute one strategy arm and adapt it to the experiments runner."""
                del problem_packet
                del condition
                metrics: dict[str, object] = {"cost_usd": 0.0}
                trace_refs: list[str] = []
                if strategy_id == "random_selection":
                    random_seed = int(getattr(run_spec, "seed", 0) or 0)
                    rng = random.Random(random_seed)
                    candidate = {
                        factor_key: rng.choice(levels)
                        for factor_key, levels in factor_levels_by_key.items()
                    }
                    resolved_provider = "baseline"
                    resolved_model = "random-selection"
                    model_text = json.dumps(candidate, sort_keys=True)
                else:
                    strategy_prompt = "\n".join(
                        [
                            base_prompt,
                            "",
                            strategy_instruction,
                            "Return JSON only with no markdown fences and no extra commentary.",
                        ]
                    )
                    request_id = str(getattr(run_spec, "run_id", STUDY_ID))
                    execution = agent_workflow.run(
                        strategy_prompt,
                        request_id=request_id,
                    )
                    if not execution.success:
                        raise RuntimeError(f"Live workflow failed: {execution.error}")

                    candidate = execution.output_dict("final_output")
                    if not candidate:
                        raise RuntimeError(
                            "Workflow completed without a structured candidate output."
                        )

                    model_response = execution.model_response
                    usage = getattr(model_response, "usage", None)
                    prompt_tokens = None
                    completion_tokens = None
                    if isinstance(usage, dict):
                        prompt_tokens = usage.get("prompt_tokens")
                        completion_tokens = usage.get("completion_tokens")
                    elif usage is not None:
                        prompt_tokens = getattr(usage, "prompt_tokens", None)
                        completion_tokens = getattr(usage, "completion_tokens", None)
                    if isinstance(prompt_tokens, int):
                        metrics["input_tokens"] = prompt_tokens
                    if isinstance(completion_tokens, int):
                        metrics["output_tokens"] = completion_tokens

                    resolved_provider = str(
                        getattr(model_response, "provider", "") or provider_name
                    )
                    resolved_model = str(
                        getattr(model_response, "model", "") or configured_model_name
                    )
                    model_text = str(execution.output_value("model_text", "") or "").strip()
                    trace_path = execution.metadata.get("trace_path")
                    if isinstance(trace_path, str) and trace_path.strip():
                        trace_refs.append(trace_path)

                _, evaluation_summary = evaluate_candidate(candidate)
                return {
                    "output": candidate,
                    "metrics": metrics,
                    "events": [
                        {
                            "text": f"Selected packaged problem: {problem_title}",
                            "event_type": "problem_selected",
                            "actor_id": "system",
                        },
                        {
                            "text": f"Brief excerpt: {problem_summary}",
                            "event_type": "problem_summary",
                            "actor_id": "system",
                        },
                        {
                            "text": f"Assigned comparison arm: agent_id={strategy_id}",
                            "event_type": "condition_assigned",
                            "actor_id": "system",
                            "meta_json": {"agent_id": strategy_id},
                        },
                        {
                            "text": strategy_instruction,
                            "event_type": "condition_instruction",
                            "actor_id": "system",
                            "meta_json": {
                                "provider": resolved_provider,
                                "model_name": resolved_model,
                            },
                        },
                        {
                            "text": f"Requested candidate over factors: {', '.join(factor_keys)}",
                            "event_type": (
                                "random_request"
                                if strategy_id == "random_selection"
                                else "model_request"
                            ),
                            "actor_id": "system",
                            "meta_json": {
                                "provider": resolved_provider,
                                "model_name": resolved_model,
                            },
                        },
                        {
                            "text": model_text or json.dumps(candidate, sort_keys=True),
                            "event_type": (
                                "random_response"
                                if strategy_id == "random_selection"
                                else "model_response"
                            ),
                            "actor_id": "agent",
                            "meta_json": {
                                "provider": resolved_provider,
                                "model_name": resolved_model,
                            },
                        },
                        {
                            "text": f"Candidate selected: {candidate}",
                            "event_type": "candidate_selected",
                            "actor_id": "agent",
                        },
                        {
                            "text": (
                                "Preview metrics: "
                                "market_share_proxy="
                                f"{evaluation_summary['market_share_proxy']:.4f}, "
                                "expected_demand_units="
                                f"{evaluation_summary['expected_demand_units']:.0f}, "
                                f"utility={evaluation_summary['utility']:.4f}"
                            ),
                            "event_type": "candidate_evaluated",
                            "actor_id": "system",
                            "meta_json": evaluation_summary,
                        },
                    ],
                    "trace_refs": trace_refs,
                    "metadata": {
                        "model_name": resolved_model,
                        "provider": resolved_provider,
                    },
                }

            return run

        agent_factories = {
            strategy_id: (
                lambda _condition, strategy_id=strategy_id: strategy_runner_factory(strategy_id)
            )
            for strategy_id in STRATEGY_ORDER
        }
        results = dr.experiments.run_study(
            study,
            conditions=conditions,
            agent_factories=agent_factories,
            problem_registry=problem_registry,
            checkpoint=False,
        )

    artifact_paths = dr.experiments.export_analysis_tables(
        study,
        conditions=conditions,
        run_results=results,
        output_dir=OUTPUT_DIR,
    )

    with artifact_paths["events.csv"].open(encoding="utf-8", newline="") as handle:
        event_rows = list(csv.DictReader(handle))
    with artifact_paths["runs.csv"].open(encoding="utf-8", newline="") as handle:
        run_rows = list(csv.DictReader(handle))
    with artifact_paths["conditions.csv"].open(encoding="utf-8", newline="") as handle:
        condition_rows = list(csv.DictReader(handle))
    with artifact_paths["evaluations.csv"].open(encoding="utf-8", newline="") as handle:
        evaluation_rows = list(csv.DictReader(handle))

    validation_report = dr.analysis.validate_unified_table(event_rows)
    if validation_report.errors:
        raise RuntimeError(
            "Unified event table validation failed:\n- " + "\n- ".join(validation_report.errors)
        )

    primary_metric_rows = dr.analysis.build_condition_metric_table(
        run_rows,
        metric="market_share_proxy",
        condition_column="agent_id",
        evaluations=evaluation_rows,
    )
    demand_metric_rows = dr.analysis.build_condition_metric_table(
        run_rows,
        metric="expected_demand_units",
        condition_column="agent_id",
        evaluations=evaluation_rows,
    )
    comparison_report = dr.analysis.compare_condition_pairs(
        primary_metric_rows,
        condition_pairs=PAIRWISE_COMPARISONS,
        alternative="greater",
        alpha=SIGNIFICANCE_ALPHA,
        exact_threshold=EXACT_PERMUTATION_THRESHOLD,
        n_permutations=MONTE_CARLO_PERMUTATIONS,
        seed=PERMUTATION_TEST_SEED,
    )
    significance_rows = comparison_report.to_significance_rows()

    condition_means = _condition_means(primary_metric_rows)
    demand_means = _condition_means(demand_metric_rows)

    summary_markdown = dr.experiments.render_markdown_summary(study, results)
    methods_markdown = dr.experiments.render_methods_scaffold(study)
    codebook_markdown = dr.experiments.render_codebook(study, conditions)
    comparison_markdown = comparison_report.render_brief()
    significance_markdown = dr.experiments.render_significance_brief(significance_rows)
    summary_report_path = dr.experiments.write_markdown_report(
        study.output_dir,
        SUMMARY_REPORT_NAME,
        "\n\n".join(
            [
                summary_markdown,
                methods_markdown,
                codebook_markdown,
                comparison_markdown,
                significance_markdown,
            ]
        ),
    )

    successful_results = [result for result in results if str(result.status).lower() == "success"]
    if not successful_results:
        raise RuntimeError("Study completed without any successful runs.")

    print(f"Problem: {PROBLEM_ID}")
    print(f"Study: {study.study_id}")
    print(f"Live provider: {provider_name}")
    print(f"Live model API name: {configured_model_name}")
    print(f"Model source: {configured_model_source}")
    print(f"Replicates per condition: {configured_replicates}")
    print(f"Hypotheses: {len(study.hypotheses)}")
    print(f"Conditions: {len(conditions)}")
    print(f"Runs: {len(results)}")
    print("Condition means:")
    for strategy_name in STRATEGY_ORDER:
        print(
            f"  - agent_id={strategy_name}: "
            f"mean_market_share_proxy={condition_means.get(strategy_name, 0.0):.4f}, "
            f"mean_expected_demand_units={demand_means.get(strategy_name, 0.0):.0f}"
        )
    print(comparison_markdown)
    print(significance_markdown)
    print(f"Summary report: {summary_report_path}")
    print("Artifacts:")
    for artifact_name in ARTIFACT_NAMES:
        print(f"  - {artifact_name}: {artifact_paths[artifact_name]}")
    print(f"Event rows: {len(event_rows)}")
    print(f"Validation warnings: {len(validation_report.warnings)}")
    print(f"Condition rows: {len(condition_rows)}")


def _condition_means(rows: list[dict[str, object]]) -> dict[str, float]:
    """Compute one mean per condition label from normalized rows."""
    grouped: dict[str, list[float]] = {}
    for row in rows:
        condition = str(row["condition"])
        grouped.setdefault(condition, []).append(float(row["value"]))
    return {
        condition: (sum(values) / len(values) if values else 0.0)
        for condition, values in grouped.items()
    }


def _render_problem_brief(problem: object) -> str:
    """Prefer the packaged reusable brief, falling back to the raw statement."""
    render_brief = getattr(problem, "render_brief", None)
    if callable(render_brief):
        try:
            brief_markdown = str(render_brief(include_citation=False)).strip()
        except TypeError:
            brief_markdown = str(render_brief()).strip()
        if brief_markdown:
            return brief_markdown
    return str(getattr(problem, "statement_markdown", "")).strip()


def _require_april_branch_apis() -> None:
    """Fail fast when the local environment still points at pre-April releases."""
    required_apis = {
        "design_research.experiments": (
            dr.experiments,
            (
                "AnalysisPlan",
                "FactorKind",
                "ProblemPacket",
                "StrategyComparisonConfig",
                "build_strategy_comparison_study",
                "render_codebook",
                "render_markdown_summary",
                "render_methods_scaffold",
                "render_significance_brief",
                "write_markdown_report",
            ),
        ),
        "design_research.analysis": (
            dr.analysis,
            (
                "build_condition_metric_table",
                "compare_condition_pairs",
            ),
        ),
    }
    missing: list[str] = []
    for namespace, (module, names) in required_apis.items():
        for name in names:
            if not hasattr(module, name):
                missing.append(f"{namespace}.{name}")
    workflow_init_params = inspect.signature(dr.agents.Workflow).parameters
    if "prompt_context_key" not in workflow_init_params:
        missing.append("design_research.agents.Workflow(prompt_mode)")
    if missing:
        raise RuntimeError(
            "This walkthrough tracks the April 2026 sibling-library branches. Install "
            "design-research-agents, design-research-experiments, and "
            "design-research-analysis from those branches, or wait for the matching release "
            "versions, before running it. Missing APIs: " + ", ".join(missing)
        )


if __name__ == "__main__":
    main()
