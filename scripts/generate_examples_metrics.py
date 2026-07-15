"""Compute example inventory and public-API coverage metrics."""

from __future__ import annotations

import json
from pathlib import Path

from _example_support import (
    PUBLIC_API_INIT,
    REPO_ROOT,
    collect_covered_exports,
    default_examples,
    discover_examples,
    example_enabled,
    example_path_text,
    extract_exports,
    opt_in_examples,
    selection_state,
)

METRICS_PATH = REPO_ROOT / "artifacts" / "examples" / "examples_metrics.json"
RESULTS_PATH = REPO_ROOT / "artifacts" / "examples" / "example_results.json"


def _percent(part: int, whole: int) -> float:
    """Return a one-decimal percentage for ``part / whole``.

    Args:
        part: Numerator.
        whole: Denominator.

    Returns:
        Percentage rounded to one decimal place.
    """
    if whole == 0:
        return 100.0
    return round((part / whole) * 100.0, 1)


def _read_execution_results(examples: tuple[Path, ...]) -> list[dict[str, object]]:
    """Read and validate per-example execution evidence."""
    if not RESULTS_PATH.exists():
        raise ValueError(f"Example execution evidence is missing: {RESULTS_PATH}")
    payload = json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
    if payload.get("schema_version") != 1:
        raise ValueError("Example execution evidence has an unsupported schema version.")
    if payload.get("selection") != selection_state():
        raise ValueError(
            "Example execution evidence does not match the current live-runtime selection."
        )
    raw_results = payload.get("results")
    if not isinstance(raw_results, list):
        raise ValueError("Example execution evidence must contain a results list.")

    examples_by_path = {example_path_text(example): example for example in examples}
    results: list[dict[str, object]] = []
    paths: list[str] = []
    for raw_result in raw_results:
        if not isinstance(raw_result, dict):
            raise ValueError("Each example execution result must be an object.")
        path = raw_result.get("path")
        status = raw_result.get("status")
        if not isinstance(path, str) or status not in {"passed", "failed", "skipped"}:
            raise ValueError("Example execution evidence contains an invalid path or status.")
        example = examples_by_path.get(path)
        if example is not None:
            selected = example_enabled(example)
            if selected and status == "skipped":
                raise ValueError(f"Selected example is incorrectly marked skipped: {path}")
            if not selected and status != "skipped":
                raise ValueError(f"Unselected example is incorrectly marked {status}: {path}")
        if status == "passed" and raw_result.get("returncode") != 0:
            raise ValueError(f"Passed example lacks a zero return code: {path}")
        if status == "failed" and (
            not isinstance(raw_result.get("returncode"), int) or raw_result["returncode"] == 0
        ):
            raise ValueError(f"Failed example lacks a nonzero return code: {path}")
        if status == "skipped" and not isinstance(raw_result.get("reason"), str):
            raise ValueError(f"Skipped example lacks a reason: {path}")
        paths.append(path)
        results.append(raw_result)

    expected_paths = [example_path_text(path) for path in examples]
    if len(paths) != len(set(paths)):
        raise ValueError("Example execution evidence contains duplicate paths.")
    if set(paths) != set(expected_paths):
        raise ValueError(
            "Example execution evidence does not match the discovered example inventory."
        )
    return results


def main() -> None:
    """Compute and write example inventory and public-API coverage metrics."""
    examples = discover_examples()
    if not examples:
        raise ValueError("No examples found under examples/.")

    default_runnable_examples = default_examples(examples)
    live_examples = opt_in_examples(examples)
    execution_results = _read_execution_results(examples)
    exports = extract_exports(PUBLIC_API_INIT)
    covered = collect_covered_exports(examples, exports)

    example_count = len(examples)
    passed = sum(result["status"] == "passed" for result in execution_results)
    failed = sum(result["status"] == "failed" for result in execution_results)
    skipped = sum(result["status"] == "skipped" for result in execution_results)
    attempted = passed + failed
    covered_exports = len(covered)
    total_exports = len(exports)
    metrics = {
        "examples": {
            "passed": passed,
            "failed": failed,
            "total": attempted,
            "pass_percent": _percent(passed, attempted),
            "available": example_count,
            "skipped": skipped,
            "selection": selection_state(),
        },
        "public_api": {
            "covered_exports": covered_exports,
            "total_exports": total_exports,
            "coverage_percent": _percent(covered_exports, total_exports),
        },
        "inventory": {
            "example_file_count": example_count,
            "default_example_count": len(default_runnable_examples),
            "opt_in_example_count": len(live_examples),
            "opt_in_examples": [example_path_text(path) for path in live_examples],
            "public_api_symbol_count": total_exports,
            "used_public_api_symbols": sorted(covered),
        },
        "example_file_count": example_count,
        "public_api_symbol_count": total_exports,
        "used_public_api_symbols": sorted(covered),
        "api_coverage_pct": _percent(covered_exports, total_exports),
    }

    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    METRICS_PATH.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(
        f"Wrote {METRICS_PATH} "
        "(examples: "
        f"{passed}/{attempted} passed, {skipped} skipped of {example_count} available, "
        f"api: {covered_exports}/{total_exports})"
    )


if __name__ == "__main__":
    main()
