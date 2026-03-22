"""Private helpers for future-state umbrella examples."""

from __future__ import annotations

import csv
import importlib
import importlib.util
import json
import os
import sys
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_WORKSPACE_ROOT = REPO_ROOT.parent
WORKSPACE_ROOT_ENV = "DESIGN_RESEARCH_WORKSPACE_ROOT"
_SIBLING_REPOS = {
    "analysis": "design-research-analysis",
    "agents": "design-research-agents",
    "experiments": "design-research-experiments",
    "problems": "design-research-problems",
}


def bootstrap_future_stack() -> tuple[str, ...]:
    """Add sibling repository ``src/`` directories to ``sys.path`` when available."""
    inserted: list[str] = []
    for repo_key, repo_dir_name in _SIBLING_REPOS.items():
        repo_root = _resolve_repo_root(repo_key, repo_dir_name)
        src_path = repo_root / "src"
        src_text = str(src_path)
        if not src_path.exists() or src_text in sys.path:
            continue
        sys.path.insert(0, src_text)
        inserted.append(src_text)
    return tuple(inserted)


def import_design_research() -> Any:
    """Bootstrap sibling sources and import the umbrella package."""
    bootstrap_future_stack()
    return importlib.import_module("design_research")


def require_future_apis(dr: Any, *, live: bool = False) -> None:
    """Fail fast when the future-state sibling APIs are unavailable."""
    required = {
        "design_research.experiments": (
            "BenchmarkBundle",
            "build_strategy_comparison_study",
            "render_markdown_summary",
        ),
        "design_research.analysis": (
            "compare_condition_pairs",
            "build_condition_metric_table",
            "validate_unified_table",
        ),
        "design_research.agents": (
            "SeededRandomBaselineAgent",
            "Workflow",
        ),
        "design_research.problems": (
            "get_problem_as",
            "list_problems",
        ),
    }
    missing: list[str] = []
    for namespace, names in required.items():
        module = _resolve_namespace(dr, namespace)
        for name in names:
            if not hasattr(module, name):
                missing.append(f"{namespace}.{name}")

    if live and not hasattr(dr.agents, "LlamaCppServerLLMClient"):
        missing.append("design_research.agents.LlamaCppServerLLMClient")

    if missing:
        raise RuntimeError(
            "These examples track the future recipe-first sibling APIs. Install the target "
            "branches or keep sibling worktrees next to this repo. Missing APIs: "
            + ", ".join(missing)
        )


def make_delegate_agent_factory(
    delegate_builder: Callable[[], object],
    *,
    prompt_builder: Callable[[object, object, object], str] | None = None,
) -> Callable[[object], Callable[..., dict[str, object]]]:
    """Adapt a delegate or workflow-backed agent to the experiments factory contract."""
    resolved_prompt_builder = prompt_builder or _default_prompt

    def factory(_condition: object) -> Callable[..., dict[str, object]]:
        """Build one experiments-compatible executor from a delegate instance."""
        delegate = delegate_builder()
        run_delegate = delegate.run

        def run(
            *,
            problem_packet: object,
            run_spec: object,
            condition: object,
        ) -> dict[str, object]:
            """Execute one delegate call and normalize its outputs for experiments."""
            dependencies = {
                "problem_packet": problem_packet,
                "problem": _problem_object(problem_packet),
                "run_spec": run_spec,
                "condition": condition,
                "seed": getattr(run_spec, "seed", None),
            }
            execution = run_delegate(
                resolved_prompt_builder(problem_packet, run_spec, condition),
                request_id=str(getattr(run_spec, "run_id", "")),
                dependencies=dependencies,
            )
            if not bool(getattr(execution, "success", False)):
                raise RuntimeError(
                    f"Agent execution failed: {getattr(execution, 'error', 'unknown error')}"
                )

            metadata = dict(getattr(execution, "metadata", {}) or {})
            trace_refs = _trace_refs(metadata=metadata)
            return {
                "output": _output_mapping(execution, "final_output"),
                "metrics": _output_mapping(execution, "metrics"),
                "events": _output_sequence(execution, "events"),
                "trace_refs": trace_refs,
                "metadata": metadata,
            }

        return run

    return factory


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    """Read one exported CSV table into a list of row dictionaries."""
    with path.open("r", encoding="utf-8", newline="") as file_obj:
        return list(csv.DictReader(file_obj))


def load_analysis_exports(
    artifact_paths: Mapping[str, Path],
    *,
    names: Sequence[str],
) -> dict[str, list[dict[str, str]]]:
    """Load selected exported CSV artifacts into memory."""
    return {name: read_csv_rows(artifact_paths[name]) for name in names}


def validate_exported_events(dr: Any, artifact_paths: Mapping[str, Path]) -> Any:
    """Validate the exported canonical event table through the analysis layer."""
    return dr.analysis.validate_unified_table(read_csv_rows(artifact_paths["events.csv"]))


