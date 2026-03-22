"""Real runnable umbrella-stack interoperability example.

## Introduction
Run one packaged decision problem through the umbrella package, export the
canonical artifacts, and validate the resulting `events.csv` contract through
the analysis layer.

## Technical Implementation
1. Bootstrap sibling April workspaces when they are available locally.
2. Resolve a packaged decision problem into an explicit `ProblemPacket`.
3. Execute one deterministic baseline run, export artifacts, and validate the
   analysis handoff.

## Expected Results
The script prints the packaged problem identity, the seeded-baseline backend in
use, one successful run result, and the exported artifact filenames.
"""

from __future__ import annotations

import csv
import importlib
from pathlib import Path

from _stack_interop import (
    PORTABLE_BASELINE_AGENT_ID,
    build_problem_packet,
    make_portable_agent_factories,
    portable_agent_backend,
    run_study_compatible,
)
from _workspace_bootstrap import bootstrap_sibling_sources

bootstrap_sibling_sources()

dr = importlib.import_module("design_research")

PROBLEM_ID = "decision_laptop_design_profit_maximization"
STUDY_ID = "real_stack_interoperability"
OUTPUT_DIR = Path("artifacts") / "examples" / STUDY_ID


def _build_study() -> object:
    """Build one small umbrella study around a packaged decision problem."""
    return dr.experiments.Study(
        study_id=STUDY_ID,
        title="Real Stack Interoperability",
        description=(
            "Run one packaged decision problem through the umbrella stack with "
            "canonical artifact export and analysis validation."
        ),
        output_dir=OUTPUT_DIR,
        problem_ids=(PROBLEM_ID,),
        agent_specs=(PORTABLE_BASELINE_AGENT_ID,),
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


def main() -> None:
    """Run one real end-to-end interoperability path through the umbrella stack."""
    packaged_problem, problem_packet = build_problem_packet(dr, problem_id=PROBLEM_ID)
    study = _build_study()
    conditions = dr.experiments.build_design(study)
    run_results = run_study_compatible(
        dr,
        study=study,
        conditions=conditions,
        agent_factories=make_portable_agent_factories(dr),
        problem_registry={PROBLEM_ID: problem_packet},
    )
    exported_paths = dr.experiments.export_analysis_tables(
        study,
        conditions=conditions,
        run_results=run_results,
        output_dir=study.output_dir / "analysis",
        validate_with_analysis_package=True,
    )

    with exported_paths["events.csv"].open("r", encoding="utf-8", newline="") as file_obj:
        rows = list(csv.DictReader(file_obj))
    report = dr.analysis.validate_unified_table(dr.analysis.coerce_unified_table(rows))

    run_result = run_results[0]
    print("Problem ID:", packaged_problem.metadata.problem_id)
    print("Problem title:", packaged_problem.metadata.title)
    print("Problem family:", packaged_problem.metadata.kind.value)
    print("Agent backend:", portable_agent_backend(dr))
    print("Completed runs:", len(run_results))
    print("Run status:", run_result.status.value)
    print("Output keys:", ", ".join(sorted(run_result.outputs)))
    print("Primary outcome:", run_result.metrics.get("primary_outcome"))
    print("Event rows valid:", report.is_valid, f"(rows={report.n_rows})")
    print("Exported artifacts:", ", ".join(path.name for path in exported_paths.values()))


if __name__ == "__main__":
    main()
