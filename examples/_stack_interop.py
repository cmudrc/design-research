"""Portable helpers for runnable umbrella interoperability examples."""

from __future__ import annotations

import inspect
import random
from collections.abc import Mapping, Sequence
from typing import Any

import numpy as np

PORTABLE_BASELINE_AGENT_ID = "SeededRandomBaselineAgent"


def public_seeded_baseline_available(dr: Any) -> bool:
    """Return whether the umbrella wrapper exposes the seeded baseline agent."""
    return callable(getattr(dr.agents, PORTABLE_BASELINE_AGENT_ID, None))


def portable_agent_backend(dr: Any) -> str:
    """Describe which seeded-baseline backend the examples will use."""
    if public_seeded_baseline_available(dr):
        return "public_seeded_random_baseline"
    return "portable_example_fallback"


def build_problem_packet(dr: Any, *, problem_id: str) -> tuple[Any, Any]:
    """Resolve one packaged problem and wrap it as a portable `ProblemPacket`."""
    problem = dr.problems.get_problem(problem_id)
    metadata = getattr(problem, "metadata", None)
    family = _problem_family(problem)
    brief = _problem_brief(problem, fallback=str(getattr(metadata, "title", problem_id)))

    def evaluator(run_output: Mapping[str, Any]) -> list[dict[str, Any]]:
        """Evaluate one normalized run output against the packaged problem."""
        candidate = _extract_candidate(run_output)
        evaluation = _evaluate_problem(problem, candidate)
        return _normalize_evaluation_rows(evaluation)

    packet = dr.experiments.ProblemPacket(
        problem_id=str(getattr(metadata, "problem_id", problem_id)),
        family=family,
        brief=brief,
        payload={"problem_object": problem},
        metadata={
            "problem_class": problem.__class__.__name__,
            "title": str(getattr(metadata, "title", problem_id)),
            "summary": str(getattr(metadata, "summary", brief)),
            "capabilities": tuple(getattr(metadata, "capabilities", ())),
            "study_suitability": tuple(getattr(metadata, "study_suitability", ())),
        },
        evaluator=evaluator,
    )
    return problem, packet


def make_portable_agent_factories(dr: Any) -> dict[str, Any]:
    """Return agent factories that work on both released and April stack versions."""

    def factory(_condition: object) -> Any:
        """Build one executable seeded-baseline adapter for a study condition."""

        def execute_portable_agent(
            problem_packet: Any | None = None,
            problem: Any | None = None,
            brief: str | None = None,
            run_spec: Any | None = None,
            condition: Any | None = None,
            seed: int | None = None,
            prompt: Any | None = None,
            input: Any | None = None,
            request_id: str | None = None,
            dependencies: Mapping[str, object] | None = None,
        ) -> dict[str, Any]:
            """Execute one portable seeded-baseline run and normalize the result."""
            del condition

            resolved_problem = _problem_from_inputs(problem_packet=problem_packet, problem=problem)
            resolved_seed = _seed_from_inputs(
                seed=seed,
                run_spec=run_spec,
                dependencies=dependencies,
            )
            resolved_request_id = _request_id_from_inputs(
                request_id=request_id,
                run_spec=run_spec,
            )
            prompt_text = _prompt_from_inputs(
                prompt=prompt,
                input_value=input,
                brief=brief,
                problem_packet=problem_packet,
                problem=resolved_problem,
            )
            resolved_dependencies = _dependencies_from_inputs(
                problem_packet=problem_packet,
                problem=resolved_problem,
                run_spec=run_spec,
                seed=resolved_seed,
                dependencies=dependencies,
            )

            public_agent_ctor = getattr(dr.agents, PORTABLE_BASELINE_AGENT_ID, None)
            if callable(public_agent_ctor):
                public_agent = public_agent_ctor()
                raw_result = public_agent.run(
                    prompt_text,
                    request_id=resolved_request_id,
                    dependencies=resolved_dependencies,
                )
                return _normalize_public_agent_result(
                    raw_result,
                    backend=portable_agent_backend(dr),
                    seed=resolved_seed,
                )

            if resolved_problem is None:
                raise RuntimeError("Portable baseline fallback requires a packaged problem object.")

            return _fallback_agent_result(
                problem=resolved_problem,
                seed=resolved_seed,
                backend=portable_agent_backend(dr),
            )

        return execute_portable_agent

    return {PORTABLE_BASELINE_AGENT_ID: factory}


