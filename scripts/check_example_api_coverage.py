"""Check public API usage coverage across example files."""

from __future__ import annotations

import argparse

from _example_support import (
    PUBLIC_API_INIT,
    collect_covered_exports,
    discover_examples,
    extract_exports,
)


def main() -> int:
    """Compute example API-usage coverage and enforce a threshold."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--minimum", type=float, default=90.0)
    args = parser.parse_args()

    exports = extract_exports(PUBLIC_API_INIT)
    if not exports:
        raise ValueError("Failed to extract __all__ exports from package __init__.py")
    export_set = set(exports)

    examples = discover_examples()
    if not examples:
        raise ValueError("No examples found under examples/.")

    covered = collect_covered_exports(examples, exports)

    coverage_percent = (len(covered) / len(exports)) * 100.0 if exports else 100.0
    missing = sorted(export_set - covered)

    print(f"Example API coverage: {coverage_percent:.1f}% ({len(covered)}/{len(exports)})")
    if missing:
        print("Missing exports in examples:")
        for symbol in missing:
            print(f"- {symbol}")

    if coverage_percent < args.minimum:
        print(f"Coverage threshold failed: {coverage_percent:.1f}% < {args.minimum:.1f}%")
        return 1

    print("Example API coverage threshold passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
