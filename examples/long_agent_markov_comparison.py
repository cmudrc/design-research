"""Compare long agent process traces as condition-specific Markov chains."""

from __future__ import annotations

import random
from collections.abc import Mapping
from pathlib import Path
from statistics import mean

import design_research as dr

STUDY_ID = "long_agent_markov_comparison"
OUTPUT_DIR = Path("artifacts") / "examples" / STUDY_ID
PROBLEM_ID = "ideation_accessible_drinking_fountain"
BASELINE_AGENT = "baseline_agent"
PLANNER_AGENT = "planner_agent"
ACTION_COUNT = 30
PRIMARY_METRIC = "primary_outcome"

TRANSITIONS = {
    BASELINE_AGENT: {
        "inspect": ("sketch", "retrieve", "sketch", "critique"),
        "retrieve": ("sketch", "inspect", "sketch", "revise"),
        "sketch": ("sketch", "critique", "revise", "select"),
        "critique": ("revise", "sketch", "select", "inspect"),
        "revise": ("sketch", "critique", "select", "sketch"),
        "select": ("sketch", "critique", "inspect", "select"),
    },
    PLANNER_AGENT: {
        "inspect": ("retrieve", "retrieve", "sketch", "critique"),
        "retrieve": ("sketch", "critique", "sketch", "revise"),
        "sketch": ("critique", "revise", "critique", "select"),
        "critique": ("revise", "retrieve", "revise", "select"),
        "revise": ("critique", "select", "select", "sketch"),
        "select": ("inspect", "retrieve", "critique", "select"),
    },
}


def main() -> None:
    """Run two agent treatments, then compare their transition matrices."""
    # The problem package supplies the real design-task context. The agents below
    # stay scripted so the example can focus on process traces and analysis.
    problem = dr.problems.get_problem(PROBLEM_ID)

    # Both treatments get the same action vocabulary and run budget. Only the
    # transition tendencies differ, which makes the Markov comparison meaningful.
    study = dr.experiments.Study(
        study_id=STUDY_ID,
        title="Long Agent Markov Comparison",
        description=(
            "Run long synthetic traces with the same action vocabulary and compare "
            "condition-specific Markov-chain matrices from exported artifacts."
        ),
        factors=(
            dr.experiments.Factor(
                name="agent_id",
                description="Agent process treatment.",
                levels=(
                    dr.experiments.Level(name=BASELINE_AGENT, value=BASELINE_AGENT),
                    dr.experiments.Level(name=PLANNER_AGENT, value=PLANNER_AGENT),
                ),
            ),
        ),
        problem_ids=(PROBLEM_ID,),
        run_budget=dr.experiments.RunBudget(replicates=10, parallelism=1, max_runs=20),
        output_dir=OUTPUT_DIR,
    )

    # Build the condition table and bind each agent id to the same callable. The
    # callable reads the condition to choose the scripted transition policy.
    conditions = dr.experiments.build_design(study)
    results = dr.experiments.run_study(
        study,
        conditions=conditions,
        agent_bindings={BASELINE_AGENT: _agent_run, PLANNER_AGENT: _agent_run},
        checkpoint=False,
        show_progress=False,
    )

    # Export the run history as canonical artifacts. From this point on, the
    # analysis code works from files rather than the in-memory run objects.
    artifacts = dr.experiments.export_analysis_tables(
        study,
        conditions=conditions,
        run_results=results,
        output_dir=study.output_dir / "analysis",
        validate_with_analysis_package=True,
    )

    # Fit one Markov chain per treatment from event sequences, then compare the
    # transition matrices directly from the same event artifact.
    chains = dr.analysis.fit_markov_chains_from_artifacts(
        artifacts["events.csv"],
        condition_column="agent_id",
        session_column="run_id",
    )
    comparison = dr.analysis.compare_markov_chains_from_artifacts(
        artifacts["events.csv"],
        condition_column="agent_id",
        left_condition=PLANNER_AGENT,
        right_condition=BASELINE_AGENT,
        session_column="run_id",
    )

    # Outcome metrics use the same artifact-first path, so process analysis and
    # score summaries come from a single exported contract.
    metric_rows = dr.analysis.build_condition_metric_table_from_artifacts(
        artifacts["events.csv"],
        metric=PRIMARY_METRIC,
        condition_column="agent_id",
    )
    validation = dr.analysis.validate_experiment_events(artifacts["events.csv"])

    means = _means_by_condition(metric_rows)

    # The printout is intentionally brief: headline process comparison, outcome
    # means, and the artifact directory for deeper inspection.
    print("Long agent Markov comparison:", study.study_id)
    print("Problem:", problem.metadata.title)
    print("Actions per run:", ACTION_COUNT)
    print("Runs:", len(results))
    print("Event rows valid:", validation.is_valid, f"(rows={validation.n_rows})")
    print("States:", len(chains[PLANNER_AGENT].states))
    print("Mean primary_outcome:")
    for agent_id in (BASELINE_AGENT, PLANNER_AGENT):
        print(f"- {agent_id}: {means[agent_id]:.3f}")
    print("Transition matrix delta:", f"{comparison.estimate:.4f}")
    if comparison.p_value is not None:
        print("Transition matrix p-value:", f"{comparison.p_value:.4f}")
    print("Artifacts directory:", artifacts["events.csv"].parent)


def _agent_run(
    *,
    condition: dr.experiments.Condition,
    problem_packet: dr.experiments.ProblemPacket,
    seed: int,
) -> dict[str, object]:
    """Generate one deterministic long agent trace for a treatment condition."""
    agent_id = str(condition.factor_assignments["agent_id"])
    rng = random.Random(seed)
    action = "inspect"
    events = []

    # Emit a long sequence of canonical events. Each event type is also a Markov
    # state, which lets analysis reconstruct transition counts without adapters.
    for step in range(1, ACTION_COUNT + 1):
        action = rng.choice(TRANSITIONS[agent_id][action])
        events.append(
            {
                "event_type": action,
                "actor_id": "agent",
                "text": f"{action} step for {problem_packet.problem_id}",
                "step_id": f"step-{step:02d}",
                "meta_json": {"step": step},
            }
        )

    score = _score_events(events, agent_id=agent_id)

    # Let experiments build the standard custom-agent payload so readers do not
    # have to memorize the raw return keys.
    return dr.experiments.agent_result(
        f"{agent_id} final concept score {score:.3f}",
        metrics={
            PRIMARY_METRIC: score,
            "input_tokens": 180 + ACTION_COUNT,
            "output_tokens": 90 + (2 * ACTION_COUNT),
        },
        events=events,
        metadata={
            "agent_kind": "scripted",
            "model_name": agent_id,
            "pattern_name": "long-process-trace",
        },
    )


def _score_events(events: list[Mapping[str, object]], *, agent_id: str) -> float:
    """Compute a simple outcome from the trace structure and treatment."""
    actions = [str(event["event_type"]) for event in events]
    deliberate_moves = (
        actions.count("retrieve") + actions.count("critique") + actions.count("revise")
    )
    selection_bonus = 0.04 * actions[-6:].count("select")
    treatment_bonus = 0.10 if agent_id == PLANNER_AGENT else 0.0
    return 0.45 + (0.012 * deliberate_moves) + selection_bonus + treatment_bonus


def _means_by_condition(rows: list[dict[str, object]]) -> dict[str, float]:
    """Summarize the artifact-derived condition metric rows."""
    grouped: dict[str, list[float]] = {}
    for row in rows:
        grouped.setdefault(str(row["condition"]), []).append(float(row["value"]))
    return {condition: mean(values) for condition, values in grouped.items()}


if __name__ == "__main__":
    main()
