"""Authentic pump and battery benchmark portfolio for the umbrella package."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

import design_research as dr

# Group the packaged problem ids up front so the portfolio nature of the example
# is obvious at a glance.
BENCHMARK_PROBLEM_IDS = (
    "treadle_pump_ide_material_min",
    "moneymaker_hip_pump_cost_min",
    "battery_pack_18650_series_parallel_cost_min",
)
STUDY_ID = "pump_and_battery_design_portfolio"
OUTPUT_DIR = Path("artifacts") / "examples" / STUDY_ID
SUMMARY_REPORT_NAME = "pump_and_battery_design_summary.md"
BASELINE_AGENT_ID = "SeededRandomBaselineAgent"


def main() -> None:
    """Run the primary engineering recipe and print the portfolio snapshot."""
    # Resolve the real packaged benchmark titles up front so the rest of the
    # script can report application names instead of only ids.
    benchmark_titles = {
        problem_id: dr.problems.get_problem(problem_id).metadata.title
        for problem_id in BENCHMARK_PROBLEM_IDS
    }

    # Keep the bundle inline so readers can see exactly which real applications
    # are being grouped together for the portfolio run.
    benchmark_bundle = dr.experiments.BenchmarkBundle(
        bundle_id="pump-and-battery-design",
        name="Pump and Battery Design Bundle",
        description=(
            "Packaged engineering optimization problems spanning pumps and battery-pack layout."
        ),
        problem_ids=BENCHMARK_PROBLEM_IDS,
        agent_specs=(BASELINE_AGENT_ID,),
        metadata={"domain": "mechanical-engineering", "applications": ("pumps", "battery-packs")},
    )

    # Build the executed study inline so the primary recipe configuration is
    # visible in one continuous block.
    primary_study = dr.experiments.build_strategy_comparison_study(
        dr.experiments.StrategyComparisonConfig(
            study_id=STUDY_ID,
            title="Pump and Battery Design Portfolio",
            description=(
                "Run a seeded baseline across real pump and battery optimization benchmarks and "
                "report the observed objective values and feasibility."
            ),
            bundle=benchmark_bundle,
            run_budget=dr.experiments.RunBudget(
                replicates=1,
                parallelism=1,
                max_runs=len(BENCHMARK_PROBLEM_IDS),
            ),
            output_dir=OUTPUT_DIR,
        )
    )

    # Build one alternate recipe preview from the same bundle so readers can see
    # how little extra boilerplate is needed to try a different scaffold.
    preview_study = dr.experiments.build_bivariate_comparison_study(
        dr.experiments.BivariateComparisonConfig(
            study_id="pump_and_battery_recipe_preview",
            title="Pump and Battery Recipe Preview",
            description="Preview a second recipe over the same packaged engineering bundle.",
            bundle=benchmark_bundle,
            output_dir=OUTPUT_DIR / "preview",
        )
    )

    # Materialize the primary study's condition table before execution.
    conditions = dr.experiments.build_design(primary_study)

    results = dr.experiments.run_study(
        primary_study,
        conditions=conditions,
        # Resolve each packaged problem through the experiments wrapper so the
        # study sees normalized problem packets with real evaluator behavior.
        problem_registry={
            problem_id: dr.experiments.resolve_problem(problem_id)
            for problem_id in BENCHMARK_PROBLEM_IDS
        },
        checkpoint=False,
        show_progress=False,
    )

    # Export canonical CSV artifacts for later analysis and reporting.
    artifact_paths = dr.experiments.export_analysis_tables(
        primary_study,
        conditions=conditions,
        run_results=results,
        output_dir=primary_study.output_dir / "analysis",
    )

    # Check that the event export is internally consistent before reporting
    # success back to the reader.
    validation_report = validate_exported_events(artifact_paths)

    # Write a lightweight markdown summary next to those exported artifacts.
    summary_path = dr.experiments.write_markdown_report(
        primary_study.output_dir,
        SUMMARY_REPORT_NAME,
        dr.experiments.render_markdown_summary(primary_study, results),
    )

    # Count successful runs so the terminal summary is easier to read than a raw
    # dump of every result object.
    success_count = sum(result.status.value == "success" for result in results)

    # Print a portfolio snapshot showing the real applications, the executed
    # recipe, the preview recipe, and the authentic evaluator outputs.
    print("Application bundle:", benchmark_bundle.name)
    print("Benchmark portfolio:")
    for problem_id in BENCHMARK_PROBLEM_IDS:
        print(f"- {benchmark_titles[problem_id]}")
    print("Executed study:", primary_study.study_id)
    print("Preview study:", preview_study.study_id)
    print("Runs:", len(results), f"({success_count} success)")
    print("Observed benchmark results:")
    for result in results:
        run_spec = result.run_spec
        problem_id = str(getattr(run_spec, "problem_id", ""))
        metrics = getattr(result, "metrics", {}) or {}
        print(
            "- "
            f"{benchmark_titles[problem_id]}: "
            f"objective_value={float(metrics.get('objective_value', 0.0)):.6f}, "
            f"is_feasible={bool(metrics.get('is_feasible', False))}, "
            f"total_constraint_violation="
            f"{float(metrics.get('total_constraint_violation', 0.0)):.6f}"
        )
    print("Event rows valid:", validation_report.is_valid, f"(rows={validation_report.n_rows})")
    print("Summary report:", summary_path.name)
    print("Artifacts:", artifact_names(artifact_paths))


def artifact_names(artifact_paths: Mapping[str, Path]) -> str:
    """Return exported artifact filenames in stable sorted order."""
    return ", ".join(sorted(path.name for path in artifact_paths.values()))


def validate_exported_events(
    artifact_paths: Mapping[str, Path],
) -> object:
    """Validate the exported canonical event table through the analysis layer."""
    return dr.analysis.integration.validate_experiment_events(artifact_paths["events.csv"])


if __name__ == "__main__":
    main()
