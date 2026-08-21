"""Tests for the reproducible IDETC 2026 participant downloads."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from zipfile import ZipFile

from tests._subprocess_support import REPO_ROOT

BUNDLE_DIR = REPO_ROOT / "docs" / "_static"
SETUP_REQUIREMENTS_PATH = BUNDLE_DIR / "workshop-requirements.txt"
SETUP_PREFLIGHT_PATH = BUNDLE_DIR / "workshop-preflight.py"
SETUP_ZIP_PATH = BUNDLE_DIR / "idetc2026-design-research-setup.zip"
ACTIVITIES_PATH = BUNDLE_DIR / "idetc2026-design-research-activities.zip"
ACTIVITIES_ROOT = "idetc2026-design-research-activities"

EXPECTED_ACTIVITIES_PATHS = (
    f"{ACTIVITIES_ROOT}/README.md",
    f"{ACTIVITIES_ROOT}/notebooks/problems_text_map.ipynb",
    f"{ACTIVITIES_ROOT}/notebooks/problems_truss_grammar.ipynb",
    f"{ACTIVITIES_ROOT}/notebooks/agents_workflow.ipynb",
    f"{ACTIVITIES_ROOT}/notebooks/experiments_monty_hall.ipynb",
    f"{ACTIVITIES_ROOT}/notebooks/analysis_reliability.ipynb",
    f"{ACTIVITIES_ROOT}/scripts/canonical_artifact_flow.py",
    f"{ACTIVITIES_ROOT}/scripts/long_agent_markov_comparison.py",
    f"{ACTIVITIES_ROOT}/scripts/partial_factorial_ideation_regression.py",
)
EXPECTED_REQUIREMENTS = (
    "design-research==0.4.0\n"
    "design-research-agents[memory-graph,providers]==0.6.0\n"
    "design-research-analysis[data,lang,seq,stats]==0.3.1\n"
    "design-research-experiments[doe]==0.3.0\n"
    "design-research-problems[grammar,pandas,solvers]==0.4.0\n"
    "ipykernel>=7.3,<8\n"
    "nbclient>=0.11,<1\n"
    "nbformat>=5.10,<6\n"
)


def test_committed_downloads_match_source_manifests() -> None:
    """The public downloads should never drift from their canonical sources."""
    completed = subprocess.run(
        [sys.executable, "scripts/build_idetc2026_bundle.py", "--check"],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert completed.stdout.count("Workshop setup asset is current") == 2
    assert "IDETC 2026 activities bundle is current" in completed.stdout


def _assert_safe_manifest(path: Path, expected_paths: tuple[str, ...]) -> None:
    """Assert that one archive has only deterministic readable files."""
    with ZipFile(path) as archive:
        infos = archive.infolist()
        names = tuple(info.filename for info in infos)

    assert names == expected_paths
    assert all(info.date_time == (1980, 1, 1, 0, 0, 0) for info in infos)
    assert all(info.external_attr >> 16 == 0o100644 for info in infos)
    assert all(info.file_size > 0 for info in infos)
    assert all(".." not in Path(name).parts for name in names)


def test_setup_assets_are_direct_environment_only_downloads() -> None:
    """The advance setup should publish only direct environment files."""
    source_root = REPO_ROOT / "tutorial_materials" / "idetc2026"

    assert SETUP_REQUIREMENTS_PATH.read_text() == EXPECTED_REQUIREMENTS
    assert SETUP_REQUIREMENTS_PATH.read_bytes() == (source_root / "requirements.txt").read_bytes()
    assert SETUP_PREFLIGHT_PATH.read_bytes() == (source_root / "preflight.py").read_bytes()
    compile(SETUP_PREFLIGHT_PATH.read_text(), str(SETUP_PREFLIGHT_PATH), "exec")
    assert not SETUP_ZIP_PATH.exists()

    setup_page = (REPO_ROOT / "docs" / "workshop-setup.rst").read_text()
    assert "idetc2026-design-research-setup.zip" not in setup_page
    assert "workshop-requirements.txt" in setup_page
    assert "workshop-preflight.py" in setup_page
    assert "curl -fsSLo requirements.txt" in setup_page
    assert "curl -fsSLo preflight.py" in setup_page
    assert "curl.exe -fsSLo requirements.txt" in setup_page
    assert "curl.exe -fsSLo preflight.py" in setup_page
    assert "urllib.request" not in setup_page
    assert "--insecure" not in setup_page
    assert "curl -k" not in setup_page
    assert "IDETC" not in setup_page
    assert "ASME" not in setup_page


def test_activity_bundle_has_safe_content_only_manifest() -> None:
    """The mutable activity download should not replace environment files."""
    _assert_safe_manifest(ACTIVITIES_PATH, EXPECTED_ACTIVITIES_PATHS)

    assert not any(name.endswith("/requirements.txt") for name in EXPECTED_ACTIVITIES_PATHS)
    assert not any(name.endswith("/preflight.py") for name in EXPECTED_ACTIVITIES_PATHS)
