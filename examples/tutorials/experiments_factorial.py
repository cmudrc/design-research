"""Define and materialize a reproducible two-factor experiment."""

from __future__ import annotations

from pathlib import Path

import design_research_experiments as experiments

OUTPUT_DIR = Path("artifacts") / "tutorials" / "experiments_factorial"


def build_study() -> experiments.Study:
    """Build a small 2x2 factorial study definition."""
    return experiments.Study(
        study_id="prompt-layout-factorial",
        title="Prompt and Layout Factorial",
        description="Compare two prompt frames across two design representations.",
        factors=(
            experiments.Factor(
                name="prompt_frame",
                description="How the design task is framed.",
                levels=(
                    experiments.Level(name="neutral", value="neutral"),
                    experiments.Level(name="challenge", value="challenge"),
                ),
            ),
            experiments.Factor(
                name="representation",
                description="Representation available to the participant.",
                levels=(
                    experiments.Level(name="text", value="text"),
                    experiments.Level(name="sketch", value="sketch"),
                ),
            ),
        ),
        outcomes=(
            experiments.OutcomeSpec(
                name="quality",
                source_table="runs",
                column="quality",
                aggregation="mean",
                primary=True,
            ),
        ),
        run_budget=experiments.RunBudget(replicates=3, parallelism=1, max_runs=12),
        seed_policy=experiments.SeedPolicy(base_seed=42),
        output_dir=OUTPUT_DIR,
        problem_ids=("local_design_brief",),
        agent_specs=("participant",),
        primary_outcomes=("quality",),
    )


def main() -> None:
    """Validate, materialize, and serialize the tutorial study."""
    study = build_study()
    errors = experiments.validate_study(study)
    if errors:
        raise RuntimeError("\n".join(errors))

    conditions = experiments.build_design(study)
    definition_path = study.to_json(OUTPUT_DIR / "study.json")
    first_seed = study.seed_policy.derive_seed(
        study.study_id,
        conditions[0].condition_id,
        replicate=0,
    )

    print("Study valid:", not errors)
    print("Conditions:", len(conditions))
    print("Planned runs:", len(conditions) * study.run_budget.replicates)
    for condition in conditions:
        print(
            "-",
            condition.factor_assignments["prompt_frame"],
            "/",
            condition.factor_assignments["representation"],
        )
    print("First run seed:", first_seed)
    print("Study definition:", definition_path)


if __name__ == "__main__":
    main()