def run_study_compatible(
    dr: Any,
    *,
    study: Any,
    conditions: Sequence[Any],
    agent_factories: Mapping[str, Any],
    problem_registry: Mapping[str, Any],
) -> list[Any]:
    """Run one study while tolerating pre-April and April runner signatures."""
    kwargs: dict[str, Any] = {
        "conditions": conditions,
        "agent_factories": agent_factories,
        "problem_registry": problem_registry,
    }
    if "show_progress" in inspect.signature(dr.experiments.run_study).parameters:
        kwargs["show_progress"] = False
    return list(dr.experiments.run_study(study, **kwargs))


def _problem_family(problem: Any) -> str:
    """Return the best available packaged-problem family label."""
    metadata = getattr(problem, "metadata", None)
    kind = getattr(getattr(metadata, "kind", None), "value", None)
    if kind is not None:
        return str(kind)
    family = getattr(problem, "family", None)
    if family is not None:
        return str(family)
    return problem.__class__.__name__


def _problem_brief(problem: Any, *, fallback: str) -> str:
    """Return one markdown brief when the packaged problem exposes it."""
    render_brief = getattr(problem, "render_brief", None)
    if callable(render_brief):
        rendered = render_brief()
        if rendered:
            return str(rendered)
    brief = getattr(problem, "brief", None)
    if brief:
        return str(brief)
    prompt = getattr(problem, "prompt", None)
    if prompt:
        return str(prompt)
    return fallback


def _problem_from_inputs(*, problem_packet: Any | None, problem: Any | None) -> Any | None:
    """Resolve the native packaged problem object from adapter inputs."""
    if problem is not None and not _looks_like_problem_packet(problem):
        return problem
    if problem_packet is None:
        return None
    payload = getattr(problem_packet, "payload", {})
    if isinstance(payload, Mapping):
        return payload.get("problem_object")
    return None


def _seed_from_inputs(
    *,
    seed: int | None,
    run_spec: Any | None,
    dependencies: Mapping[str, object] | None,
) -> int:
    """Resolve one deterministic seed from all supported call conventions."""
    if seed is not None:
        return int(seed)
    if dependencies is not None and "seed" in dependencies:
        return int(dependencies["seed"])
    if run_spec is not None and hasattr(run_spec, "seed"):
        return int(run_spec.seed)
    return 0


def _request_id_from_inputs(*, request_id: str | None, run_spec: Any | None) -> str | None:
    """Resolve one stable request id for public agent calls."""
    if request_id:
        return request_id
    if run_spec is not None and hasattr(run_spec, "run_id"):
        return str(run_spec.run_id)
    return None


def _prompt_from_inputs(
    *,
    prompt: Any | None,
    input_value: Any | None,
    brief: str | None,
    problem_packet: Any | None,
    problem: Any | None,
) -> str:
    """Render one prompt string for public agent implementations."""
    for value in (prompt, input_value, brief):
        if isinstance(value, str) and value.strip():
            return value
    if problem is not None:
        rendered = _problem_brief(problem, fallback="")
        if rendered:
            return rendered
    if problem_packet is not None and hasattr(problem_packet, "brief"):
        return str(problem_packet.brief)
    return "Generate one candidate for the packaged problem."


def _dependencies_from_inputs(
    *,
    problem_packet: Any | None,
    problem: Any | None,
    run_spec: Any | None,
    seed: int,
    dependencies: Mapping[str, object] | None,
) -> dict[str, object]:
    """Build the dependency payload shared with public April agents."""
    resolved = dict(dependencies or {})
    if problem_packet is not None:
        resolved.setdefault("problem_packet", problem_packet)
    if problem is not None:
        resolved.setdefault("problem", problem)
    if run_spec is not None:
        resolved.setdefault("run_spec", run_spec)
    resolved.setdefault("seed", seed)
    return resolved


