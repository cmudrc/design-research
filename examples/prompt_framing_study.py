"""Canonical live strategy-comparison walkthrough for the umbrella package."""

from __future__ import annotations

import csv
import importlib.util
import json
import os
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

    # Resolve the packaged problem once so every run pulls from the same
    # normalized problem packet.
    problem_registry = {PROBLEM_ID: dr.experiments.resolve_problem(PROBLEM_ID)}

    # Start a managed llama.cpp server client for the duration of the study.
    # The context manager handles startup/shutdown around the live run.
    with dr.agents.LlamaCppServerLLMClient(
        model=str(runtime["model_source"]),
        hf_model_repo_id=runtime["model_repo"],
        api_model=str(runtime["model_name"]),
        host=str(runtime["host"]),
        port=int(runtime["port"]),
        context_window=int(runtime["context_window"]),
    ) as llm_client:
        # Each `agent_id` in the strategy bundle maps either to a public agent
        # id resolved directly by experiments or to one explicit binding that
        # returns a prompt-driven workflow agent.
        agent_bindings = {
            # The neutral condition uses the live model but keeps the instruction
            # framing generic.
            "neutral_prompt": lambda _condition: dr.agents.PromptWorkflowAgent(
                workflow=build_json_model_workflow(
                    llm_client=llm_client,
                    candidate_schema=candidate_schema,
                    study_id=STUDY_ID,
                    problem_id=PROBLEM_ID,
                    fallback_model_name=str(runtime["model_name"]),
                    fallback_provider=str(runtime["provider_name"]),
                ),
                prompt_builder=lambda problem_packet, _run_spec, _condition: _strategy_prompt(
                    problem_packet,
                    instruction=(
                        "Condition: neutral prompt. Choose the best overall candidate using the "
                        "packaged demand and feasibility information."
                    ),
                ),
            ),
            # The profit-focused condition swaps only the framing instruction so
            # the study isolates prompt strategy rather than model identity.
            "profit_focus_prompt": lambda _condition: dr.agents.PromptWorkflowAgent(
                workflow=build_json_model_workflow(
                    llm_client=llm_client,
                    candidate_schema=candidate_schema,
                    study_id=STUDY_ID,
                    problem_id=PROBLEM_ID,
                    fallback_model_name=str(runtime["model_name"]),
                    fallback_provider=str(runtime["provider_name"]),
                ),
                prompt_builder=lambda problem_packet, _run_spec, _condition: _strategy_prompt(
                    problem_packet,
                    instruction=(
                        "Condition: profit-focus prompt. Prioritize choices that maximize "
                        "market share proxy and expected demand."
                    ),
                ),
            ),
        }

        # Execute the full study while the managed llama.cpp client is running.
        results = dr.experiments.run_study(
            study,
            conditions=conditions,
            agent_bindings=agent_bindings,
            problem_registry=problem_registry,
            checkpoint=False,
            show_progress=False,
        )

    # Export the standard analysis tables so the next steps can work from the
    # same artifacts users would inspect after their own runs.
    artifact_paths = dr.experiments.export_analysis_tables(
        study,
        conditions=conditions,
        run_results=results,
        output_dir=OUTPUT_DIR,
    )

    # Load only the CSVs we need for the walkthrough's reporting and statistical
    # comparison steps.
    exported_rows = load_analysis_exports(
        artifact_paths,
        names=("conditions.csv", "runs.csv", "evaluations.csv"),
    )

    # Confirm that the event-level export is structurally valid before building
    # downstream tables from it.
    validation_report = validate_exported_events(artifact_paths)

    # Build one condition-by-metric table for the primary outcome we care about
    # and another for a secondary business-facing metric.
    primary_metric_rows = dr.analysis.build_condition_metric_table(
        exported_rows["runs.csv"],
        metric="market_share_proxy",
        condition_column="agent_id",
        conditions=exported_rows["conditions.csv"],
        evaluations=exported_rows["evaluations.csv"],
    )
    demand_metric_rows = dr.analysis.build_condition_metric_table(
        exported_rows["runs.csv"],
        metric="expected_demand_units",
        condition_column="agent_id",
        conditions=exported_rows["conditions.csv"],
        evaluations=exported_rows["evaluations.csv"],
    )

    # Compare the strategy pairs using the analysis package's pairwise
    # permutation test helper.
    comparison_report = dr.analysis.compare_condition_pairs(
        primary_metric_rows,
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
    successful_results = [result for result in results if result.status.value == "success"]

    # Fail loudly if the live walkthrough did not actually produce usable data.
    if not successful_results:
        raise RuntimeError("The live walkthrough completed without any successful runs.")
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
            f"mean_market_share_proxy={primary_means.get(strategy_name, 0.0):.4f}, "
            f"mean_expected_demand_units={demand_means.get(strategy_name, 0.0):.0f}"
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


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    """Read one exported CSV table into a list of row dictionaries."""
    with path.open("r", encoding="utf-8", newline="") as file_obj:
        return list(csv.DictReader(file_obj))


def load_analysis_exports(
    artifact_paths: dict[str, Path],
    *,
    names: tuple[str, ...],
) -> dict[str, list[dict[str, str]]]:
    """Load selected exported CSV artifacts into memory."""
    return {name: read_csv_rows(artifact_paths[name]) for name in names}


def validate_exported_events(artifact_paths: dict[str, Path]) -> object:
    """Validate the exported canonical event table through the analysis layer."""
    return dr.analysis.integration.validate_experiment_events(artifact_paths["events.csv"])


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
            "Install llama-cpp-python[server] before running the live walkthrough. Missing: "
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
            "Install huggingface-hub or point LLAMA_CPP_MODEL at a local GGUF file before "
            "running the live walkthrough."
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
        "replicates": replicates,
    }


