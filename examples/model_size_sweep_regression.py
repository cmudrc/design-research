"""Sweep model sizes within one model class and regress outcomes."""

from __future__ import annotations

import math
import random
from pathlib import Path

import design_research as dr

STUDY_ID = "model_size_sweep_regression"
OUTPUT_DIR = Path("artifacts") / "examples" / STUDY_ID
PROBLEM_ID = "ideation_bicycle_safety_lock"
AGENT_ID = "scripted_model_family_agent"
PRIMARY_METRIC = "primary_outcome"
MODEL_SIZES_B = (1.5, 3.0, 7.0, 14.0)


def main() -> None:
    """Run a deterministic model-size sweep and fit an artifact-first regression."""
    problem = dr.problems.get_problem(PROBLEM_ID)
    study = dr.experiments.Study(
        study_id=STUDY_ID,
        title="Model Size Sweep Regression",
        description="Compare one model class across size tiers using canonical artifacts.",
        factors=(
            dr.experiments.Factor(
                name="model_size_b",
                description="Parameter count in billions for one model class.",
                dtype="float",
                levels=tuple(
                    dr.experiments.Level(name=f"{size:g}b", value=size) for size in MODEL_SIZES_B
                ),
            ),
        ),
        problem_ids=(PROBLEM_ID,),
        agent_specs=(AGENT_ID,),
        run_budget=dr.experiments.RunBudget(replicates=5, parallelism=1, max_runs=20),
        output_dir=OUTPUT_DIR,
    )
    conditions = dr.experiments.build_design(study)
    results = dr.experiments.run_study(
        study,
        conditions=conditions,
        agent_bindings={AGENT_ID: _sweep_agent},
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

    regression = dr.analysis.fit_regression_from_artifacts(
        artifacts["events.csv"],
        outcome=PRIMARY_METRIC,
        predictors=("model_size_b",),
    )
    run_rows = dr.analysis.build_run_metric_table_from_artifacts(
        artifacts["events.csv"],
        metrics=PRIMARY_METRIC,
        condition_columns=("model_size_b",),
    )
    validation = dr.analysis.validate_experiment_events(artifacts["events.csv"])

    print("Model size sweep regression:", study.study_id)
    print("Problem:", problem.metadata.title)
    print("Model class:", "scripted-open-class")
    print("Runs:", len(results))
    print("Event rows valid:", validation.is_valid, f"(rows={validation.n_rows})")
    print("Regression samples:", regression.n_samples)
    print("Coefficient model_size_b:", f"{regression.coefficients['model_size_b']:.4f}")
    print("R2:", f"{regression.r2:.3f}")
    print("Observed size tiers:", ", ".join(_observed_tiers(run_rows)))
    print("Artifacts directory:", artifacts["events.csv"].parent)


def _sweep_agent(
    *,
    condition: dr.experiments.Condition,
    problem_packet: dr.experiments.ProblemPacket,
    seed: int,
) -> dict[str, object]:
    """Generate one deterministic ideation result for a model-size condition."""
    size_b = float(condition.factor_assignments["model_size_b"])
    rng = random.Random(seed)
    noise = rng.uniform(-0.015, 0.015)
    score = 0.52 + (0.08 * math.log2(size_b + 1.0)) + noise
    events = [
        {
            "event_type": "inspect",
            "text": problem_packet.brief[:80],
            "meta_json": {"size_b": size_b},
        },
        {"event_type": "ideate", "text": f"draft concepts with {size_b:g}b model"},
        {"event_type": "select", "text": "select strongest safety-lock concept"},
    ]
    return {
        "output": {"text": f"{size_b:g}b concept set"},
        "metrics": {
            PRIMARY_METRIC: score,
            "input_tokens": 220 + int(size_b * 8),
            "output_tokens": 90 + int(size_b * 5),
            "cost_usd": round(size_b * 0.0004, 5),
        },
        "events": events,
        "metadata": {
            "agent_kind": "scripted",
            "model_name": f"scripted-open-class-{size_b:g}b",
            "pattern_name": "model-size-sweep",
        },
    }


def _observed_tiers(rows: list[dict[str, object]]) -> list[str]:
    """Return the sorted model-size tiers observed in artifact-derived rows."""
    tiers = sorted({float(row["model_size_b"]) for row in rows})
    return [f"{tier:g}b" for tier in tiers]


if __name__ == "__main__":
    main()