def condition_means(rows: list[dict[str, object]]) -> dict[str, float]:
    """Compute one mean per condition label from normalized rows."""
    grouped: dict[str, list[float]] = {}
    for row in rows:
        grouped.setdefault(str(row["condition"]), []).append(float(row["value"]))
    return {
        condition: (sum(values) / len(values) if values else 0.0)
        for condition, values in grouped.items()
    }


def decision_candidate_schema(problem: object) -> dict[str, object]:
    """Build a JSON schema for discrete decision-factor candidates."""
    properties: dict[str, object] = {}
    required: list[str] = []
    for factor in getattr(problem, "option_factors", ()):
        levels = tuple(getattr(factor, "levels", ()))
        key = str(getattr(factor, "key", ""))
        if not key or not levels:
            continue
        properties[key] = {"type": "number", "enum": list(levels)}
        required.append(key)

    if not required:
        raise RuntimeError("Expected a packaged decision problem with explicit option factors.")

    return {
        "type": "object",
        "properties": properties,
        "required": required,
        "additionalProperties": False,
    }


def llama_cpp_runtime_config(*, default_replicates: int) -> dict[str, object]:
    """Resolve runtime configuration and fail fast on missing live dependencies."""
    missing_runtime = [
        module_name
        for module_name in ("llama_cpp", "fastapi", "uvicorn")
        if importlib.util.find_spec(module_name) is None
    ]
    if missing_runtime:
        raise RuntimeError(
            "Install llama-cpp-python[server] before running the live walkthrough. Missing: "
            + ", ".join(sorted(missing_runtime))
        )

    model_source = (
        os.getenv("LLAMA_CPP_MODEL", "Qwen2.5-1.5B-Instruct-Q4_K_M.gguf").strip()
        or "Qwen2.5-1.5B-Instruct-Q4_K_M.gguf"
    )
    model_repo = (
        os.getenv("LLAMA_CPP_HF_MODEL_REPO_ID", "bartowski/Qwen2.5-1.5B-Instruct-GGUF").strip()
        or None
    )
    if (
        model_repo
        and not Path(model_source).expanduser().exists()
        and importlib.util.find_spec("huggingface_hub") is None
    ):
        raise RuntimeError(
            "Install huggingface-hub or point LLAMA_CPP_MODEL at a local GGUF file before "
            "running the live walkthrough."
        )

    replicates = int(os.getenv("PROMPT_STUDY_REPLICATES", str(default_replicates)))
    if replicates < 2:
        raise RuntimeError("PROMPT_STUDY_REPLICATES must be at least 2.")

    return {
        "provider_name": "llama-cpp",
        "model_source": model_source,
        "model_name": os.getenv("LLAMA_CPP_API_MODEL", "qwen2-1.5b-q4").strip() or "qwen2-1.5b-q4",
        "model_repo": model_repo,
        "host": os.getenv("LLAMA_CPP_HOST", "127.0.0.1").strip() or "127.0.0.1",
        "port": int(os.getenv("LLAMA_CPP_PORT", "8001")),
        "context_window": int(os.getenv("LLAMA_CPP_CONTEXT_WINDOW", "4096")),
        "replicates": replicates,
    }


def build_json_model_workflow(
    dr: Any,
    *,
    llm_client: object,
    candidate_schema: dict[str, object],
    study_id: str,
    problem_id: str,
    fallback_model_name: str,
    fallback_provider: str,
) -> object:
    """Build one reusable prompt-mode workflow that returns structured JSON."""

    def request_builder(context: Mapping[str, object]) -> object:
        """Build one structured LLM request from the workflow context."""
        return dr.agents.LLMRequest(
            messages=[
                dr.agents.LLMMessage(
                    role="system",
                    content=(
                        "You are a careful study participant. Return valid JSON only and match "
                        "the requested schema exactly."
                    ),
                ),
                dr.agents.LLMMessage(role="user", content=str(context["prompt"])),
            ],
            temperature=0.0,
            max_tokens=400,
            response_schema=candidate_schema,
            metadata={"study_id": study_id, "problem_id": problem_id},
        )

    def response_parser(response: object, _context: Mapping[str, object]) -> dict[str, object]:
        """Parse one model response into workflow output, metrics, and events."""
        model_text = strip_markdown_fences(str(getattr(response, "text", "")).strip())
        candidate = json.loads(model_text)
        if not isinstance(candidate, dict):
            raise RuntimeError("Expected the live workflow to return one JSON object candidate.")
        provider = str(getattr(response, "provider", "") or fallback_provider)
        model_name = str(getattr(response, "model", "") or fallback_model_name)
        return {
            "final_output": candidate,
            "metrics": usage_metrics(getattr(response, "usage", None)),
            "events": [
                {
                    "event_type": "model_response",
                    "actor_id": "agent",
                    "text": model_text,
                    "meta_json": {"provider": provider, "model_name": model_name},
                }
            ],
        }

    return dr.agents.Workflow(
        steps=(
            dr.agents.ModelStep(
                step_id="select_candidate",
                llm_client=llm_client,
                request_builder=request_builder,
                response_parser=response_parser,
            ),
        ),
        output_schema=candidate_schema,
        default_request_id_prefix=study_id,
    )


