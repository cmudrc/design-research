"""Run an authentic packaged design evaluator, then draft from retained evidence."""

from __future__ import annotations

import argparse
import csv
import json
import statistics
from pathlib import Path
from typing import Any

import design_research as dr
from _paper_workflow import compile_paper_draft, run_fresh_phases

STUDY_ID = "computational_design_evidence_to_paper"
OUTPUT_DIR = Path("artifacts") / "examples" / STUDY_ID
PROBLEM_ID = "decision_laptop_design_profit_maximization"
AGENT_ID = "SeededRandomBaselineAgent"
ANALYSIS_ID = "laptop-evaluator-summary"
SUPPORTING_DATA = "artifacts/analysis/supporting-data/laptop-metrics.csv"


def main() -> None:
    """Execute the selected phase or orchestrate both phases in fresh processes."""
    args = _parse_args()
    if args.phase == "all":
        run_fresh_phases(
            Path(__file__),
            args.output_dir,
            require_tectonic=args.require_tectonic,
        )
    elif args.phase == "run":
        _run_and_analyze(args.output_dir)
    else:
        _draft_compile_and_bundle(args.output_dir, require_tectonic=args.require_tectonic)


def _parse_args() -> argparse.Namespace:
    """Parse the example's explicit lifecycle controls."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=("all", "run", "draft"), default="all")
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    parser.add_argument("--require-tectonic", action="store_true")
    return parser.parse_args()


def _study(output_dir: Path) -> Any:
    """Build a seeded packaged laptop-design evaluation study."""
    return dr.experiments.Study(
        study_id=STUDY_ID,
        title="Computational Design Evidence to Paper Draft",
        description=(
            "A deterministic offline sample of packaged laptop candidates and evaluator outputs."
        ),
        rationale=(
            "The example demonstrates retained candidate designs, authentic evaluator records, "
            "artifact-first metric analysis, and an explicit paper-draft handoff."
        ),
        problem_ids=(PROBLEM_ID,),
        agent_specs=(AGENT_ID,),
        outcomes=(
            dr.experiments.OutcomeSpec(
                name="primary_outcome",
                source_table="runs",
                column="primary_outcome",
                aggregation="mean",
                primary=True,
            ),
        ),
        run_budget=dr.experiments.RunBudget(replicates=8, parallelism=1, max_runs=8),
        output_dir=output_dir,
    )


def _run_and_analyze(output_dir: Path) -> None:
    """Execute real problem evaluation and persist its analysis record and assets."""
    study = _study(output_dir)
    conditions = dr.experiments.build_design(study)
    results = dr.experiments.run_study(
        study,
        conditions=conditions,
        checkpoint=False,
        show_progress=False,
    )
    successful = [result for result in results if result.status.value == "success"]
    metric_rows = dr.analysis.build_run_metric_table_from_artifacts(
        output_dir,
        metrics=("primary_outcome", "utility", "predicted_share", "expected_demand_units"),
        run_columns=("replicate", "problem_id", "status", "seed"),
    )
    metric_path = output_dir / SUPPORTING_DATA
    _write_metric_rows(metric_path, metric_rows)
    profile = dr.analysis.profile_dataframe(metric_path)
    table_path = _write_summary_table(output_dir, metric_rows)
    figure_path = _write_evaluator_figure(output_dir, metric_rows)
    record = dr.analysis.build_analysis_result(
        profile,
        analysis_id=ANALYSIS_ID,
        candidate_run_ids=tuple(result.run_id for result in successful),
        included_run_ids=tuple(result.run_id for result in successful),
        tables=(table_path.relative_to(output_dir).as_posix(),),
        figures=(figure_path.relative_to(output_dir).as_posix(),),
        evidence_refs=("runs.csv", "evaluations.csv", SUPPORTING_DATA),
        source_api="build_run_metric_table_from_artifacts + profile_dataframe",
    )
    dr.analysis.write_analysis_result(record, output_dir=output_dir, overwrite=True)
    private_dir = output_dir / "artifacts" / "runs" / successful[0].run_id / "attachments"
    private_dir.mkdir(parents=True, exist_ok=True)
    (private_dir / "participant-private-note.txt").write_text(
        "Sensitive fixture excluded unless explicitly selected.\n",
        encoding="utf-8",
    )
    print(f"Computational design study: {study.study_id}")
    print(f"Packaged problem: {PROBLEM_ID}")
    print(f"Runs: {len(results)} ({len(successful)} successful)")
    print(f"Raw candidate records: {len(successful)}")
    print(f"Evaluator metric rows: {sum(len(result.evaluator_outputs) for result in successful)}")
    print("Paper draft created during execution: False")


def _write_metric_rows(path: Path, rows: list[dict[str, Any]]) -> None:
    """Persist the artifact-first metric table selected for the bundle."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0])
    with path.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _write_summary_table(output_dir: Path, rows: list[dict[str, Any]]) -> Path:
    """Write a compact LaTeX table of authentic evaluator summaries."""
    path = output_dir / "artifacts" / "analysis" / "tables" / "laptop-summary.tex"
    path.parent.mkdir(parents=True, exist_ok=True)
    metrics = ("primary_outcome", "utility", "expected_demand_units")
    lines = ["\\begin{tabular}{lrrr}", "Metric & Mean & Min & Max \\\\", "\\hline"]
    for metric in metrics:
        values = [float(row[metric]) for row in rows]
        label = metric.replace("_", "\\_")
        lines.append(
            f"{label} & {statistics.fmean(values):.4g} & {min(values):.4g} & {max(values):.4g} \\\\"
        )
    lines.append("\\end{tabular}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def _write_evaluator_figure(output_dir: Path, rows: list[dict[str, Any]]) -> Path:
    """Plot retained share and utility outputs by deterministic replicate."""
    import matplotlib.pyplot as plt

    path = output_dir / "artifacts" / "analysis" / "figures" / "laptop-evaluator.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    figure, left_axis = plt.subplots(figsize=(5.2, 3.2))
    replicates = [int(row["replicate"]) for row in rows]
    left_axis.plot(
        replicates,
        [float(row["predicted_share"]) for row in rows],
        marker="o",
        color="#1f5a85",
        label="Predicted share",
    )
    left_axis.set(xlabel="Replicate", ylabel="Predicted share")
    right_axis = left_axis.twinx()
    right_axis.plot(
        replicates,
        [float(row["utility"]) for row in rows],
        marker="s",
        color="#a14f2b",
        label="Utility",
    )
    right_axis.set_ylabel("Utility")
    figure.tight_layout()
    figure.savefig(path, dpi=140)
    plt.close(figure)
    return path


def _agent_packet(run_ids: tuple[str, ...]) -> dict[str, Any]:
    """Collect configured and observed metadata for the packaged baseline agent."""
    return dr.agents.collect_agent_paper_contributions(
        dr.agents.SeededRandomBaselineAgent(),
        execution_result={
            "success": True,
            "execution_order": ["seeded_random_baseline"],
            "step_results": {"seeded_random_baseline": {"status": "completed"}},
            "tool_results": [],
            "metadata": {},
        },
        evidence_refs=tuple(f"artifacts/runs/{run_id}/run.json" for run_id in run_ids),
    )


def _draft_compile_and_bundle(output_dir: Path, *, require_tectonic: bool) -> None:
    """Regenerate metadata, export a draft, compile it, and verify its bundle."""
    record = dr.analysis.load_analysis_result(
        output_dir / "artifacts" / "analysis" / "results" / f"{ANALYSIS_ID}.json"
    )
    packets = (
        dr.problems.collect_problem_paper_contributions(PROBLEM_ID),
        _agent_packet(tuple(record.included_run_ids)),
        dr.analysis.collect_analysis_paper_contributions(record),
    )
    paths = dr.experiments.export_paper_draft(
        output_dir,
        component_packets=packets,
        overwrite=True,
    )
    compiled = compile_paper_draft(
        paths["main.tex"].parent,
        require_tectonic=require_tectonic,
    )
    bundle = dr.analysis.create_research_bundle(
        output_dir,
        supporting_data=(SUPPORTING_DATA,),
        overwrite=True,
    )
    verification = dr.analysis.verify_research_bundle(bundle)
    manifest = json.loads(paths["paper_draft_manifest.json"].read_text(encoding="utf-8"))
    print("Fresh-process draft: paper-draft/main.tex")
    print(f"LaTeX compile: {'passed' if compiled else 'skipped (tectonic unavailable)'}")
    print(f"Run accounting: {json.dumps(manifest['run_accounting'], sort_keys=True)}")
    print(f"Bundle verified: {verification['valid']} ({verification['file_count']} members)")


if __name__ == "__main__":
    main()
