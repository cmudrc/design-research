"""Run a deterministic ideation study, then assemble its paper draft afresh."""

from __future__ import annotations

import argparse
import csv
import json
import random
from pathlib import Path
from typing import Any

import design_research as dr
from _paper_workflow import compile_paper_draft, run_fresh_phases

STUDY_ID = "ideation_evidence_to_paper"
OUTPUT_DIR = Path("artifacts") / "examples" / STUDY_ID
AGENT_ID = "scripted_partial_factorial_ideator"
PRIMARY_METRIC = "primary_outcome"
ANALYSIS_ID = "h1-ideation-regression"
SUPPORTING_DATA = "artifacts/analysis/supporting-data/ideation-regression"

MODEL_LEVELS = {
    "mini": ("open-class-mini", 1.5, "open_class"),
    "base": ("open-class-base", 7.0, "open_class"),
    "large": ("open-class-large", 14.0, "open_class"),
    "reasoner": ("open-class-reasoner", 32.0, "open_class"),
}
TASK_LEVELS = {
    "access": ("ideation_accessible_drinking_fountain", "accessibility", 0.07),
    "mobility": ("ideation_bicycle_safety_lock", "mobility", 0.02),
    "workspace": ("ideation_office_sit_stand_table", "furniture", 0.04),
    "energy": ("ideation_solar_powered_cooking_device", "energy", -0.01),
    "medical": ("ideation_hospital_blood_pressure_measurement", "medical", 0.00),
    "agriculture": ("ideation_peanut_shelling", "agriculture", -0.03),
}
PARTIAL_ROWS = (
    ("mini", "access"),
    ("mini", "energy"),
    ("mini", "medical"),
    ("base", "mobility"),
    ("base", "workspace"),
    ("base", "agriculture"),
    ("large", "access"),
    ("large", "workspace"),
    ("large", "energy"),
    ("reasoner", "mobility"),
    ("reasoner", "medical"),
    ("reasoner", "agriculture"),
)


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
    """Build the partial-factorial ideation study definition."""
    return dr.experiments.Study(
        study_id=STUDY_ID,
        title="Ideation Evidence to Paper Draft",
        description=(
            "A deterministic partial-factorial study of model scale and packaged ideation task."
        ),
        rationale=(
            "The example tests whether the scripted quality proxy changes with model scale while "
            "retaining prompt and source lineage for the selected tasks."
        ),
        factors=(
            dr.experiments.Factor(
                name="model_size_b",
                description="Nominal model parameter count in billions.",
                dtype="float",
                levels=tuple(
                    dr.experiments.Level(name=key, value=size)
                    for key, (_, size, _) in MODEL_LEVELS.items()
                ),
            ),
            dr.experiments.Factor(
                name="task_family",
                description="Packaged ideation task family.",
                levels=tuple(
                    dr.experiments.Level(name=key, value=family)
                    for key, (_, family, _) in TASK_LEVELS.items()
                ),
            ),
        ),
        agent_specs=(AGENT_ID,),
        problem_ids=tuple(problem_id for problem_id, _, _ in TASK_LEVELS.values()),
        hypotheses=(
            dr.experiments.Hypothesis(
                hypothesis_id="H1",
                label="Model-scale association",
                statement="The retained ideation quality proxy changes with nominal model scale.",
                independent_vars=("model_size_b",),
                dependent_vars=(PRIMARY_METRIC,),
            ),
        ),
        outcomes=(
            dr.experiments.OutcomeSpec(
                name=PRIMARY_METRIC,
                source_table="runs",
                column=PRIMARY_METRIC,
                aggregation="mean",
                primary=True,
            ),
        ),
        analysis_plans=(
            dr.experiments.AnalysisPlan(
                analysis_plan_id="ap-ideation-regression",
                hypothesis_ids=("H1",),
                tests=("ordinary_least_squares",),
                outcomes=(PRIMARY_METRIC,),
            ),
        ),
        run_budget=dr.experiments.RunBudget(replicates=2, parallelism=1, max_runs=24),
        output_dir=output_dir,
    )


def _conditions() -> list[Any]:
    """Materialize the explicit 12-row partial-factorial design."""
    conditions = []
    for index, (model_key, task_key) in enumerate(PARTIAL_ROWS, start=1):
        model_name, model_size_b, model_family = MODEL_LEVELS[model_key]
        problem_id, task_family, _ = TASK_LEVELS[task_key]
        conditions.append(
            dr.experiments.Condition(
                condition_id=f"pf-{index:02d}",
                factor_assignments={
                    "model_name": model_name,
                    "model_family": model_family,
                    "model_size_b": model_size_b,
                    "task_family": task_family,
                    "problem_id": problem_id,
                },
                block_assignments={},
                metadata={"model_key": model_key, "task_key": task_key},
            )
        )
    return conditions


