"""Canonical live strategy-comparison walkthrough for the umbrella package."""

from __future__ import annotations

import importlib.util
import os
from collections.abc import Sequence
from pathlib import Path

import design_research as dr

# These constants keep the live walkthrough readable: one packaged problem, one
# study id, stable artifact paths, and the statistical settings used in the
# pairwise comparisons later on.
BASELINE_AGENT_ID = "SeededRandomBaselineAgent"
PROBLEM_ID = "decision_laptop_design_profit_maximization"
STUDY_ID = "prompt_strategy_comparison_study"
OUTPUT_DIR = Path("artifacts") / "examples" / STUDY_ID
SUMMARY_REPORT_NAME = "prompt_strategy_summary.md"
DEFAULT_REPLICATES_PER_CONDITION = 50
SIGNIFICANCE_ALPHA = 0.05
EXACT_PERMUTATION_THRESHOLD = 250_000
MONTE_CARLO_PERMUTATIONS = 20_000
PERMUTATION_TEST_SEED = 17
STRATEGY_ORDER = (BASELINE_AGENT_ID, "neutral_prompt", "profit_focus_prompt")
MODEL_BACKED_STRATEGY_IDS = ("neutral_prompt", "profit_focus_prompt")
PRIMARY_METRIC = "predicted_share"
SECONDARY_METRIC = "expected_demand_units"
PAIRWISE_COMPARISONS = (
    ("profit_focus_prompt", "neutral_prompt"),
    ("neutral_prompt", BASELINE_AGENT_ID),
    ("profit_focus_prompt", BASELINE_AGENT_ID),
)


