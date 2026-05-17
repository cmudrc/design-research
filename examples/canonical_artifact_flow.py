"""Smallest deterministic problems-agents-experiments-analysis handoff."""

from __future__ import annotations

from pathlib import Path
from statistics import mean

import design_research as dr

PROBLEM_ID = "decision_laptop_design_profit_maximization"
AGENT_ID = "SeededRandomBaselineAgent"
STUDY_ID = "canonical_artifact_flow"
OUTPUT_DIR = Path("artifacts") / "examples" / STUDY_ID
PRIMARY_METRIC = "primary_outcome"


def main() -> None:
    """Run one packaged problem through the public umbrella stack."""
    problem = dr.problems.get_problem(PROBLEM_ID)
    study = dr.experiments.build_strategy_comparison_study(
        dr.experiments.StrategyComparisonConfig(
            study_id=STUDY_ID,
            title="Canonical Artifact Flow",
            description="Run the minimal composed ecosystem path and validate its artifacts.",
            bundle=dr.experiments.BenchmarkBundle(
                bundle_id="canonical-artifact-flow",
                name="Canonical Artifact Flow",
                description="One packaged benchmark and one public baseline agent.",
                problem_ids=(PROBLEM_ID,),
                agent_specs=(AGENT_ID,),
            ),
            run_budget=dr.experiments.RunBudget(replicates=2, parallelism=1, max_runs=2),
            output_dir=OUTPUT_DIR,
        )
    )

    conditions = dr.experiments.build_design(study)
    results = dr.experiments.run_study(
        study,
        conditions=conditions,
        checkpoint=False,
        show_progress=False,
    )
    artifacts = dr.experiments.export_analysis_tables(
        study,
        conditions=conditions,
        run_results=results,
        output_dir=study.output_dir / "analysis",
        validate_with_analysis_package=True,
    )

    loaded = dr.analysis.integration.load_experiment_artifacts(artifacts["events.csv"])
    event_report = dr.analysis.integration.validate_experiment_events(artifacts["events.csv"])
    metric_rows = dr.analysis.build_condition_metric_table(
        loaded["runs.csv"],
        metric=PRIMARY_METRIC,
        condition_column="agent_id",
        conditions=loaded["conditions.csv"],
        evaluations=loaded["evaluations.csv"],
    )
    summary_path = dr.experiments.write_markdown_report(
        study.output_dir,
        "canonical_artifact_flow_summary.md",
        dr.experiments.render_markdown_summary(study, results),
    )

    values = [float(row["value"]) for row in metric_rows]
    successes = sum(result.status.value == "success" for result in results)

    print("Canonical artifact flow:", study.study_id)
    print("Package path: problems -> agents -> experiments -> analysis")
    print("Problem:", problem.metadata.title)
    print("Agent:", AGENT_ID)
    print("Runs:", len(results), f"({successes} success)")
    print(f"Mean {PRIMARY_METRIC}:", f"{mean(values):.4f}")
    print("Event rows valid:", event_report.is_valid, f"(rows={event_report.n_rows})")
    print("Summary report:", summary_path.name)
    print("Artifacts directory:", artifacts["events.csv"].parent)


if __name__ == "__main__":
    main()
