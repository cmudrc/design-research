"""Tests for the reproducible IDETC 2026 participant bundle."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from zipfile import ZipFile

from tests._subprocess_support import REPO_ROOT

BUNDLE_PATH = REPO_ROOT / "docs" / "_static" / "idetc2026-design-research-tutorial.zip"
BUNDLE_ROOT = "idetc2026-design-research-tutorial"
EXPECTED_PATHS = (
    f"{BUNDLE_ROOT}/README.md",
    f"{BUNDLE_ROOT}/requirements.txt",
    f"{BUNDLE_ROOT}/preflight.py",
    f"{BUNDLE_ROOT}/notebooks/problems_text_map.ipynb",
    f"{BUNDLE_ROOT}/notebooks/problems_truss_grammar.ipynb",
    f"{BUNDLE_ROOT}/notebooks/agents_workflow.ipynb",
    f"{BUNDLE_ROOT}/notebooks/experiments_monty_hall.ipynb",
    f"{BUNDLE_ROOT}/notebooks/analysis_reliability.ipynb",
    f"{BUNDLE_ROOT}/scripts/canonical_artifact_flow.py",
    f"{BUNDLE_ROOT}/scripts/long_agent_markov_comparison.py",
    f"{BUNDLE_ROOT}/scripts/partial_factorial_ideation_regression.py",
)


def test_committed_bundle_matches_source_manifest() -> None:
    """The public archive should never drift from its canonical sources."""
    completed = subprocess.run(
        [sys.executable, "scripts/build_idetc2026_bundle.py", "--check"],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert "IDETC 2026 bundle is current" in completed.stdout


def test_bundle_has_safe_deterministic_manifest() -> None:
    """The archive should contain only fixed, readable tutorial files."""
    with ZipFile(BUNDLE_PATH) as archive:
        infos = archive.infolist()
        names = tuple(info.filename for info in infos)
        requirements = archive.read(f"{BUNDLE_ROOT}/requirements.txt").decode()

    assert names == EXPECTED_PATHS
    assert all(info.date_time == (1980, 1, 1, 0, 0, 0) for info in infos)
    assert all(info.external_attr >> 16 == 0o100644 for info in infos)
    assert all(info.file_size > 0 for info in infos)
    assert all(".." not in Path(name).parts for name in names)
    assert requirements == ("design-research==0.4.0\nipykernel>=7.3,<8\nscikit-learn>=1.5,<2\n")