def main() -> None:
    """Run the live strategy-comparison walkthrough with managed llama.cpp."""
    # Read runtime settings from the environment and apply the example's default
    # replicate count when the user does not override it.
    runtime = llama_cpp_runtime_config(default_replicates=DEFAULT_REPLICATES_PER_CONDITION)

    # Load the packaged decision problem and derive the JSON candidate schema the
    # model-based agents should emit.
    packaged_problem = dr.problems.get_problem(PROBLEM_ID)
    candidate_schema = decision_candidate_schema(packaged_problem)

    # Build the recipe-defined study and then materialize its conditions. The
    # conditions encode one row per strategy/replicate combination.
    study = _build_study(replicates=int(runtime["replicates"]))
    conditions = dr.experiments.build_design(study)

    # Start a managed llama.cpp server client for the duration of the study.
    # The context manager handles startup/shutdown around the live run.
    with dr.agents.LlamaCppServerLLMClient(
        model=str(runtime["model_source"]),
        hf_model_repo_id=runtime["model_repo"],
        api_model=str(runtime["model_name"]),
        host=str(runtime["host"]),
        port=int(runtime["port"]),
        context_window=int(runtime["context_window"]),
        startup_timeout_seconds=float(runtime["startup_timeout_seconds"]),
        request_timeout_seconds=float(runtime["request_timeout_seconds"]),
    ) as llm_client:
        # Each `agent_id` in the strategy bundle maps either to a public agent
        # id resolved directly by experiments or to one explicit binding that
        # returns a prompt-driven workflow agent.
        agent_bindings = {
            # The neutral condition uses the live model but keeps the instruction
            # framing generic.
            "neutral_prompt": _prompt_agent_binding(
                llm_client=llm_client,
                candidate_schema=candidate_schema,
                runtime=runtime,
                instruction=(
                    "Condition: neutral prompt. Choose the best overall candidate using the "
                    "packaged demand and feasibility information."
                ),
            ),
            # The profit-focused condition swaps only the framing instruction so
            # the study isolates prompt strategy rather than model identity.
            "profit_focus_prompt": _prompt_agent_binding(
                llm_client=llm_client,
                candidate_schema=candidate_schema,
                runtime=runtime,
                instruction=(
                    "Condition: profit-focus prompt. Prioritize choices that maximize "
                    "market share proxy and expected demand."
                ),
            ),
        }

        # Execute the full study while the managed llama.cpp client is running.
        results = dr.experiments.run_study(
            study,
            conditions=conditions,
            agent_bindings=agent_bindings,
            checkpoint=False,
            show_progress=False,
        )

    # Treat this as a live-runtime check, not merely a deterministic-baseline
    # check: every model-backed prompt strategy must produce usable evidence.
    successful_results = _require_successful_model_strategies(results)

    # Export the standard analysis tables so the next steps can work from the
    # same artifacts users would inspect after their own runs.
    artifact_paths = dr.experiments.export_analysis_tables(
        study,
        conditions=conditions,
        run_results=results,
        output_dir=OUTPUT_DIR,
    )

    # Confirm that the event-level export is structurally valid before building
    # downstream tables from it.
    validation_report = dr.analysis.validate_experiment_events(artifact_paths["events.csv"])

    # Build one condition-by-metric table for the primary outcome we care about
    # and another for a secondary business-facing metric, without hand-loading CSVs.
    primary_metric_rows = dr.analysis.build_condition_metric_table_from_artifacts(
        artifact_paths["events.csv"],
        metric=PRIMARY_METRIC,
        condition_column="agent_id",
    )
    demand_metric_rows = dr.analysis.build_condition_metric_table_from_artifacts(
        artifact_paths["events.csv"],
        metric=SECONDARY_METRIC,
        condition_column="agent_id",
    )

    # Compare the strategy pairs using the analysis package's pairwise
    # permutation test helper.
    comparison_report = dr.analysis.compare_condition_pairs_from_artifacts(
        artifact_paths["events.csv"],
        metric=PRIMARY_METRIC,
        condition_column="agent_id",
        condition_pairs=PAIRWISE_COMPARISONS,
        alternative="greater",
        alpha=SIGNIFICANCE_ALPHA,
        exact_threshold=EXACT_PERMUTATION_THRESHOLD,
        n_permutations=MONTE_CARLO_PERMUTATIONS,
        seed=PERMUTATION_TEST_SEED,
    )

    # Convert the statistical report into rows that the experiments reporting
    # helpers can render alongside the study summary.
    significance_rows = comparison_report.to_significance_rows()

    # Write one consolidated markdown report that includes the study summary,
    # methods scaffold, variable codebook, and the pairwise comparison brief.
    summary_path = dr.experiments.write_markdown_report(
        study.output_dir,
        SUMMARY_REPORT_NAME,
        "\n\n".join(
            [
                dr.experiments.render_markdown_summary(study, results),
                dr.experiments.render_methods_scaffold(study),
                dr.experiments.render_codebook(study, conditions),
                comparison_report.render_brief(),
                dr.experiments.render_significance_brief(significance_rows),
            ]
        ),
    )

    # Collapse the metric tables to per-strategy means for a concise console
    # summary after the run finishes.
    primary_means = condition_means(primary_metric_rows)
    demand_means = condition_means(demand_metric_rows)

    # Fail loudly if the exported live data is not structurally usable.
    if validation_report.errors:
        raise RuntimeError(
            "Unified event table validation failed:\n- " + "\n- ".join(validation_report.errors)
        )

    # Print a guided end-of-run summary so the console output doubles as a quick
    # tour of the artifacts and the headline comparison result.
    print("Problem:", PROBLEM_ID)
    print("Study:", study.study_id)
    print("Live provider:", runtime["provider_name"])
    print("Live model API name:", runtime["model_name"])
    print("Model source:", runtime["model_source"])
    print("Replicates per condition:", runtime["replicates"])
    print("Conditions:", len(conditions))
    print("Runs:", len(results), f"({len(successful_results)} success)")
    print("Condition means:")
    for strategy_name in STRATEGY_ORDER:
        print(
            f"  - agent_id={strategy_name}: "
            f"mean_{PRIMARY_METRIC}={primary_means.get(strategy_name, 0.0):.4f}, "
            f"mean_{SECONDARY_METRIC}={demand_means.get(strategy_name, 0.0):.0f}"
        )
    print(comparison_report.render_brief())
    print(dr.experiments.render_significance_brief(significance_rows))
    print("Event rows valid:", validation_report.is_valid, f"(rows={validation_report.n_rows})")
    print("Summary report:", summary_path)
    print("Artifacts:", artifact_names(artifact_paths))


