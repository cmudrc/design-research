"""Build deterministic IDETC 2026 setup assets and activity archive."""

from __future__ import annotations

import argparse
import hashlib
import io
from pathlib import Path, PurePosixPath
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = REPO_ROOT / "tutorial_materials" / "idetc2026"
FIXED_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
FILE_MODE = 0o100644

SETUP_ASSETS = (
    (
        SOURCE_ROOT / "requirements.txt",
        REPO_ROOT / "docs" / "_static" / "workshop-requirements.txt",
    ),
    (
        SOURCE_ROOT / "preflight.py",
        REPO_ROOT / "docs" / "_static" / "workshop-preflight.py",
    ),
)

ACTIVITIES_ROOT = PurePosixPath("idetc2026-design-research-activities")
ACTIVITIES_OUTPUT_PATH = REPO_ROOT / "docs" / "_static" / "idetc2026-design-research-activities.zip"
ACTIVITIES_FILES = (
    (SOURCE_ROOT / "ACTIVITIES.md", PurePosixPath("README.md")),
    (
        REPO_ROOT / "examples" / "tutorials" / "problems_text_map.ipynb",
        PurePosixPath("notebooks/problems_text_map.ipynb"),
    ),
    (
        REPO_ROOT / "examples" / "tutorials" / "problems_truss_grammar.ipynb",
        PurePosixPath("notebooks/problems_truss_grammar.ipynb"),
    ),
    (
        REPO_ROOT / "examples" / "tutorials" / "agents_workflow.ipynb",
        PurePosixPath("notebooks/agents_workflow.ipynb"),
    ),
    (
        REPO_ROOT / "examples" / "tutorials" / "experiments_monty_hall.ipynb",
        PurePosixPath("notebooks/experiments_monty_hall.ipynb"),
    ),
    (
        REPO_ROOT / "examples" / "tutorials" / "analysis_reliability.ipynb",
        PurePosixPath("notebooks/analysis_reliability.ipynb"),
    ),
    (
        REPO_ROOT / "examples" / "canonical_artifact_flow.py",
        PurePosixPath("scripts/canonical_artifact_flow.py"),
    ),
    (
        REPO_ROOT / "examples" / "long_agent_markov_comparison.py",
        PurePosixPath("scripts/long_agent_markov_comparison.py"),
    ),
    (
        REPO_ROOT / "examples" / "partial_factorial_ideation_regression.py",
        PurePosixPath("scripts/partial_factorial_ideation_regression.py"),
    ),
)


def build_bundle_bytes(
    archive_root: PurePosixPath,
    bundle_files: tuple[tuple[Path, PurePosixPath], ...],
) -> bytes:
    """Return one complete archive as deterministic bytes."""
    buffer = io.BytesIO()
    with ZipFile(buffer, mode="w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for source_path, relative_path in bundle_files:
            archive_path = archive_root / relative_path
            info = ZipInfo(str(archive_path), date_time=FIXED_TIMESTAMP)
            info.compress_type = ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = FILE_MODE << 16
            archive.writestr(info, source_path.read_bytes(), compresslevel=9)
    return buffer.getvalue()


def bundle_summary(payload: bytes) -> str:
    """Return compact size and checksum evidence for an archive payload."""
    digest = hashlib.sha256(payload).hexdigest()
    return f"{len(payload)} bytes, sha256={digest}"


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if a committed download does not match its source",
    )
    parser.add_argument(
        "--kind",
        choices=("all", "setup", "activities"),
        default="all",
        help="downloads to build or check; defaults to all",
    )
    return parser.parse_args()


def main() -> int:
    """Build downloads or verify that the committed copies are current."""
    args = parse_args()
    failed = False

    if args.kind in {"all", "setup"}:
        for source_path, output_path in SETUP_ASSETS:
            expected = source_path.read_bytes()
            label = output_path.name
            if not args.check:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_bytes(expected)
                print(f"Wrote {output_path}: {bundle_summary(expected)}")
                continue
            if not output_path.is_file():
                print(f"Workshop setup asset is missing: {output_path}")
                failed = True
                continue
            actual = output_path.read_bytes()
            if actual != expected:
                print(f"Workshop setup asset is stale: {output_path}")
                print(f"Expected {bundle_summary(expected)}")
                print(f"Actual   {bundle_summary(actual)}")
                failed = True
                continue
            print(f"Workshop setup asset is current ({label}): {bundle_summary(actual)}")

    if args.kind in {"all", "activities"}:
        expected = build_bundle_bytes(ACTIVITIES_ROOT, ACTIVITIES_FILES)
        if not args.check:
            ACTIVITIES_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
            ACTIVITIES_OUTPUT_PATH.write_bytes(expected)
            print(f"Wrote {ACTIVITIES_OUTPUT_PATH}: {bundle_summary(expected)}")
        elif not ACTIVITIES_OUTPUT_PATH.is_file():
            print(f"IDETC 2026 activities bundle is missing: {ACTIVITIES_OUTPUT_PATH}")
            failed = True
        else:
            actual = ACTIVITIES_OUTPUT_PATH.read_bytes()
            if actual != expected:
                print(f"IDETC 2026 activities bundle is stale: {ACTIVITIES_OUTPUT_PATH}")
                print(f"Expected {bundle_summary(expected)}")
                print(f"Actual   {bundle_summary(actual)}")
                failed = True
            else:
                print(f"IDETC 2026 activities bundle is current: {bundle_summary(actual)}")

    if failed:
        print("Run `make idetc2026-bundle` to refresh the downloads.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