def build_json_model_workflow(
    *,
    llm_client: object,
    candidate_schema: dict[str, object],
    study_id: str,
    problem_id: str,
    fallback_model_name: str,
    fallback_provider: str,
) -> object:
    """Build one reusable prompt-mode workflow that returns structured JSON."""

    def request_builder(context: dict[str, object]) -> object:
        """Build one structured LLM request from the workflow context."""
        return dr.agents.LLMRequest(
            messages=[
                dr.agents.LLMMessage(
                    role="system",
                    content=(
                        "You are a careful study participant. Return valid JSON only and match "
                        "the requested schema exactly."
                    ),
                ),
                dr.agents.LLMMessage(role="user", content=str(context["prompt"])),
            ],
            temperature=0.0,
            max_tokens=400,
            response_schema=candidate_schema,
            metadata={"study_id": study_id, "problem_id": problem_id},
        )

    def response_parser(response: object, _context: dict[str, object]) -> dict[str, object]:
        """Parse one model response into workflow output, metrics, and events."""
        model_text = strip_markdown_fences(str(getattr(response, "text", "")).strip())
        candidate = json.loads(model_text)
        if not isinstance(candidate, dict):
            raise RuntimeError("Expected the live workflow to return one JSON object candidate.")
        provider = str(getattr(response, "provider", "") or fallback_provider)
        model_name = str(getattr(response, "model", "") or fallback_model_name)
        return {
            "final_output": candidate,
            "metrics": usage_metrics(getattr(response, "usage", None)),
            "events": [
                {
                    "event_type": "model_response",
                    "actor_id": "agent",
                    "text": model_text,
                    "meta_json": {"provider": provider, "model_name": model_name},
                }
            ],
        }

    return dr.agents.Workflow(
        steps=(
            dr.agents.ModelStep(
                step_id="select_candidate",
                llm_client=llm_client,
                request_builder=request_builder,
                response_parser=response_parser,
            ),
        ),
        output_schema=candidate_schema,
        default_request_id_prefix=study_id,
    )


def strip_markdown_fences(text: str) -> str:
    """Strip one optional fenced-code wrapper from a model response."""
    if not text.startswith("```"):
        return text
    lines = text.splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].startswith("```"):
        lines = lines[:-1]
    return "\n".join(lines).strip()


def usage_metrics(usage: object) -> dict[str, object]:
    """Normalize usage payloads into canonical metric names."""
    metrics: dict[str, object] = {"cost_usd": 0.0}
    if isinstance(usage, dict):
        prompt_tokens = usage.get("prompt_tokens")
        completion_tokens = usage.get("completion_tokens")
    else:
        prompt_tokens = getattr(usage, "prompt_tokens", None)
        completion_tokens = getattr(usage, "completion_tokens", None)
    if isinstance(prompt_tokens, int):
        metrics["input_tokens"] = prompt_tokens
    if isinstance(completion_tokens, int):
        metrics["output_tokens"] = completion_tokens
    return metrics


if __name__ == "__main__":
    main()