def _ideation_agent(
    *,
    run_spec: Any,
    condition: Any,
    problem_packet: Any,
    seed: int,
) -> dict[str, object]:
    """Return one retained, deterministic ideation trace and proxy score."""
    if condition.condition_id == "pf-12" and run_spec.replicate == 2:
        raise RuntimeError("intentional fixture failure after evidence initialization")
    size_b = float(condition.factor_assignments["model_size_b"])
    model_name = str(condition.factor_assignments["model_name"])
    task_family = str(condition.factor_assignments["task_family"])
    task_bonus = next(
        bonus
        for problem_id, family, bonus in TASK_LEVELS.values()
        if problem_id == problem_packet.problem_id and family == task_family
    )
    score = 0.48 + 0.010 * size_b + task_bonus + random.Random(seed).uniform(-0.02, 0.02)
    return dr.experiments.agent_result(
        f"{model_name} concept for {problem_packet.problem_id}",
        metrics={PRIMARY_METRIC: score},
        events=(
            {"event_type": "inspect", "text": problem_packet.brief[:90]},
            {"event_type": "analogize", "text": f"look for {task_family} analogies"},
            {"event_type": "ideate", "text": f"{model_name} drafts alternatives"},
            {"event_type": "critique", "text": "score novelty and feasibility"},
            {"event_type": "select", "text": "select final concept"},
        ),
        metadata={
            "agent_kind": "scripted",
            "model_name": model_name,
            "pattern_name": "partial-factorial-ideation",
        },
    )


def _run_and_analyze(output_dir: Path) -> None:
    """Run 24 attempts, retain one failure, and analyze a documented subset."""
    study = _study(output_dir)
    results = dr.experiments.run_study(
        study,
        conditions=_conditions(),
        agent_bindings={AGENT_ID: _ideation_agent},
        checkpoint=False,
        show_progress=False,
    )
    successful = [result for result in results if result.status.value == "success"]
    failed = [result for result in results if result.status.value == "failed"]
    excluded = successful[:2]
    included = successful[2:]
    supporting_dir = output_dir / SUPPORTING_DATA
    _write_filtered_artifacts(
        output_dir,
        supporting_dir,
        included_run_ids={result.run_id for result in included},
    )
    regression = dr.analysis.fit_regression_from_artifacts(
        supporting_dir,
        outcome=PRIMARY_METRIC,
        predictors=("model_size_b", "task_family"),
        categorical_predictors=("task_family",),
    )
    table_path = _write_regression_table(output_dir, regression)
    figure_path = _write_regression_figure(output_dir, supporting_dir)
    record = dr.analysis.build_analysis_result(
        regression,
        analysis_id=ANALYSIS_ID,
        analysis_plan_ids=("ap-ideation-regression",),
        hypothesis_ids=("H1",),
        candidate_run_ids=tuple(result.run_id for result in successful),
        included_run_ids=tuple(result.run_id for result in included),
        exclusions=tuple(
            {
                "run_id": result.run_id,
                "reason": "Prespecified two-run reporting holdout for exclusion accounting.",
            }
            for result in excluded
        ),
        assumptions=(
            dr.analysis.AnalysisCheck(
                check_id="deterministic-fixture",
                status="passed",
                detail="The offline agent and study seed policy are deterministic.",
            ),
        ),
        tables=(table_path.relative_to(output_dir).as_posix(),),
        figures=(figure_path.relative_to(output_dir).as_posix(),),
        evidence_refs=tuple(f"artifacts/runs/{result.run_id}/run.json" for result in included),
        source_api="fit_regression_from_artifacts",
    )
    dr.analysis.write_analysis_result(record, output_dir=output_dir, overwrite=True)
    private_note = output_dir / "artifacts" / "runs" / successful[0].run_id / "attachments"
    private_note.mkdir(parents=True, exist_ok=True)
    (private_note / "participant-private-note.txt").write_text(
        "Sensitive fixture excluded unless explicitly selected.\n",
        encoding="utf-8",
    )
    print(f"Ideation study: {study.study_id}")
    print(f"Attempts: {len(results)} ({len(successful)} successful, {len(failed)} failed)")
    print(f"Analysis: {len(included)} included, {len(excluded)} documented exclusions")
    print(f"Regression samples: {regression.n_samples}")
    print("Paper draft created during execution: False")


