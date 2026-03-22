"""Authentic student laptop design study for the umbrella package."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

from _future_stack import (
    artifact_names,
    bootstrap_future_stack,
    make_delegate_agent_factory,
    require_future_apis,
    validate_exported_events,
)

# Pull the sibling repositories onto `sys.path` when they are available locally.
# This lets the example target the upcoming APIs directly instead of waiting for
# the next packaged releases.
bootstrap_future_stack()

# Import the umbrella package only after the bootstrap hook has had a chance to
# expose those sibling worktrees.
import design_research as dr  # noqa: E402

# Keep the packaged benchmark id, output location, and agent id as module-level
# constants so readers can see the moving pieces without digging through the
# implementation first.
PROBLEM_ID = "decision_laptop_design_profit_maximization"
STUDY_ID = "student_laptop_design_study"
OUTPUT_DIR = Path("artifacts") / "examples" / STUDY_ID
SUMMARY_REPORT_NAME = "student_laptop_design_summary.md"
BASELINE_AGENT_ID = "seeded_random_baseline"


def main() -> None:
    """Run one authentic laptop-design benchmark and print its observed results."""
    # Refuse to continue if the environment still points at older sibling APIs.
    # These refreshed examples are intentionally future-first.
    require_future_apis(dr)

    # Load the packaged problem so the summary can use the real benchmark title
    # and factor labels rather than only the internal problem id.
    problem = dr.problems.get_problem(PROBLEM_ID)

    # Define the single comparison arm inline so the script reads top to bottom
    # like a walkthrough rather than sending readers into helper functions.
    comparison_factor = dr.experiments.Factor(
        name="agent_id",
        description="Agent runtime binding used for the packaged decision benchmark.",
        kind=dr.experiments.FactorKind.MANIPULATED,
        levels=(
            dr.experiments.Level(
                name=BASELINE_AGENT_ID,
                value=BASELINE_AGENT_ID,
                label="Seeded random baseline",
                metadata={"role": "baseline", "is_baseline": True},
            ),
        ),
        metadata={"comparison_axis": True},
    )

    # Build the study directly in the script so each recipe setting is visible
    # exactly where the example is introduced.
    study = dr.experiments.build_strategy_comparison_study(
        dr.experiments.StrategyComparisonConfig(
            study_id=STUDY_ID,
            title="Student Laptop Design Study",
            description=(
                "Run a real student laptop design benchmark through the recipe-first umbrella "
                "stack and report the evaluator's observed market metrics."
            ),
            comparison_factor=comparison_factor,
            problem_ids=(PROBLEM_ID,),
            run_budget=dr.experiments.RunBudget(replicates=1, parallelism=1, max_runs=1),
            output_dir=OUTPUT_DIR,
        )
    )

    # Materialize the study design so `run_study(...)` has the concrete
    # condition rows it should execute.
    conditions = dr.experiments.build_design(study)

    # Run the study with a single baseline agent. The helper bridge adapts a
    # design-research-agents delegate into the experiments package's
    # `agent_factories` contract so the example can stay concise.
    results = dr.experiments.run_study(
        study,
        conditions=conditions,
        agent_factories={
            BASELINE_AGENT_ID: make_delegate_agent_factory(
                lambda: dr.agents.SeededRandomBaselineAgent(seed=7)
            )
        },
        # Resolve the packaged problem once up front. The future-state path is
        # that packaged problems flow straight through the umbrella without any
        # hand-built `ProblemPacket` boilerplate in the example itself.
        problem_registry={PROBLEM_ID: dr.experiments.resolve_problem(PROBLEM_ID)},
        checkpoint=False,
        show_progress=False,
    )

    # Export the canonical analysis tables that downstream reporting and
    # statistics tools consume.
    artifact_paths = dr.experiments.export_analysis_tables(
        study,
        conditions=conditions,
        run_results=results,
        output_dir=study.output_dir / "analysis",
    )

    # Sanity-check that the unified event export is structurally valid before we
    # tell readers to trust the generated artifacts.
    validation_report = validate_exported_events(dr, artifact_paths)

    # Write one human-readable markdown summary next to the raw CSV artifacts.
    summary_path = dr.experiments.write_markdown_report(
        study.output_dir,
        SUMMARY_REPORT_NAME,
        dr.experiments.render_markdown_summary(study, results),
    )

    # Pull out the only run result so the final console summary can mention its
    # status and primary metric directly.
    run_result = results[0]

    # Convert the evaluator rows into a simpler mapping so the printed summary
    # can refer to the metrics by name.
    evaluator_metrics: dict[str, object] = {}
    for row in getattr(run_result, "evaluator_outputs", ()) or ():
        if not isinstance(row, Mapping):
            continue
        name = row.get("metric_name")
        if name is not None:
            evaluator_metrics[str(name)] = row.get("metric_value")

    # Walk the packaged problem's factor metadata to turn the chosen candidate
    # into user-facing lines such as LCD size and battery life.
    candidate = run_result.outputs if isinstance(run_result.outputs, Mapping) else {}
    chosen_design_lines: list[str] = []
    for factor in getattr(problem, "option_factors", ()):
        key = str(getattr(factor, "key", ""))
        label = str(getattr(factor, "label", key))
        if key not in candidate:
            continue
        value = candidate[key]
        if label == "Price / 100":
            chosen_design_lines.append(f"{label}: {value} (${float(value) * 100:.0f})")
        else:
            chosen_design_lines.append(f"{label}: {value}")

    # Print a study summary that names the real application, the chosen laptop
    # configuration, and the evaluator's observed outcomes.
    print("Study:", study.study_id)
    print("Application:", problem.metadata.title)
    print("Problem ID:", PROBLEM_ID)
    print("Conditions:", len(conditions))
    print("Runs:", len(results), f"({run_result.status.value})")
    print("Chosen design:")
    for line in chosen_design_lines:
        print(f"- {line}")
    print("Observed results:")
    print(f"- market_share_proxy={float(evaluator_metrics.get('market_share_proxy', 0.0)):.4f}")
    print(
        f"- expected_demand_units={float(evaluator_metrics.get('expected_demand_units', 0.0)):.0f}"
    )
    print(f"- utility={float(evaluator_metrics.get('utility', 0.0)):.3f}")
    print(f"- primary_outcome={float(run_result.metrics.get('primary_outcome', 0.0)):.4f}")
    print("Event rows valid:", validation_report.is_valid, f"(rows={validation_report.n_rows})")
    print("Summary report:", summary_path.name)
    print("Artifacts:", artifact_names(artifact_paths))


if __name__ == "__main__":
    main()