def artifact_names(artifact_paths: Mapping[str, Path]) -> str:
    """Return exported artifact filenames in stable sorted order."""
    return ", ".join(sorted(path.name for path in artifact_paths.values()))


def _resolve_repo_root(repo_key: str, repo_dir_name: str) -> Path:
    """Resolve one sibling repo root from repo-specific, workspace, or local defaults."""
    root_env = f"DESIGN_RESEARCH_{repo_key.upper()}_ROOT"
    src_env = f"DESIGN_RESEARCH_{repo_key.upper()}_SRC"

    explicit_src = os.getenv(src_env, "").strip()
    if explicit_src:
        return Path(explicit_src).expanduser().resolve().parent

    explicit_root = os.getenv(root_env, "").strip()
    if explicit_root:
        explicit_path = Path(explicit_root).expanduser().resolve()
        if explicit_path.exists():
            return explicit_path

    workspace_root_text = os.getenv(WORKSPACE_ROOT_ENV, "").strip()
    if workspace_root_text:
        workspace_root = Path(workspace_root_text).expanduser().resolve()
        candidate = workspace_root / repo_dir_name
        if candidate.exists():
            return candidate

    return DEFAULT_WORKSPACE_ROOT / repo_dir_name


def _resolve_namespace(dr: Any, namespace: str) -> Any:
    """Resolve one umbrella submodule from a dotted namespace string."""
    current = dr
    for part in namespace.split(".")[1:]:
        current = getattr(current, part)
    return current


def _problem_object(problem_packet: object) -> object | None:
    """Extract the underlying packaged problem object when present."""
    payload = getattr(problem_packet, "payload", {})
    if not isinstance(payload, Mapping):
        return None
    return payload.get("problem_object")


def _default_prompt(problem_packet: object, _run_spec: object, _condition: object) -> str:
    """Build the default delegate prompt from the normalized problem packet."""
    return str(getattr(problem_packet, "brief", "")).strip()


def _output_mapping(execution: object, key: str) -> dict[str, object]:
    """Read one mapping-valued entry from an execution result."""
    output_dict = getattr(execution, "output_dict", None)
    if callable(output_dict):
        value = output_dict(key)
        if isinstance(value, Mapping):
            return dict(value)
    output = getattr(execution, "output", {})
    if isinstance(output, Mapping):
        value = output.get(key, {})
        if isinstance(value, Mapping):
            return dict(value)
    return {}


def _output_sequence(execution: object, key: str) -> list[dict[str, object]]:
    """Read one sequence-valued entry from an execution result."""
    output_list = getattr(execution, "output_list", None)
    if callable(output_list):
        value = output_list(key)
        if isinstance(value, Sequence):
            return [dict(item) for item in value if isinstance(item, Mapping)]
    output = getattr(execution, "output", {})
    if isinstance(output, Mapping):
        value = output.get(key, ())
        if isinstance(value, Sequence):
            return [dict(item) for item in value if isinstance(item, Mapping)]
    return []


def _trace_refs(*, metadata: Mapping[str, object]) -> list[str]:
    """Extract best-effort trace references from execution metadata."""
    trace_refs: list[str] = []
    for key in ("trace_path", "trace_ref"):
        value = metadata.get(key)
        if isinstance(value, str) and value.strip():
            trace_refs.append(value)
    return trace_refs


def strip_markdown_fences(text: str) -> str:
    """Strip one optional fenced-code wrapper from a model response."""
    if not text.startswith("```"):
        return text
    lines = text.splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].startswith("```"):
        lines = lines[:-1]
    return "\n".join(lines).strip()


def usage_metrics(usage: object) -> dict[str, object]:
    """Normalize usage payloads into canonical metric names."""
    metrics: dict[str, object] = {"cost_usd": 0.0}
    if isinstance(usage, Mapping):
        prompt_tokens = usage.get("prompt_tokens")
        completion_tokens = usage.get("completion_tokens")
    else:
        prompt_tokens = getattr(usage, "prompt_tokens", None)
        completion_tokens = getattr(usage, "completion_tokens", None)
    if isinstance(prompt_tokens, int):
        metrics["input_tokens"] = prompt_tokens
    if isinstance(completion_tokens, int):
        metrics["output_tokens"] = completion_tokens
    return metrics


__all__ = [
    "artifact_names",
    "bootstrap_future_stack",
    "build_json_model_workflow",
    "condition_means",
    "decision_candidate_schema",
    "import_design_research",
    "llama_cpp_runtime_config",
    "load_analysis_exports",
    "make_delegate_agent_factory",
    "read_csv_rows",
    "require_future_apis",
    "strip_markdown_fences",
    "usage_metrics",
    "validate_exported_events",
]
