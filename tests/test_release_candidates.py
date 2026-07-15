"""Tests for the component release-candidate contract."""

from __future__ import annotations

import importlib.metadata
import json

import pytest
from scripts.check_release_candidates import (
    ReleaseCandidate,
    read_component_versions,
    read_release_candidates,
    validate_candidate_set,
)
from tests._subprocess_support import REPO_ROOT

PROJECT_PATH = REPO_ROOT / "pyproject.toml"
CANDIDATES_PATH = REPO_ROOT / "requirements" / "release-candidates.txt"


def test_current_release_candidate_matrix_is_complete_and_immutable() -> None:
    """Keep one immutable source commit aligned with every component dependency."""
    versions = read_component_versions(PROJECT_PATH)
    candidates = read_release_candidates(CANDIDATES_PATH)

    assert versions == {
        "design-research-agents": "0.5.0",
        "design-research-analysis": "0.3.0",
        "design-research-experiments": "0.2.1",
        "design-research-problems": "0.4.0",
    }
    assert validate_candidate_set(versions, candidates) == []


def test_installed_source_candidates_match_the_reviewed_commits() -> None:
    """Verify exact VCS revisions when CI installs the source-candidate matrix."""
    candidates = read_release_candidates(CANDIDATES_PATH)
    expected = {candidate.name: candidate.revision for candidate in candidates}
    installed: dict[str, str] = {}

    for name in expected:
        direct_url = importlib.metadata.distribution(name).read_text("direct_url.json")
        if direct_url is None:
            continue
        commit_id = json.loads(direct_url).get("vcs_info", {}).get("commit_id")
        if commit_id is not None:
            installed[name] = str(commit_id)

    if not installed:
        pytest.skip("Component packages were installed from published distributions.")
    assert installed == expected


def test_candidate_validation_rejects_branch_references() -> None:
    """Require immutable commit SHAs instead of moving branch or tag names."""
    candidate = ReleaseCandidate(
        name="design-research-problems",
        repo="design-research-problems",
        revision="main",
    )

    errors = validate_candidate_set({"design-research-problems": "0.4.0"}, (candidate,))

    assert errors == [
        "Candidate design-research-problems must use a full 40-character lowercase commit SHA."
    ]


def test_candidate_validation_rejects_repository_mismatches() -> None:
    """Keep each package requirement tied to its same-named repository."""
    candidate = ReleaseCandidate(
        name="design-research-problems",
        repo="design-research-agents",
        revision="a" * 40,
    )

    errors = validate_candidate_set({"design-research-problems": "0.4.0"}, (candidate,))

    assert errors == [
        "Candidate design-research-problems points to repository design-research-agents; "
        "names must match."
    ]


def test_candidate_validation_rejects_missing_duplicate_and_unexpected_packages() -> None:
    """Require a one-to-one mapping between dependencies and source candidates."""
    candidate = ReleaseCandidate(
        name="design-research-agents",
        repo="design-research-agents",
        revision="a" * 40,
    )
    unexpected = ReleaseCandidate(
        name="design-research-extra",
        repo="design-research-extra",
        revision="b" * 40,
    )

    errors = validate_candidate_set(
        {
            "design-research-agents": "0.5.0",
            "design-research-problems": "0.4.0",
        },
        (candidate, candidate, unexpected),
    )

    assert errors == [
        "Candidate design-research-agents appears 2 times; expected exactly once.",
        "Missing release candidate for exact dependency design-research-problems.",
        "Unexpected release candidate without an exact dependency: design-research-extra.",
    ]
