"""Deterministic cross-library smoke coverage for the April family branches."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = REPO_ROOT.parent
SIBLING_REPOS = (
    "design-research-problems",
    "design-research-agents",
    "design-research-experiments",
    "design-research-analysis",
)


def _bootstrap_april_family() -> object:
    """Prefer adjacent sibling worktrees for the April family smoke test."""
    missing = [repo_name for repo_name in SIBLING_REPOS if not (WORKSPACE_ROOT / repo_name).exists()]
    if missing:
        pytest.skip("Missing sibling worktrees: " + ", ".join(sorted(missing)))

    for repo_name in reversed(SIBLING_REPOS):
        src_path = WORKSPACE_ROOT / repo_name / "src"
        src_text = str(src_path)
        if src_text not in sys.path:
            sys.path.insert(0, src_text)

    for module_name in (
        "design_research",
        "design_research.agents",
        "design_research.analysis",
        "design_research.experiments",
        "design_research.problems",
        "design_research_agents",
        "design_research_analysis",
        "design_research_analysis.integration",
        "design_research_experiments",
        "design_research_problems",
    ):
        sys.modules.pop(module_name, None)

    return importlib.import_module("design_research")


def test_april_family_interoperability_smoke(tmp_path: Path) -> None:
    """Run one packaged problem through the family stack and validate the artifact handoff."""
    dr = _bootstrap_april_family()
    problem_id = "gmpb_default_dynamic_min"

    study = dr.experiments.Study(
        study_id="umbrella-april-family-smoke",
        title="Umbrella April family smoke",
        description="Exercise packaged problems, agents, experiments, and analysis together.",
        output_dir=tmp_path / "umbrella-april-family-smoke",
        problem_ids=(problem_id,),
        agent_specs=("SeededRandomBaselineAgent",),
        outcomes=(
            dr.experiments.OutcomeSpec(
                name="primary_outcome",
                source_table="runs",
                column="primary_outcome",
                aggregation="mean",
                primary=True,
            ),
        ),
        run_budget=dr.experiments.RunBudget(replicates=1, parallelism=1, max_runs=1),
        primary_outcomes=("primary_outcome",),
    )
    conditions = dr.experiments.build_design(study)
    run_results = dr.experiments.run_study(
        study,
        conditions=conditions,
        problem_registry={problem_id: dr.experiments.resolve_problem(problem_id)},
        agent_factories=dr.experiments.make_seeded_random_baseline_factories(),
        checkpoint=False,
        show_progress=False,
    )

    assert len(run_results) == 1
    assert run_results[0].status.value == "success"

    exported = dr.experiments.export_analysis_tables(
        study,
        conditions=conditions,
        run_results=run_results,
        output_dir=study.output_dir / "analysis",
        validate_with_analysis_package=True,
    )

    artifacts = dr.analysis.integration.load_experiment_artifacts(exported["events.csv"])
    report = dr.analysis.integration.validate_experiment_events(exported["events.csv"])
    metric_rows = dr.analysis.build_condition_metric_table(
        artifacts["runs.csv"],
        metric="primary_outcome",
        condition_column="agent_id",
        conditions=artifacts["conditions.csv"],
        evaluations=artifacts["evaluations.csv"],
    )

    assert report.is_valid
    assert artifacts["manifest.json"]["study_id"] == study.study_id
    assert metric_rows