def _write_filtered_artifacts(
    source_dir: Path,
    target_dir: Path,
    *,
    included_run_ids: set[str],
) -> None:
    """Write the prespecified analysis subset in canonical CSV form."""
    target_dir.mkdir(parents=True, exist_ok=True)
    (target_dir / "manifest.json").write_bytes((source_dir / "manifest.json").read_bytes())
    for filename in ("conditions.csv", "runs.csv", "events.csv", "evaluations.csv"):
        with (source_dir / filename).open(newline="", encoding="utf-8") as source:
            reader = csv.DictReader(source)
            rows = list(reader)
            fieldnames = reader.fieldnames or []
        if filename != "conditions.csv":
            rows = [row for row in rows if row.get("run_id") in included_run_ids]
        with (target_dir / filename).open("w", newline="", encoding="utf-8") as target:
            writer = csv.DictWriter(target, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)


def _write_regression_table(output_dir: Path, regression: Any) -> Path:
    """Write a small LaTeX coefficient table referenced by the result record."""
    path = output_dir / "artifacts" / "analysis" / "tables" / "ideation-regression.tex"
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = ["\\begin{tabular}{lr}", "Coefficient & Estimate \\\\", "\\hline"]
    rows.append(f"Intercept & {regression.intercept:.4f} \\\\")
    for name, value in sorted(regression.coefficients.items()):
        rows.append(f"{name.replace('_', '\\_')} & {value:.4f} \\\\")
    rows.append("\\end{tabular}")
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")
    return path


def _write_regression_figure(output_dir: Path, supporting_dir: Path) -> Path:
    """Plot the retained artifact rows used by the regression."""
    import matplotlib.pyplot as plt

    metric_rows = dr.analysis.build_run_metric_table_from_artifacts(
        supporting_dir,
        metrics=PRIMARY_METRIC,
        condition_columns=("model_size_b", "task_family"),
    )
    path = output_dir / "artifacts" / "analysis" / "figures" / "ideation-regression.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    figure, axis = plt.subplots(figsize=(5.2, 3.2))
    axis.scatter(
        [float(row["model_size_b"]) for row in metric_rows],
        [float(row[PRIMARY_METRIC]) for row in metric_rows],
        color="#1f5a85",
    )
    axis.set(xlabel="Nominal model size (B)", ylabel="Retained quality proxy")
    figure.tight_layout()
    figure.savefig(path, dpi=140)
    plt.close(figure)
    return path


def _scripted_agent_packet(run_ids: tuple[str, ...]) -> dict[str, Any]:
    """Describe the example-local agent without claiming unavailable internals."""
    evidence_refs = [f"artifacts/runs/{run_id}/run.json" for run_id in run_ids]
    return {
        "schema_version": dr.problems.PAPER_CONTRIBUTION_VERSION,
        "source": {
            "package": "design-research",
            "package_version": dr.__version__,
            "component_type": "agent",
            "component_id": AGENT_ID,
        },
        "contributions": [
            {
                "contribution_id": f"umbrella:{AGENT_ID}:methods",
                "section": "methods",
                "kind": "paragraph",
                "text": (
                    "An example-local scripted ideation agent executed a five-stage inspect, "
                    "analogize, ideate, critique, and select sequence with per-run seeded noise."
                ),
                "evidence_basis": "configured",
                "citation_keys": [],
                "evidence_refs": ["study.yaml#/agent_specs/0"],
                "metadata": {"offline": True, "stages": 5},
            },
            {
                "contribution_id": f"umbrella:{AGENT_ID}:observed",
                "section": "methods",
                "kind": "paragraph",
                "text": f"Retained run evidence records {len(run_ids)} successful executions.",
                "evidence_basis": "observed",
                "citation_keys": [],
                "evidence_refs": evidence_refs,
                "metadata": {"successful_run_ids": list(run_ids)},
            },
        ],
        "references": [],
        "reporting_gaps": [],
    }


def _draft_compile_and_bundle(output_dir: Path, *, require_tectonic: bool) -> None:
    """Reconstruct contributions, export a draft, compile it, and verify its bundle."""
    record = dr.analysis.load_analysis_result(
        output_dir / "artifacts" / "analysis" / "results" / f"{ANALYSIS_ID}.json"
    )
    run_ids = tuple(record.included_run_ids)
    packets = (
        *(
            dr.problems.collect_problem_paper_contributions(problem_id)
            for problem_id, _, _ in TASK_LEVELS.values()
        ),
        _scripted_agent_packet(run_ids),
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