def _build_study(*, replicates: int) -> object:
    """Build the live strategy-comparison recipe study."""
    # The recipe builder captures the study in one config object. The bundle says
    # which packaged problems and agent strategies participate; the run budget
    # says how many replicates to execute.
    return dr.experiments.build_strategy_comparison_study(
        dr.experiments.StrategyComparisonConfig(
            study_id=STUDY_ID,
            title="Prompt Strategy Comparison Study",
            description=(
                "Compare a seeded random baseline, a neutral prompt, and a profit-focused "
                "prompt on a packaged laptop-design decision problem."
            ),
            bundle=dr.experiments.BenchmarkBundle(
                bundle_id="live-strategy-comparison",
                name="Live Strategy Comparison Bundle",
                description="Packaged decision problem with three strategy bindings.",
                problem_ids=(PROBLEM_ID,),
                agent_specs=STRATEGY_ORDER,
            ),
            run_budget=dr.experiments.RunBudget(replicates=replicates, parallelism=1),
            output_dir=OUTPUT_DIR,
        )
    )


def _strategy_prompt(problem_packet: object, *, instruction: str) -> str:
    """Render one complete strategy prompt from the normalized problem packet."""
    # Compose the final prompt from a few readable pieces instead of one giant
    # literal string. That makes it easy to see which lines stay fixed across
    # conditions and which line changes with the strategy framing.
    return "\n".join(
        [
            "You are solving a packaged design-research decision problem.",
            "Read the problem brief and return exactly one JSON object candidate.",
            instruction,
            "",
            str(getattr(problem_packet, "brief", "")).strip(),
            "",
            "Return JSON only with no markdown fences and no extra commentary.",
        ]
    )


def artifact_names(artifact_paths: dict[str, Path]) -> str:
    """Return exported artifact filenames in stable sorted order."""
    return ", ".join(sorted(path.name for path in artifact_paths.values()))


def condition_means(rows: list[dict[str, object]]) -> dict[str, float]:
    """Compute one mean per condition label from normalized rows."""
    grouped: dict[str, list[float]] = {}
    for row in rows:
        grouped.setdefault(str(row["condition"]), []).append(float(row["value"]))
    return {
        condition: (sum(values) / len(values) if values else 0.0)
        for condition, values in grouped.items()
    }


def _require_successful_model_strategies(results: Sequence[object]) -> list[object]:
    """Require observed successes from every model-backed prompt strategy."""
    successful_results: list[object] = []
    successful_strategy_ids: set[str] = set()
    model_attempts: dict[str, list[str]] = {
        strategy_id: [] for strategy_id in MODEL_BACKED_STRATEGY_IDS
    }
    for result in results:
        raw_status = getattr(result, "status", None)
        status = getattr(raw_status, "value", raw_status)
        run_spec = getattr(result, "run_spec", None)
        strategy_ref = getattr(run_spec, "agent_spec_ref", None)
        strategy_id = str(strategy_ref) if strategy_ref is not None else None
        if strategy_id in model_attempts:
            error_info = getattr(result, "error_info", None)
            detail = str(error_info).strip() if error_info else str(status)
            if detail not in model_attempts[strategy_id]:
                model_attempts[strategy_id].append(detail)
        if status != "success":
            continue
        successful_results.append(result)
        if strategy_id is not None:
            successful_strategy_ids.add(strategy_id)

    missing_strategy_ids = [
        strategy_id
        for strategy_id in MODEL_BACKED_STRATEGY_IDS
        if strategy_id not in successful_strategy_ids
    ]
    if missing_strategy_ids:
        attempt_summary = "; ".join(
            f"{strategy_id}: {', '.join(model_attempts[strategy_id]) or 'no result'}"
            for strategy_id in missing_strategy_ids
        )
        raise RuntimeError(
            "The live walkthrough requires at least one successful result from each "
            "model-backed prompt strategy. Missing successful strategies: "
            + ", ".join(missing_strategy_ids)
            + ". Observed attempts: "
            + attempt_summary
        )
    return successful_results


