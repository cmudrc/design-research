"""Build and run a deterministic workflow without an LLM service."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

import design_research_agents as agents


def scale_scores(context: Mapping[str, object]) -> dict[str, object]:
    """Scale the input scores in the first workflow step."""
    inputs = context.get("inputs")
    if not isinstance(inputs, Mapping):
        raise ValueError("Workflow inputs are missing.")
    scores = inputs.get("scores")
    scale = inputs.get("scale")
    if not isinstance(scores, Sequence) or isinstance(scores, str | bytes):
        raise ValueError("scores must be a sequence.")
    if not isinstance(scale, int | float):
        raise ValueError("scale must be numeric.")
    return {"scaled_scores": [float(score) * float(scale) for score in scores]}


def summarize_scores(context: Mapping[str, object]) -> dict[str, object]:
    """Summarize the first step's output in a dependent workflow step."""
    dependency_results = context.get("dependency_results")
    if not isinstance(dependency_results, Mapping):
        raise ValueError("Dependency results are missing.")
    prepared = dependency_results.get("scale_scores")
    if not isinstance(prepared, Mapping):
        raise ValueError("scale_scores did not produce a result.")
    output = prepared.get("output")
    if not isinstance(output, Mapping):
        raise ValueError("scale_scores output is missing.")
    scaled_scores = output.get("scaled_scores")
    if not isinstance(scaled_scores, list):
        raise ValueError("scaled_scores output is missing.")
    return {
        "count": len(scaled_scores),
        "mean": sum(float(score) for score in scaled_scores) / len(scaled_scores),
    }


def main() -> None:
    """Execute a two-step workflow and print its observable contract."""
    workflow = agents.Workflow(
        input_schema={
            "type": "object",
            "required": ["scores", "scale"],
        },
        steps=(
            agents.LogicStep(step_id="scale_scores", handler=scale_scores),
            agents.LogicStep(
                step_id="summarize_scores",
                dependencies=("scale_scores",),
                handler=summarize_scores,
            ),
        ),
    )
    result = workflow.run(
        {"scores": [0.2, 0.5, 0.8], "scale": 10},
        execution_mode="dag",
        request_id="tutorial-agents-workflow",
    )
    summary = result.step_results["summarize_scores"].output

    print("Workflow success:", result.success)
    print("Execution order:", " -> ".join(result.execution_order))
    print("Scaled score count:", summary["count"])
    print("Scaled score mean:", f"{float(summary['mean']):.1f}")
    print("Diagram starts with:", workflow.to_mermaid(direction="LR").splitlines()[0])


if __name__ == "__main__":
    main()
