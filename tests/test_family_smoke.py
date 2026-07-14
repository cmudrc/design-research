"""Deterministic cross-library smoke coverage for the pinned package family."""

from __future__ import annotations

import importlib
import json
import os
import sys
from pathlib import Path

import pytest

SIBLING_REPOS = (
    "design-research-problems",
    "design-research-agents",
    "design-research-experiments",
    "design-research-analysis",
)
EXPECTED_VERSIONS = {
    "design_research_problems": "0.4.0",
    "design_research_agents": "0.5.0",
    "design_research_experiments": "0.2.1",
    "design_research_analysis": "0.3.0",
}


def _source_override(repo_name: str) -> Path | None:
    """Resolve an explicitly configured sibling source directory."""
    repo_key = repo_name.removeprefix("design-research-").replace("-", "_").upper()
    src_override = os.getenv(f"DESIGN_RESEARCH_{repo_key}_SRC", "").strip()
    root_override = os.getenv(f"DESIGN_RESEARCH_{repo_key}_ROOT", "").strip()
    if src_override and root_override:
        raise RuntimeError(
            f"Set only one of DESIGN_RESEARCH_{repo_key}_SRC or DESIGN_RESEARCH_{repo_key}_ROOT."
        )
    if not src_override and not root_override:
        return None

    src_path = (
        Path(src_override).expanduser().resolve()
        if src_override
        else Path(root_override).expanduser().resolve() / "src"
    )
    if not src_path.is_dir():
        raise RuntimeError(f"Configured source directory does not exist: {src_path}")
    return src_path


def _bootstrap_family() -> object:
    """Load installed family packages, applying explicit source overrides only."""
    for repo_name in reversed(SIBLING_REPOS):
        src_path = _source_override(repo_name)
        if src_path is None:
            continue
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


def test_source_override_accepts_root_directory(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Translate an explicit repository root into its source directory."""
    src_path = tmp_path / "src"
    src_path.mkdir()
    monkeypatch.setenv("DESIGN_RESEARCH_PROBLEMS_ROOT", str(tmp_path))

    assert _source_override("design-research-problems") == src_path


def test_source_override_rejects_ambiguous_configuration(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Fail when both supported overrides are set for one sibling."""
    monkeypatch.setenv("DESIGN_RESEARCH_AGENTS_ROOT", str(tmp_path))
    monkeypatch.setenv("DESIGN_RESEARCH_AGENTS_SRC", str(tmp_path / "src"))

    with pytest.raises(RuntimeError, match="Set only one"):
        _source_override("design-research-agents")


def test_family_wrapper_exports_track_pinned_siblings() -> None:
    """Keep umbrella wrappers aligned with the installed sibling public APIs."""
    dr = _bootstrap_family()
    sibling_agents = importlib.import_module("design_research_agents")
    sibling_experiments = importlib.import_module("design_research_experiments")
    sibling_analysis = importlib.import_module("design_research_analysis")
    sibling_problems = importlib.import_module("design_research_problems")

    assert dr.__version__ == "0.4.0"
    assert {
        module.__name__: module.__version__
        for module in (
            sibling_problems,
            sibling_agents,
            sibling_experiments,
            sibling_analysis,
        )
    } == EXPECTED_VERSIONS
    assert dr.agents.__all__ == sibling_agents.__all__
    assert dr.experiments.__all__ == sibling_experiments.__all__
    assert dr.analysis.__all__ == sibling_analysis.__all__
    assert dr.problems.__all__ == sibling_problems.__all__
    assert dr.agents.Workflow is sibling_agents.Workflow
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
    assert dr.problems.__version__ == sibling_problems.__version__
    assert dr.problems.search_problem_summaries is sibling_problems.search_problem_summaries
    assert dr.analysis.compute_interrater_reliability is (
        sibling_analysis.compute_interrater_reliability
    )
    assert callable(dr.agents.MCPServerConfig.python_module)
    assert dr.experiments.__version__ == sibling_experiments.__version__


def test_family_interoperability_smoke(tmp_path: Path) -> None:
    """Run one packaged problem through the family stack and validate the artifact handoff."""
    dr = _bootstrap_family()
    problem_id = "gmpb_default_dynamic_min"
    baseline_agent_id = "SeededRandomBaselineAgent"

    study = dr.experiments.Study(
        study_id="umbrella-family-smoke",
        title="Umbrella family smoke",
        description="Exercise packaged problems, agents, experiments, and analysis together.",
        output_dir=tmp_path / "umbrella-family-smoke",
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

    report = dr.analysis.validate_experiment_events(exported["events.csv"])
    metric_rows = dr.analysis.build_condition_metric_table_from_artifacts(
        exported["events.csv"],
        metric="primary_outcome",
        condition_column="agent_id",
    )

    assert report.is_valid
    assert exported["manifest.json"].exists()
    manifest = json.loads(exported["manifest.json"].read_text(encoding="utf-8"))
    assert manifest["schema_version"] == "0.1.0"
    assert metric_rows
