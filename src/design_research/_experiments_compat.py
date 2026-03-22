"""Compatibility helpers for the umbrella experiments wrapper.

These helpers preserve runnable examples across sibling release boundaries
without adding new mandatory dependencies between the underlying libraries.
"""

from __future__ import annotations

import random
from collections.abc import Mapping
from typing import Any, cast

from . import problems

SEEDED_RANDOM_BASELINE_AGENT_ID = "SeededRandomBaselineAgent"


def resolve_problem(experiments_module: Any, *, problem_id: str) -> object:
    """Resolve one packaged problem through the sibling package or a local fallback."""
    library_helper = cast(Any, getattr(experiments_module, "resolve_problem", None))
    if callable(library_helper):
        return library_helper(problem_id)

    get_problem = cast(Any, problems.get_problem)
    problem = get_problem(problem_id)
    metadata = getattr(problem, "metadata", None)

    def evaluator(run_output: Mapping[str, Any]) -> Any:
        """Evaluate one candidate and normalize it to experiment rows."""
        candidate = run_output.get("candidate", run_output)
        return _normalize_evaluation_rows(problem.evaluate(candidate))

    problem_packet_cls = cast(Any, experiments_module.ProblemPacket)
    return problem_packet_cls(
        problem_id=str(getattr(metadata, "problem_id", problem_id)),
        family=str(getattr(getattr(metadata, "kind", None), "value", "unknown")),
        brief=_problem_brief(problem, fallback=str(getattr(metadata, "title", problem_id))),
        payload={"problem_object": problem},
        metadata={
            "title": str(getattr(metadata, "title", problem_id)),
            "summary": str(getattr(metadata, "summary", problem_id)),
            "capabilities": tuple(getattr(metadata, "capabilities", ())),
            "study_suitability": tuple(getattr(metadata, "study_suitability", ())),
        },
        evaluator=evaluator,
    )


def make_seeded_random_baseline_factories(experiments_module: Any) -> dict[str, Any]:
    """Return seeded-baseline factories from the sibling package or a local fallback."""
    library_helper = cast(
        Any,
        getattr(experiments_module, "make_seeded_random_baseline_factories", None),
    )
    if callable(library_helper):
        return cast(dict[str, Any], library_helper())

    def factory(_condition: object) -> Any:
        """Build one deterministic fallback baseline executor."""
        return _fallback_seeded_random_baseline

    return {SEEDED_RANDOM_BASELINE_AGENT_ID: factory}


def _fallback_seeded_random_baseline(
    *,
    problem_packet: Any,
    run_spec: Any,
    seed: int,
) -> dict[str, Any]:
    """Return one deterministic candidate when the sibling helper is unavailable."""
    payload = getattr(problem_packet, "payload", {})
    if not isinstance(payload, Mapping) or payload.get("problem_object") is None:
        raise RuntimeError(
            "Seeded random baseline fallback requires `problem_packet.payload['problem_object']`."
        )

    problem = payload["problem_object"]
    candidate = _sample_candidate(problem, seed=seed)
    return {
        "output": {"candidate": candidate},
        "events": [
            {
                "event_type": "baseline_candidate_selected",
                "actor_id": "agent",
                "text": "Generated one deterministic compatibility baseline candidate.",
                "meta_json": {
                    "agent_name": SEEDED_RANDOM_BASELINE_AGENT_ID,
                    "problem_id": getattr(problem_packet, "problem_id", "problem"),
                    "seed": seed,
                },
            }
        ],
        "metadata": {
            "agent_kind": "seeded_random_baseline",
            "request_id": getattr(run_spec, "run_id", ""),
        },
    }


def _problem_brief(problem: Any, *, fallback: str) -> str:
    """Return the richest available brief text for a packaged problem."""
    render_brief = getattr(problem, "render_brief", None)
    if callable(render_brief):
        rendered = render_brief()
        if rendered:
            return str(rendered)
    return fallback


def _sample_candidate(problem: Any, *, seed: int) -> Any:
    """Sample one deterministic candidate from a packaged problem object."""
    randomizer = random.Random(seed)

    option_factors = getattr(problem, "option_factors", None)
    if option_factors:
        return {
            str(factor.key): randomizer.choice(tuple(factor.levels))
            for factor in option_factors
            if getattr(factor, "key", None) is not None and tuple(getattr(factor, "levels", ()))
        }

    bounds = getattr(problem, "bounds", None)
    lower_bounds = getattr(bounds, "lb", None)
    upper_bounds = getattr(bounds, "ub", None)
    if lower_bounds is not None and upper_bounds is not None:
        return [
            randomizer.uniform(float(lower_bound), float(upper_bound))
            for lower_bound, upper_bound in zip(lower_bounds, upper_bounds, strict=False)
        ]

    raise RuntimeError(
        "Seeded random baseline compatibility fallback supports packaged decision "
        "problems with `option_factors` and optimization problems exposing bounds."
    )


def _normalize_evaluation_rows(evaluation: Any) -> list[dict[str, Any]]:
    """Convert packaged evaluation objects into canonical experiment rows."""
    objective_metric = str(getattr(evaluation, "objective_metric", "") or "objective_value")
    rows = [
        {
            "evaluator_id": "packaged_problem_evaluator",
            "metric_name": objective_metric,
            "metric_value": getattr(evaluation, "objective_value", None),
            "metric_unit": "unitless",
            "aggregation_level": "run",
            "notes_json": {
                "higher_is_better": bool(getattr(evaluation, "higher_is_better", True)),
            },
        }
    ]

    for metric_name, metric_unit in (
        ("predicted_share", "unitless"),
        ("expected_demand_units", "units"),
        ("utility", "unitless"),
        ("total_constraint_violation", "unitless"),
        ("max_constraint_violation", "unitless"),
        ("is_feasible", "boolean"),
    ):
        metric_value = getattr(evaluation, metric_name, None)
        if metric_value is None:
            continue
        rows.append(
            {
                "evaluator_id": "packaged_problem_evaluator",
                "metric_name": metric_name,
                "metric_value": metric_value,
                "metric_unit": metric_unit,
                "aggregation_level": "run",
                "notes_json": {},
            }
        )

    return rows


__all__ = [
    "SEEDED_RANDOM_BASELINE_AGENT_ID",
    "make_seeded_random_baseline_factories",
    "resolve_problem",
]