def _normalize_public_agent_result(raw_result: Any, *, backend: str, seed: int) -> dict[str, Any]:
    """Normalize a public April `ExecutionResult` into released-runner shape."""
    raw_output = getattr(raw_result, "output", {})
    output_mapping = dict(raw_output) if isinstance(raw_output, Mapping) else {}
    raw_metadata = getattr(raw_result, "metadata", {})
    metadata = dict(raw_metadata) if isinstance(raw_metadata, Mapping) else {}

    final_output = getattr(raw_result, "final_output", None)
    if final_output is None:
        final_output = output_mapping.get("final_output")
    output = _normalize_output_mapping(
        final_output,
        output_mapping=output_mapping,
        metadata=metadata,
    )

    metrics: dict[str, Any] = {}
    if isinstance(output_mapping.get("metrics"), Mapping):
        metrics.update(dict(output_mapping["metrics"]))

    preview = metadata.get("preview_evaluation")
    if isinstance(preview, Mapping):
        for key in (
            "objective_value",
            "total_constraint_violation",
            "max_constraint_violation",
            "predicted_share",
            "expected_demand_units",
            "utility",
            "higher_is_better",
        ):
            if key in preview and key not in metrics:
                metrics[key] = preview[key]

    raw_events = output_mapping.get("events", ())
    events = [dict(event) for event in raw_events if isinstance(event, Mapping)]

    trace_refs: list[str] = []
    for attribute in ("trace_path", "trace_dir"):
        value = getattr(raw_result, attribute, None)
        if value:
            trace_refs.append(str(value))

    metadata.setdefault("backend", backend)
    metadata.setdefault("seed", seed)
    return {
        "output": output,
        "metrics": metrics,
        "events": events,
        "metadata": metadata,
        "trace_refs": trace_refs,
    }


def _normalize_output_mapping(
    final_output: Any,
    *,
    output_mapping: Mapping[str, Any],
    metadata: Mapping[str, Any],
) -> dict[str, Any]:
    """Normalize candidate output from a public April `ExecutionResult`."""
    if isinstance(final_output, Mapping):
        return dict(final_output)
    if isinstance(final_output, Sequence) and not isinstance(final_output, (str, bytes)):
        return {"candidate": list(final_output)}
    if "candidate" in output_mapping:
        return {"candidate": output_mapping["candidate"]}
    if "candidate" in metadata:
        return {"candidate": metadata["candidate"]}
    if final_output is not None:
        return {"value": final_output}
    return {}


def _fallback_agent_result(*, problem: Any, seed: int, backend: str) -> dict[str, Any]:
    """Run a deterministic local fallback when the public baseline is unavailable."""
    candidate = _sample_candidate(problem, seed=seed)
    evaluation = _evaluate_problem(problem, candidate)
    metrics = _metrics_from_evaluation(evaluation)
    family = _problem_family(problem)
    return {
        "output": {"candidate": candidate},
        "metrics": metrics,
        "events": [
            {
                "event_type": "baseline_candidate_selected",
                "actor_id": "agent",
                "text": "Generated one deterministic example fallback candidate.",
                "meta_json": {"backend": backend, "family": family, "seed": seed},
            },
            {
                "event_type": "baseline_candidate_evaluated",
                "actor_id": "system",
                "text": "Evaluated the fallback candidate before returning it to the study runner.",
                "meta_json": metrics,
            },
        ],
        "metadata": {
            "agent_name": PORTABLE_BASELINE_AGENT_ID,
            "backend": backend,
            "seed": seed,
            "family": family,
        },
    }


def _sample_candidate(problem: Any, *, seed: int) -> Any:
    """Sample one deterministic candidate from packaged problem structure."""
    randomizer = random.Random(seed)

    option_factors = getattr(problem, "option_factors", None)
    if option_factors:
        candidate: dict[str, Any] = {}
        for factor in option_factors:
            levels = tuple(getattr(factor, "levels", ()))
            if not levels:
                continue
            candidate[str(factor.key)] = randomizer.choice(levels)
        if candidate:
            return candidate

    bounds = getattr(problem, "bounds", None)
    if bounds is not None:
        lower = np.asarray(bounds.lb, dtype=float)
        upper = np.asarray(bounds.ub, dtype=float)
        return [
            randomizer.uniform(float(lower[index]), float(upper[index]))
            for index in range(len(lower))
        ]

    raise RuntimeError("Portable baseline fallback does not know how to sample this problem.")


def _extract_candidate(run_output: Any) -> Any:
    """Extract the candidate payload from normalized run output."""
    if isinstance(run_output, Mapping):
        if "candidate" in run_output:
            return run_output["candidate"]
        final_output = run_output.get("final_output")
        if isinstance(final_output, Mapping) and "candidate" in final_output:
            return final_output["candidate"]
    return run_output


