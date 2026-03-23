"""Canonical live strategy-comparison walkthrough for the umbrella package."""

from __future__ import annotations

from pathlib import Path

from _future_stack import (
    artifact_names,
    build_json_model_workflow,
    condition_means,
    decision_candidate_schema,
    llama_cpp_runtime_config,
    load_analysis_exports,
    require_future_apis,
    validate_exported_events,
)
from _workspace_bootstrap import bootstrap_sibling_sources

# For the live walkthrough, use the workspace bootstrap helper that knows where
# the sibling repositories usually live and how to override them in local setups.
bootstrap_sibling_sources()

# Import the umbrella package only after the sibling-source bootstrap step.
import design_research as dr  # noqa: E402

# These constants keep the live walkthrough readable: one packaged problem, one
# study id, stable artifact paths, and the statistical settings used in the
# pairwise comparisons later on.
PROBLEM_ID = "decision_laptop_design_profit_maximization"
STUDY_ID = "prompt_strategy_comparison_study"
OUTPUT_DIR = Path("artifacts") / "examples" / STUDY_ID
SUMMARY_REPORT_NAME = "prompt_strategy_summary.md"
DEFAULT_REPLICATES_PER_CONDITION = 50
SIGNIFICANCE_ALPHA = 0.05
EXACT_PERMUTATION_THRESHOLD = 250_000
MONTE_CARLO_PERMUTATIONS = 20_000
PERMUTATION_TEST_SEED = 17
STRATEGY_ORDER = ("random_selection", "neutral_prompt", "profit_focus_prompt")
PAIRWISE_COMPARISONS = (
    ("profit_focus_prompt", "neutral_prompt"),
    ("neutral_prompt", "random_selection"),
    ("profit_focus_prompt", "random_selection"),
)


def main() -> None:
    """Run the live strategy-comparison walkthrough with managed llama.cpp."""
    # The live example expects the newer sibling APIs and a usable llama.cpp
    # runtime. `live=True` keeps the error message honest if either is missing.
    require_future_apis(dr, live=True)

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
        # Each `agent_id` in the strategy bundle maps to an experiments
        # `agent_factory`. Workflow-backed conditions use the sibling-owned
        # `WorkflowStudyDelegate` so experiments receives a normal executable
        # agent without any umbrella-only bridge code.
        agent_factories = {
            # A simple seeded baseline gives us something deterministic to
            # compare the prompt-based strategies against.
            "random_selection": lambda _condition: dr.agents.SeededRandomBaselineAgent(seed=7),
            # The neutral condition uses the live model but keeps the instruction
            # framing generic.
            "neutral_prompt": lambda _condition: dr.agents.WorkflowStudyDelegate(
                workflow=build_json_model_workflow(
                    dr,
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
            "profit_focus_prompt": lambda _condition: dr.agents.WorkflowStudyDelegate(
                workflow=build_json_model_workflow(
                    dr,
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
            agent_factories=agent_factories,
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
    validation_report = validate_exported_events(dr, artifact_paths)

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


if __name__ == "__main__":
    main()
