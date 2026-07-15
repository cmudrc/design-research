"""Validate the umbrella's component dependency and source-commit matrix."""

from __future__ import annotations

import re
import tomllib
from dataclasses import dataclass
from pathlib import Path

PROJECT_PATH = Path("pyproject.toml")
CANDIDATES_PATH = Path("requirements/release-candidates.txt")
COMPONENT_PREFIX = "design-research-"
EXACT_DEPENDENCY_PATTERN = re.compile(
    r"^(?P<name>design-research-[a-z0-9-]+)==(?P<version>[^\s;]+)$"
)
CANDIDATE_PATTERN = re.compile(
    r"^(?P<name>design-research-[a-z0-9-]+)\s+@\s+"
    r"git\+https://github\.com/cmudrc/(?P<repo>design-research-[a-z0-9-]+)\.git@"
    r"(?P<revision>\S+)$"
)
COMMIT_PATTERN = re.compile(r"^[0-9a-f]{40}$")


@dataclass(frozen=True)
class ReleaseCandidate:
    """One component package pinned to one repository revision."""

    name: str
    repo: str
    revision: str


def read_component_versions(project_path: Path = PROJECT_PATH) -> dict[str, str]:
    """Read exact component versions from project dependencies."""
    project = tomllib.loads(project_path.read_text(encoding="utf-8"))["project"]
    versions: dict[str, str] = {}
    for dependency in project.get("dependencies", []):
        if not dependency.startswith(COMPONENT_PREFIX):
            continue
        match = EXACT_DEPENDENCY_PATTERN.fullmatch(dependency)
        if match is None:
            raise ValueError(f"Component dependency must use an exact version: {dependency!r}")
        name = match.group("name")
        if name in versions:
            raise ValueError(f"Duplicate component dependency: {name}")
        versions[name] = match.group("version")
    if not versions:
        raise ValueError("No component dependencies found in pyproject.toml")
    return versions


def read_release_candidates(
    candidates_path: Path = CANDIDATES_PATH,
) -> tuple[ReleaseCandidate, ...]:
    """Read component source requirements from the candidate matrix."""
    candidates: list[ReleaseCandidate] = []
    for line_number, line in enumerate(
        candidates_path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        match = CANDIDATE_PATTERN.fullmatch(stripped)
        if match is None:
            raise ValueError(
                f"Invalid release candidate at {candidates_path}:{line_number}: {stripped!r}"
            )
        candidates.append(ReleaseCandidate(**match.groupdict()))
    return tuple(candidates)


def validate_candidate_set(
    component_versions: dict[str, str],
    candidates: tuple[ReleaseCandidate, ...],
) -> list[str]:
    """Return validation errors for an in-memory candidate matrix."""
    errors: list[str] = []
    counts: dict[str, int] = {}
    for candidate in candidates:
        counts[candidate.name] = counts.get(candidate.name, 0) + 1
        if candidate.repo != candidate.name:
            errors.append(
                f"Candidate {candidate.name} points to repository {candidate.repo}; "
                "names must match."
            )
        if COMMIT_PATTERN.fullmatch(candidate.revision) is None:
            errors.append(
                f"Candidate {candidate.name} must use a full 40-character lowercase commit SHA."
            )

    for name, count in sorted(counts.items()):
        if count > 1:
            errors.append(f"Candidate {name} appears {count} times; expected exactly once.")

    expected = set(component_versions)
    actual = set(counts)
    for name in sorted(expected - actual):
        errors.append(f"Missing release candidate for exact dependency {name}.")
    for name in sorted(actual - expected):
        errors.append(f"Unexpected release candidate without an exact dependency: {name}.")
    return errors


def validate_files(
    project_path: Path = PROJECT_PATH,
    candidates_path: Path = CANDIDATES_PATH,
) -> tuple[dict[str, str], tuple[ReleaseCandidate, ...], list[str]]:
    """Load and validate the project dependency and candidate files."""
    component_versions = read_component_versions(project_path)
    candidates = read_release_candidates(candidates_path)
    errors = validate_candidate_set(component_versions, candidates)
    return component_versions, candidates, errors


def main() -> int:
    """Validate the repository's release-candidate contract."""
    try:
        component_versions, candidates, errors = validate_files()
    except (KeyError, OSError, tomllib.TOMLDecodeError, ValueError) as exc:
        print(f"Release-candidate validation failed: {exc}")
        return 1

    if errors:
        for error in errors:
            print(f"Release-candidate validation failed: {error}")
        return 1

    revisions = {candidate.name: candidate.revision for candidate in candidates}
    for name, version in sorted(component_versions.items()):
        print(f"{name}=={version} -> {revisions[name]}")
    print("Release-candidate checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