def decision_candidate_schema(problem: object) -> dict[str, object]:
    """Build a JSON schema for discrete decision-factor candidates."""
    properties: dict[str, object] = {}
    required: list[str] = []
    for factor in getattr(problem, "option_factors", ()):
        levels = tuple(getattr(factor, "levels", ()))
        key = str(getattr(factor, "key", ""))
        if not key or not levels:
            continue
        properties[key] = {"type": "number", "enum": list(levels)}
        required.append(key)

    if not required:
        raise RuntimeError("Expected a packaged decision problem with explicit option factors.")

    return {
        "type": "object",
        "properties": properties,
        "required": required,
        "additionalProperties": False,
    }


def llama_cpp_runtime_config(*, default_replicates: int) -> dict[str, object]:
    """Resolve runtime configuration and fail fast on missing live dependencies."""
    missing_runtime = [
        module_name
        for module_name in ("llama_cpp", "fastapi", "uvicorn")
        if importlib.util.find_spec(module_name) is None
    ]
    if missing_runtime:
        raise RuntimeError(
            "Install the owning Agents extra before running the live walkthrough: "
            'python -m pip install "design-research-agents[llama_cpp]==0.7.0". Missing: '
            + ", ".join(sorted(missing_runtime))
        )

    model_source = (
        os.getenv("LLAMA_CPP_MODEL", "Qwen2.5-1.5B-Instruct-Q4_K_M.gguf").strip()
        or "Qwen2.5-1.5B-Instruct-Q4_K_M.gguf"
    )
    model_repo = (
        os.getenv("LLAMA_CPP_HF_MODEL_REPO_ID", "bartowski/Qwen2.5-1.5B-Instruct-GGUF").strip()
        or None
    )
    if (
        model_repo
        and not Path(model_source).expanduser().exists()
        and importlib.util.find_spec("huggingface_hub") is None
    ):
        raise RuntimeError(
            "Install the owning Agents extra with "
            'python -m pip install "design-research-agents[llama_cpp]==0.7.0" or point '
            "LLAMA_CPP_MODEL at a local GGUF file before running the live walkthrough."
        )

    replicates = int(os.getenv("PROMPT_STUDY_REPLICATES", str(default_replicates)))
    if replicates < 2:
        raise RuntimeError("PROMPT_STUDY_REPLICATES must be at least 2.")

    return {
        "provider_name": "llama-cpp",
        "model_source": model_source,
        "model_name": os.getenv("LLAMA_CPP_API_MODEL", "qwen2-1.5b-q4").strip() or "qwen2-1.5b-q4",
        "model_repo": model_repo,
        "host": os.getenv("LLAMA_CPP_HOST", "127.0.0.1").strip() or "127.0.0.1",
        "port": int(os.getenv("LLAMA_CPP_PORT", "8001")),
        "context_window": int(os.getenv("LLAMA_CPP_CONTEXT_WINDOW", "4096")),
        # The first startup may include a roughly 1 GB model download. Keep the
        # wait finite but long enough for an ordinary laptop connection.
        "startup_timeout_seconds": float(os.getenv("LLAMA_CPP_STARTUP_TIMEOUT_SECONDS", "300")),
        "request_timeout_seconds": float(os.getenv("LLAMA_CPP_REQUEST_TIMEOUT_SECONDS", "120")),
        "replicates": replicates,
    }


def _prompt_agent_binding(
    *,
    llm_client: object,
    candidate_schema: dict[str, object],
    runtime: dict[str, object],
    instruction: str,
) -> object:
    """Build one condition-scoped prompt workflow agent binding."""

    def _binding(_condition: object) -> object:
        """Return one prompt workflow agent for a concrete experiment condition."""
        return dr.agents.PromptWorkflowAgent(
            workflow=dr.agents.build_json_prompt_workflow(
                llm_client=llm_client,
                response_schema=candidate_schema,
                request_metadata={"study_id": STUDY_ID, "problem_id": PROBLEM_ID},
                default_request_id_prefix=STUDY_ID,
                fallback_model_name=str(runtime["model_name"]),
                fallback_provider=str(runtime["provider_name"]),
            ),
            prompt_builder=lambda problem_packet, _run_spec, _condition: _strategy_prompt(
                problem_packet,
                instruction=instruction,
            ),
        )

    return _binding


if __name__ == "__main__":
    main()
