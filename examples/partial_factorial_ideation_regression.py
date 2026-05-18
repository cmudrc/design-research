"""Run a partial factorial ideation study and fit a linear model."""

from __future__ import annotations

import random
from pathlib import Path

import design_research as dr

STUDY_ID = "partial_factorial_ideation_regression"
OUTPUT_DIR = Path("artifacts") / "examples" / STUDY_ID
AGENT_ID = "scripted_partial_factorial_ideator"
PRIMARY_METRIC = "primary_outcome"

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
    """Run a larger ideation DOE without touching the exported tables directly."""
    # Build the study separately from the condition matrix so the tutorial can
    # show both pieces of a custom design of experiments.
    study = _study()
    conditions = _partial_factorial_conditions()

    # The scripted agent keeps execution offline and deterministic, but it still
    # returns the same result shape expected from a live ideation agent.
    results = dr.experiments.run_study(
        study,
        conditions=conditions,
        agent_bindings={AGENT_ID: _ideation_agent},
        checkpoint=False,
        show_progress=False,
    )

    # Persist the standard artifacts before analysis. This keeps the example
    # aligned with a reproducible workflow where tables can be inspected later.
    artifacts = dr.experiments.export_analysis_tables(
        study,
        conditions=conditions,
        run_results=results,
        output_dir=study.output_dir / "analysis",
        validate_with_analysis_package=True,
    )

    # Fit a linear model from artifacts with both a numeric predictor and a
    # categorical task-family predictor. No user code touches the CSV tables.
    regression = dr.analysis.fit_regression_from_artifacts(
        artifacts["events.csv"],
        outcome=PRIMARY_METRIC,
        predictors=("model_size_b", "task_family"),
        categorical_predictors=("task_family",),
    )
    validation = dr.analysis.validate_experiment_events(artifacts["events.csv"])

    # Print the regression headline and validation status; the detailed rows stay
    # in the generated artifacts.
    print("Partial factorial ideation regression:", study.study_id)
    print("Conditions:", len(conditions))
    print("Runs:", len(results))
    print("Event rows valid:", validation.is_valid, f"(rows={validation.n_rows})")
    print("Regression samples:", regression.n_samples)
    print("Model size coefficient:", f"{regression.coefficients['model_size_b']:.4f}")
    print("Task family terms:", _task_terms(regression.coefficients))
    print("R2:", f"{regression.r2:.3f}")
    print("Artifacts directory:", artifacts["events.csv"].parent)


def _study() -> dr.experiments.Study:
    """Build the ideation study definition for the partial factorial design."""
    # The factor definitions describe the design space even though this example
    # samples only a partial matrix below.
    return dr.experiments.Study(
        study_id=STUDY_ID,
        title="Partial Factorial Ideation Regression",
        description="Sample model-size by design-task combinations and regress ideation quality.",
        factors=(
            dr.experiments.Factor(
                name="model_size_b",
                description="Parameter count in billions.",
                dtype="float",
                levels=tuple(
                    dr.experiments.Level(name=key, value=size)
                    for key, (_, size, _) in MODEL_LEVELS.items()
                ),
            ),
            dr.experiments.Factor(
                name="task_family",
                description="Ideation task family.",
                levels=tuple(
                    dr.experiments.Level(name=key, value=family)
                    for key, (_, family, _) in TASK_LEVELS.items()
                ),
            ),
        ),
        agent_specs=(AGENT_ID,),
        problem_ids=tuple(problem_id for problem_id, _, _ in TASK_LEVELS.values()),
        run_budget=dr.experiments.RunBudget(replicates=2, parallelism=1, max_runs=24),
        output_dir=OUTPUT_DIR,
    )


def _partial_factorial_conditions() -> list[dr.experiments.Condition]:
    """Materialize the explicit partial factorial condition matrix."""
    conditions = []

    # Spell out the partial factorial rows rather than generating a full cross
    # product. This is the pattern to use when the DOE is intentionally sparse.
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
    condition: dr.experiments.Condition,
    problem_packet: dr.experiments.ProblemPacket,
    seed: int,
) -> dict[str, object]:
    """Generate one deterministic ideation run for a model-task condition."""
    size_b = float(condition.factor_assignments["model_size_b"])
    model_name = str(condition.factor_assignments["model_name"])
    task_family = str(condition.factor_assignments["task_family"])

    # Each task family has a small deterministic offset so the regression has
    # categorical terms worth estimating.
    task_bonus = next(
        bonus
        for problem_id, family, bonus in TASK_LEVELS.values()
        if problem_id == problem_packet.problem_id and family == task_family
    )
    rng = random.Random(seed)
    score = 0.48 + (0.010 * size_b) + task_bonus + rng.uniform(-0.02, 0.02)

    # The event sequence resembles a lightweight ideation workflow. Analysis can
    # read these rows later without knowing how the scripted agent was written.
    events = [
        {"event_type": "inspect", "text": problem_packet.brief[:90]},
        {"event_type": "analogize", "text": f"look for {task_family} analogies"},
        {"event_type": "ideate", "text": f"{model_name} drafts alternatives"},
        {"event_type": "critique", "text": "score novelty and feasibility"},
        {"event_type": "select", "text": "select final concept"},
    ]

    # Let experiments build the standard custom-agent payload so this example
    # stays focused on the DOE, not return-shape plumbing.
    return dr.experiments.agent_result(
        f"{model_name} concept for {problem_packet.problem_id}",
        metrics={
            PRIMARY_METRIC: score,
            "input_tokens": 260 + int(size_b * 6),
            "output_tokens": 120 + int(size_b * 3),
            "cost_usd": round(size_b * 0.0005, 5),
        },
        events=events,
        metadata={
            "agent_kind": "scripted",
            "model_name": model_name,
            "pattern_name": "partial-factorial-ideation",
        },
    )


def _task_terms(coefficients: dict[str, float]) -> str:
    """Format the categorical task-family coefficient names."""
    terms = sorted(name for name in coefficients if name.startswith("task_family["))
    return ", ".join(terms)


if __name__ == "__main__":
    main()