def _evaluate_problem(problem: Any, candidate: Any) -> Any:
    """Evaluate one candidate against a packaged problem object."""
    option_factors = getattr(problem, "option_factors", None)
    if option_factors:
        if not isinstance(candidate, Mapping):
            raise TypeError("Expected a mapping candidate for a decision problem.")
        normalized_candidate = {str(key): value for key, value in candidate.items()}
        return problem.evaluate(normalized_candidate)

    bounds = getattr(problem, "bounds", None)
    if bounds is not None:
        if isinstance(candidate, Mapping):
            if "candidate" in candidate:
                candidate = candidate["candidate"]
            elif "x" in candidate:
                candidate = candidate["x"]
        return problem.evaluate(np.asarray(candidate, dtype=float))

    return problem.evaluate(candidate)


def _metrics_from_evaluation(evaluation: Any) -> dict[str, Any]:
    """Extract preview metrics from one packaged-problem evaluation object."""
    metrics = {
        "objective_value": float(getattr(evaluation, "objective_value", 0.0) or 0.0),
        "higher_is_better": bool(getattr(evaluation, "higher_is_better", True)),
    }
    for key in (
        "predicted_share",
        "expected_demand_units",
        "utility",
        "total_constraint_violation",
        "max_constraint_violation",
    ):
        value = _numeric_metric(getattr(evaluation, key, None))
        if value is not None:
            metrics[key] = value

    is_feasible = getattr(evaluation, "is_feasible", None)
    if isinstance(is_feasible, bool):
        metrics["is_feasible"] = float(is_feasible)
    return metrics


def _normalize_evaluation_rows(evaluation: Any) -> list[dict[str, Any]]:
    """Convert packaged problem evaluations into canonical experiment rows."""
    objective_metric = str(getattr(evaluation, "objective_metric", "") or "objective_value")
    objective_value = float(getattr(evaluation, "objective_value", 0.0) or 0.0)
    notes_json: dict[str, Any] = {
        "higher_is_better": bool(getattr(evaluation, "higher_is_better", True)),
    }
    candidate_label = getattr(evaluation, "candidate_label", None)
    if candidate_label:
        notes_json["candidate_label"] = str(candidate_label)

    rows = [
        {
            "evaluator_id": "packaged_problem_evaluator",
            "metric_name": objective_metric,
            "metric_value": objective_value,
            "metric_unit": "unitless",
            "aggregation_level": "run",
            "notes_json": dict(notes_json),
        }
    ]

    for metric_name, metric_unit in (
        ("predicted_share", "unitless"),
        ("expected_demand_units", "units"),
        ("utility", "unitless"),
        ("total_constraint_violation", "unitless"),
        ("max_constraint_violation", "unitless"),
    ):
        metric_value = _numeric_metric(getattr(evaluation, metric_name, None))
        if metric_value is None:
            continue
        rows.append(
            {
                "evaluator_id": "packaged_problem_evaluator",
                "metric_name": metric_name,
                "metric_value": metric_value,
                "metric_unit": metric_unit,
                "aggregation_level": "run",
                "notes_json": dict(notes_json),
            }
        )

    is_feasible = getattr(evaluation, "is_feasible", None)
    if isinstance(is_feasible, bool):
        rows.append(
            {
                "evaluator_id": "packaged_problem_evaluator",
                "metric_name": "is_feasible",
                "metric_value": float(is_feasible),
                "metric_unit": "boolean-as-float",
                "aggregation_level": "run",
                "notes_json": dict(notes_json),
            }
        )

    return rows


def _numeric_metric(value: Any) -> float | None:
    """Convert supported scalar metric values to float."""
    if value is None:
        return None
    if isinstance(value, bool):
        return float(value)
    if isinstance(value, (int, float)):
        return float(value)
    return None


def _looks_like_problem_packet(value: Any) -> bool:
    """Return whether an object is likely the experiments `ProblemPacket`."""
    return all(hasattr(value, attribute) for attribute in ("problem_id", "family", "brief"))


__all__ = [
    "PORTABLE_BASELINE_AGENT_ID",
    "build_problem_packet",
    "make_portable_agent_factories",
    "portable_agent_backend",
    "public_seeded_baseline_available",
    "run_study_compatible",
]
