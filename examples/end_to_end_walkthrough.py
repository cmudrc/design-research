"""Canonical end-to-end umbrella workflow example."""

from __future__ import annotations

import csv
import importlib.util
import json
import os
from pathlib import Path

import design_research as dr

PROBLEM_ID = "decision_laptop_design_profit_maximization"
STUDY_ID = "umbrella_end_to_end_walkthrough"
OUTPUT_DIR = Path("artifacts") / "examples" / STUDY_ID
AGENT_ID = "live-workflow-agent"
ARTIFACT_NAMES = (
    "study.yaml",
    "manifest.json",
    "conditions.csv",
    "runs.csv",
    "events.csv",
    "evaluations.csv",
)


def main() -> None:
    """Run the umbrella walkthrough as one linear script."""
    # Start by resolving the real packaged problem that anchors the walkthrough.
    packaged_problem = dr.problems.get_problem(PROBLEM_ID)

    problem_title = str(
        getattr(getattr(packaged_problem, "metadata", object()), "title", PROBLEM_ID)
    )
    problem_statement_markdown = str(getattr(packaged_problem, "statement_markdown", "")).strip()
    problem_statement = problem_statement_markdown.replace("\n", " ").strip()
    if not problem_statement_markdown:
        problem_summary = "Using the packaged problem statement from design_research.problems."
    elif len(problem_statement) <= 220:
        problem_summary = problem_statement
    else:
        problem_summary = f"{problem_statement[:217].rstrip()}..."

    candidate_schema: dict[str, object] = {
        "type": "object",
        "properties": {},
        "required": [],
        "additionalProperties": False,
    }
    factor_lines: list[str] = []
    for factor in getattr(packaged_problem, "option_factors", ()):
        key = getattr(factor, "key", None)
        levels = tuple(getattr(factor, "levels", ()))
        if key is None or not levels:
            continue
        factor_key = str(key)
        factor_lines.append(f"- {factor_key}: {', '.join(str(level) for level in levels)}")
        candidate_schema["properties"][factor_key] = {
            "type": "number",
            "enum": list(levels),
        }
        candidate_schema["required"].append(factor_key)

    factor_keys = tuple(candidate_schema["required"])
    if not factor_keys:
        raise RuntimeError("Expected a packaged decision problem with explicit option factors.")

    if importlib.util.find_spec("llama_cpp") is None:
        raise RuntimeError(
            "Install llama-cpp-python before running the live walkthrough example "
            "(for example: python -m pip install llama-cpp-python)."
        )
    provider_name = "llama-cpp"
    configured_model_source = (
        os.getenv("LLAMA_CPP_MODEL", "Qwen2.5-1.5B-Instruct-Q4_K_M.gguf").strip()
        or "Qwen2.5-1.5B-Instruct-Q4_K_M.gguf"
    )
    configured_model_name = (
        os.getenv("LLAMA_CPP_API_MODEL", "qwen2-1.5b-q4").strip() or "qwen2-1.5b-q4"
    )
    configured_model_repo = (
        os.getenv("LLAMA_CPP_HF_MODEL_REPO_ID", "bartowski/Qwen2.5-1.5B-Instruct-GGUF").strip()
        or None
    )
    configured_host = os.getenv("LLAMA_CPP_HOST", "127.0.0.1").strip() or "127.0.0.1"
    configured_port = int(os.getenv("LLAMA_CPP_PORT", "8001"))
    configured_context_window = int(os.getenv("LLAMA_CPP_CONTEXT_WINDOW", "4096"))

    walkthrough_prompt = "\n".join(
        [
            "You are solving a packaged design-research decision problem.",
            "Read the problem statement and return exactly one JSON object.",
            "Choose one allowed value for each factor key.",
            "Return JSON only with no markdown fences and no extra commentary.",
            "",
            f"Problem title: {problem_title}",
            "Problem statement:",
            problem_statement_markdown,
            "",
            "Allowed factor values:",
            *factor_lines,
        ]
    )

    with dr.agents.LlamaCppServerLLMClient(
        model=configured_model_source,
        hf_model_repo_id=configured_model_repo,
        api_model=configured_model_name,
        host=configured_host,
        port=configured_port,
        context_window=configured_context_window,
    ) as llm_client:
        # Keep the required callbacks small and local so the walkthrough still reads
        # like one top-to-bottom script.
        def build_request(context: dict[str, object]) -> object:
            """Build one structured model request for the workflow step."""
            inputs = context.get("inputs", {})
            if not isinstance(inputs, dict):
                raise RuntimeError("Workflow inputs were not materialized as a mapping.")
            prompt = str(inputs.get("prompt", "")).strip()
            if not prompt:
                raise RuntimeError("Expected a non-empty walkthrough prompt.")
            return dr.agents.LLMRequest(
                messages=[
                    dr.agents.LLMMessage(
                        role="system",
                        content=(
                            "You are a careful study participant. Respond with valid JSON only "
                            "and match the requested schema exactly."
                        ),
                    ),
                    dr.agents.LLMMessage(role="user", content=prompt),
                ],
                temperature=0.0,
                max_tokens=400,
                response_schema=candidate_schema,
                metadata={"study_id": STUDY_ID, "problem_id": PROBLEM_ID},
            )

        def parse_response(response: object, context: dict[str, object]) -> dict[str, object]:
            """Parse the workflow model response into the final candidate payload."""
            del context
            response_text = str(getattr(response, "text", "")).strip()
            if response_text.startswith("```"):
                response_lines = response_text.splitlines()
                if response_lines and response_lines[0].startswith("```"):
                    response_lines = response_lines[1:]
                if response_lines and response_lines[-1].startswith("```"):
                    response_lines = response_lines[:-1]
                response_text = "\n".join(response_lines).strip()
            candidate = json.loads(response_text)
            if not isinstance(candidate, dict):
                raise RuntimeError("Expected the model to return a JSON object candidate.")
            return {"final_output": candidate, "model_text": str(getattr(response, "text", ""))}

        agent_workflow = dr.agents.Workflow(
            steps=(
                dr.agents.ModelStep(
                    step_id="select_candidate",
                    llm_client=llm_client,
                    request_builder=build_request,
                    response_parser=parse_response,
                ),
            ),
            input_schema={
                "type": "object",
                "properties": {"prompt": {"type": "string", "minLength": 1}},
                "required": ["prompt"],
                "additionalProperties": False,
            },
            output_schema=candidate_schema,
            default_request_id_prefix=STUDY_ID,
        )

        def live_agent_factory(condition: object) -> object:
            """Return one workflow-backed agent for the active condition."""
            del condition

            def run(problem_packet: object, run_spec: object | None = None) -> dict[str, object]:
                """Execute the live workflow and adapt it to experiment outputs."""
                del problem_packet
                request_id = str(getattr(run_spec, "run_id", STUDY_ID))
                execution = agent_workflow.run(
                    {"prompt": walkthrough_prompt}, request_id=request_id
                )
                if not execution.success:
                    raise RuntimeError(f"Live workflow failed: {execution.error}")

                candidate = execution.output_dict("final_output")
                if not candidate:
                    raise RuntimeError("Workflow completed without a structured candidate output.")

                model_response = execution.model_response
                usage = getattr(model_response, "usage", None)
                prompt_tokens = None
                completion_tokens = None
                if isinstance(usage, dict):
                    prompt_tokens = usage.get("prompt_tokens")
                    completion_tokens = usage.get("completion_tokens")
                elif usage is not None:
                    prompt_tokens = getattr(usage, "prompt_tokens", None)
                    completion_tokens = getattr(usage, "completion_tokens", None)

                metrics: dict[str, object] = {"cost_usd": 0.0}
                if isinstance(prompt_tokens, int):
                    metrics["input_tokens"] = prompt_tokens
                if isinstance(completion_tokens, int):
                    metrics["output_tokens"] = completion_tokens

                resolved_provider = str(getattr(model_response, "provider", "") or provider_name)
                resolved_model = str(getattr(model_response, "model", "") or configured_model_name)
                model_text = str(execution.output_value("model_text", "") or "").strip()

                trace_refs: list[str] = []
                trace_path = execution.metadata.get("trace_path")
                if isinstance(trace_path, str) and trace_path.strip():
                    trace_refs.append(trace_path)

                return {
                    "output": candidate,
                    "metrics": metrics,
                    "events": [
                        {
                            "text": f"Selected packaged problem: {problem_title}",
                            "event_type": "problem_selected",
                            "actor_id": "system",
                        },
                        {
                            "text": f"Statement excerpt: {problem_summary}",
                            "event_type": "problem_summary",
                            "actor_id": "system",
                        },
                        {
                            "text": f"Requested candidate over factors: {', '.join(factor_keys)}",
                            "event_type": "model_request",
                            "actor_id": "system",
                            "meta_json": {
                                "provider": resolved_provider,
                                "model_name": resolved_model,
                            },
                        },
                        {
                            "text": model_text or json.dumps(candidate, sort_keys=True),
                            "event_type": "model_response",
                            "actor_id": "agent",
                            "meta_json": {
                                "provider": resolved_provider,
                                "model_name": resolved_model,
                            },
                        },
                        {
                            "text": f"Candidate selected: {candidate}",
                            "event_type": "candidate_selected",
                            "actor_id": "agent",
                        },
                    ],
                    "trace_refs": trace_refs,
                    "metadata": {
                        "model_name": resolved_model,
                        "provider": resolved_provider,
                    },
                }

            return run

        # Define the study, materialize conditions, run it, and export canonical artifacts.
        study = dr.experiments.Study(
            study_id=STUDY_ID,
            title="Umbrella End-to-End Walkthrough",
            description=(
                "Live umbrella walkthrough using a real packaged problem, a managed "
                "llama.cpp workflow agent, and canonical experiment artifacts."
            ),
            notes=(
                "Requires llama-cpp-python and uses a managed llama_cpp.server runtime. "
                "The example intentionally has no deterministic fallback."
            ),
            problem_ids=(PROBLEM_ID,),
            agent_specs=(AGENT_ID,),
            output_dir=OUTPUT_DIR,
        )

        validation_errors = dr.experiments.validate_study(study)
        if validation_errors:
            raise RuntimeError("Study validation failed:\n- " + "\n- ".join(validation_errors))

        conditions = dr.experiments.build_design(study)
        results = dr.experiments.run_study(
            study,
            conditions=conditions,
            agent_factories={AGENT_ID: live_agent_factory},
            parallelism=1,
            checkpoint=False,
        )
        artifact_paths = dr.experiments.export_analysis_tables(
            study,
            conditions=conditions,
            run_results=results,
            output_dir=OUTPUT_DIR,
        )

        # Load the exported event rows back through the umbrella analysis layer.
        with artifact_paths["events.csv"].open(encoding="utf-8", newline="") as handle:
            event_rows = list(csv.DictReader(handle))
        report = dr.analysis.validate_unified_table(event_rows)
        if report.errors:
            raise RuntimeError(
                "Unified event table validation failed:\n- " + "\n- ".join(report.errors)
            )

        print(f"Problem: {PROBLEM_ID}")
        print(f"Provider: {provider_name}")
        print(
            f"Model API name: {results[0].provenance_info.get('model_name', configured_model_name)}"
        )
        print(f"Model source: {configured_model_source}")
        print(f"Conditions: {len(conditions)}")
        print(f"Runs: {len(results)} ({results[0].status})")
        print("Artifacts:")
        for artifact_name in ARTIFACT_NAMES:
            print(f"  - {artifact_name}: {artifact_paths[artifact_name]}")
        print(f"Event rows: {len(event_rows)}")
        print(f"Validation warnings: {len(report.warnings)}")


if __name__ == "__main__":
    main()
