"""Deterministic cross-library smoke coverage for the April family branches."""

from __future__ import annotations

import importlib
import os
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


def _resolve_repo_root(repo_name: str) -> Path:
    """Resolve one sibling repo root from repo-specific env overrides when present."""
    repo_key = repo_name.removeprefix("design-research-").replace("-", "_").upper()
    src_override = os.getenv(f"DESIGN_RESEARCH_{repo_key}_SRC", "").strip()
    if src_override:
        return Path(src_override).expanduser().resolve().parent

    root_override = os.getenv(f"DESIGN_RESEARCH_{repo_key}_ROOT", "").strip()
    if root_override:
        return Path(root_override).expanduser().resolve()

    return WORKSPACE_ROOT / repo_name


def _bootstrap_april_family() -> object:
    """Prefer adjacent sibling worktrees for the April family smoke test."""
    repo_roots = {repo_name: _resolve_repo_root(repo_name) for repo_name in SIBLING_REPOS}
    missing = [repo_name for repo_name, repo_root in repo_roots.items() if not repo_root.exists()]
    if missing:
        pytest.skip("Missing sibling worktrees: " + ", ".join(sorted(missing)))

    for repo_name in reversed(SIBLING_REPOS):
        src_path = repo_roots[repo_name] / "src"
        src_text = str(src_path)
        if src_text not in sys.path:
            sys.path.insert(0, src_text)

    for module_prefix in (
        "design_research",
        "design_research_agents",
        "design_research_analysis",
        "design_research_experiments",
        "design_research_problems",
    ):
        for module_name in [
            name
            for name in sys.modules
            if name == module_prefix or name.startswith(f"{module_prefix}.")
        ]:
            sys.modules.pop(module_name, None)

    return importlib.import_module("design_research")


def test_april_family_wrapper_exports_track_local_siblings() -> None:
    """Keep the umbrella wrappers aligned with adjacent sibling public exports."""
    dr = _bootstrap_april_family()
    sibling_agents = importlib.import_module("design_research_agents")
    sibling_experiments = importlib.import_module("design_research_experiments")
    sibling_analysis = importlib.import_module("design_research_analysis")
    sibling_problems = importlib.import_module("design_research_problems")

    assert dr.agents.__all__ == sibling_agents.__all__
    assert dr.experiments.__all__ == sibling_experiments.__all__
    assert dr.analysis.__all__ == sibling_analysis.__all__
    assert dr.problems.__all__ == sibling_problems.__all__
    assert dr.agents.Workflow is sibling_agents.Workflow
    assert dr.agents.integration is sibling_agents.integration
    assert dr.experiments.build_strategy_comparison_study is (
        sibling_experiments.build_strategy_comparison_study
    )
    assert dr.analysis.build_condition_metric_table is sibling_analysis.build_condition_metric_table
    assert dr.analysis.compare_condition_pairs is sibling_analysis.compare_condition_pairs
    assert dr.analysis.embedding_maps is sibling_analysis.embedding_maps
    assert dr.analysis.integration is sibling_analysis.integration
    assert dr.analysis.visualization is sibling_analysis.visualization
    assert dr.analysis.__version__ == sibling_analysis.__version__
    assert dr.problems.list_problems is sibling_problems.list_problems
    assert dr.problems.integration is sibling_problems.integration
    assert dr.problems.__version__ == sibling_problems.__version__


def test_april_family_interoperability_smoke(tmp_path: Path) -> None:
    """Run one packaged problem through the family stack and validate the artifact handoff."""
    dr = _bootstrap_april_family()
    problem_id = "gmpb_default_dynamic_min"
    baseline_agent_id = "SeededRandomBaselineAgent"

    study = dr.experiments.Study(
        study_id="umbrella-april-family-smoke",
        title="Umbrella April family smoke",
        description="Exercise packaged problems, agents, experiments, and analysis together.",
        output_dir=tmp_path / "umbrella-april-family-smoke",
        problem_ids=(problem_id,),
        agent_specs=(baseline_agent_id,),
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
