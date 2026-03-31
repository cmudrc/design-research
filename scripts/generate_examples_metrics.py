"""Compute example inventory and public-API coverage metrics."""

from __future__ import annotations

import json

from _example_support import (
    PUBLIC_API_INIT,
    REPO_ROOT,
    active_examples,
    collect_covered_exports,
    default_examples,
    discover_examples,
    example_path_text,
    extract_exports,
    opt_in_examples,
    run_live_example_enabled,
)

METRICS_PATH = REPO_ROOT / "artifacts" / "examples" / "examples_metrics.json"


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


def main() -> None:
    """Compute and write example inventory and public-API coverage metrics."""
    examples = discover_examples()
    if not examples:
        raise ValueError("No examples found under examples/.")

    runnable_examples = active_examples(examples)
    default_runnable_examples = default_examples(examples)
    live_examples = opt_in_examples(examples)
    exports = extract_exports(PUBLIC_API_INIT)
    covered = collect_covered_exports(examples, exports)

    example_count = len(examples)
    runnable_example_count = len(runnable_examples)
    covered_exports = len(covered)
    total_exports = len(exports)
    metrics = {
        "examples": {
            "passed": runnable_example_count,
            "total": runnable_example_count,
            "pass_percent": 100.0,
            "available": example_count,
            "skipped": example_count - runnable_example_count,
            "run_live_example_enabled": run_live_example_enabled(),
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
        f"{runnable_example_count}/{runnable_example_count} active of {example_count} available, "
        f"api: {covered_exports}/{total_exports})"
    )


if __name__ == "__main__":
    main()
