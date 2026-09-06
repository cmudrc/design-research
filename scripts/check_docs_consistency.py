"""Run a few lightweight consistency checks for the docs tree."""

from __future__ import annotations

import ast
import re
import tomllib
from importlib.metadata import PackageNotFoundError, metadata
from pathlib import Path

DOCS_DIR = Path("docs")
INDEX_PATH = DOCS_DIR / "index.rst"
API_PATH = DOCS_DIR / "api.rst"
README_PATH = Path("README.md")
PROJECT_PATH = Path("pyproject.toml")
VERSION_PATH = Path("src/design_research/_version.py")
COMPATIBILITY_PATH = DOCS_DIR / "compatibility.rst"
IDETC_REDIRECT_PATH = DOCS_DIR / "idetc2026.rst"
WORKSHOP_SETUP_PATH = DOCS_DIR / "workshop-setup.rst"
FAMILY_SMOKE_PATH = Path("tests/test_family_smoke.py")
PROMPT_STUDY_PATH = Path("examples/prompt_framing_study.py")
PROMPT_STUDY_DOC_PATH = DOCS_DIR / "prompt_framing_study.rst"
EXPECTED_BADGES = (
    "CI",
    "Coverage",
    "Examples Passing",
    "API in Examples",
    "Docs",
    "PyPI Version",
    "Python Versions",
)
COMPONENT_DOC_URLS = (
    "https://cmudrc.github.io/design-research-problems/",
    "https://cmudrc.github.io/design-research-agents/",
    "https://cmudrc.github.io/design-research-experiments/",
    "https://cmudrc.github.io/design-research-analysis/",
)
MATURITY_ISSUE_URL = "https://github.com/cmudrc/design-research/issues/12"
EXPECTED_ROOT_TOCTREE = ("guides", "tutorials/index", "architecture", "reference")
INSTALL_REQUIREMENT_PATTERN = re.compile(
    r"(?P<package>design-research(?:-(?:problems|agents|experiments|analysis))?)"
    r"(?:\[[A-Za-z0-9_.-]+(?:,[A-Za-z0-9_.-]+)*\])?==(?P<version>[0-9.]+)"
)
COMPATIBILITY_ROW_PATTERN = re.compile(
    r"^\s*\* - ``(?P<package>design-research(?:-(?:problems|agents|experiments|analysis))?)``\s*$"
    r"\n^\s*- ``(?P<version>[0-9.]+)``\s*$"
    r"\n^\s*- (?P<status>[A-Za-z][A-Za-z -]*[A-Za-z])\s*$",
    flags=re.MULTILINE,
)
ARTIFACT_SCHEMA_PATTERN = re.compile(
    r"assert\s+manifest\[['\"]schema_version['\"]\]\s*==\s*"
    r"['\"](?P<version>[^'\"]+)['\"]"
)
DEFAULT_REPLICATES_PATTERN = re.compile(
    r"default configuration uses (?P<count>[0-9]+) replicates per condition",
    flags=re.IGNORECASE,
)


def extract_toctree_entries(index_path: Path) -> tuple[str, ...]:
    """Extract document entries from every toctree in an RST page.

    Args:
        index_path: Path to the docs index file.

    Returns:
        The referenced document names without suffixes.
    """
    entries: list[str] = []
    in_toctree = False
    for line in index_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped == ".. toctree::":
            in_toctree = True
            continue
        if not in_toctree:
            continue
        if not stripped:
            continue
        if line.startswith("   "):
            if stripped.startswith(":"):
                continue
            entries.append(stripped)
            continue
        in_toctree = False
    return tuple(entries)


def validate_docs_tree() -> list[str]:
    """Collect any missing or inconsistent documentation references.

    Returns:
        A list of validation error messages.
    """
    errors: list[str] = []
    if not README_PATH.exists():
        errors.append("README.md is missing.")
    if not INDEX_PATH.exists():
        errors.append("docs/index.rst is missing.")
        return errors

    for entry in extract_toctree_entries(INDEX_PATH):
        if "<" in entry and ">" in entry:
            continue
        if not (DOCS_DIR / f"{entry}.rst").exists():
            errors.append(f"docs/index.rst references missing document: {entry}.rst")

    if not API_PATH.exists():
        errors.append("docs/api.rst is missing.")
    elif "design_research" not in API_PATH.read_text(encoding="utf-8"):
        errors.append("docs/api.rst does not reference the package module.")
    errors.extend(validate_home_contract())
    errors.extend(validate_documented_versions())
    errors.extend(validate_prompt_study_replicates())
    return errors


def expected_artifact_schema_version() -> str:
    """Read the artifact schema asserted by the umbrella family smoke test."""
    match = ARTIFACT_SCHEMA_PATTERN.search(FAMILY_SMOKE_PATH.read_text(encoding="utf-8"))
    if match is None:
        raise ValueError(f"{FAMILY_SMOKE_PATH} omits an artifact schema assertion.")
    return match.group("version")


def validate_home_contract() -> list[str]:
    """Keep shared identity, navigation, badges, and compatibility framing aligned."""
    readme = README_PATH.read_text(encoding="utf-8")
    index = INDEX_PATH.read_text(encoding="utf-8")
    compatibility = COMPATIBILITY_PATH.read_text(encoding="utf-8")
    errors: list[str] = []

    for badge in EXPECTED_BADGES:
        if f"![{badge}]" not in readme:
            errors.append(f"README.md omits the {badge} badge.")
        if f'alt="{badge}"' not in index:
            errors.append(f"docs/index.rst omits the {badge} badge.")

    for heading in ("Control Topology", "Runtime And Data Flow"):
        if heading not in index:
            errors.append(f"docs/index.rst omits the {heading} architecture view.")

    for component_url in COMPONENT_DOC_URLS:
        if component_url not in readme:
            errors.append(f"README.md omits component documentation link: {component_url}")
        if component_url not in index:
            errors.append(f"docs/index.rst omits component documentation link: {component_url}")

    root_entries = extract_toctree_entries(INDEX_PATH)
    if root_entries != EXPECTED_ROOT_TOCTREE:
        errors.append(
            "docs/index.rst root navigation must be section-first: "
            f"expected {EXPECTED_ROOT_TOCTREE}, observed {root_entries}."
        )
    if "idetc2026" in root_entries:
        errors.append("docs/index.rst must not include the legacy idetc2026 redirect.")
    if not IDETC_REDIRECT_PATH.read_text(encoding="utf-8").lstrip().startswith(":orphan:"):
        errors.append("docs/idetc2026.rst must remain an orphaned legacy redirect.")

    artifact_schema = expected_artifact_schema_version()
    if f"artifact schema ``{artifact_schema}``" not in compatibility:
        errors.append(f"docs/compatibility.rst omits tested artifact schema {artifact_schema}.")
    if MATURITY_ISSUE_URL not in compatibility:
        errors.append("docs/compatibility.rst omits the open maturity-policy issue.")
    return errors


def expected_package_versions() -> dict[str, str]:
    """Return umbrella and exact component versions from package metadata."""
    project = tomllib.loads(PROJECT_PATH.read_text(encoding="utf-8"))["project"]
    versions: dict[str, str] = {}
    for dependency in project["dependencies"]:
        name, separator, version = dependency.partition("==")
        if separator and name.startswith("design-research-"):
            versions[name] = version

    version_module = ast.parse(VERSION_PATH.read_text(encoding="utf-8"))
    umbrella_version = next(
        node.value.value
        for node in version_module.body
        if isinstance(node, ast.Assign)
        and any(
            isinstance(target, ast.Name) and target.id == "__version__" for target in node.targets
        )
        and isinstance(node.value, ast.Constant)
        and isinstance(node.value.value, str)
    )
    versions["design-research"] = umbrella_version
    return versions


def _development_status_label(classifiers: list[str] | tuple[str, ...]) -> str:
    """Extract one PyPI development-status label from classifier strings."""
    matches = [
        classifier.split(" - ", maxsplit=1)[1]
        for classifier in classifiers
        if classifier.startswith("Development Status :: ") and " - " in classifier
    ]
    if len(matches) != 1:
        raise ValueError(f"Expected one Development Status classifier; found {matches}.")
    return matches[0]


def expected_development_statuses(versions: dict[str, str]) -> dict[str, str]:
    """Read development status from source metadata or the installed exact pin.

    An adjacent component checkout is preferred during package-family work.
    Standalone umbrella checkouts fall back to installed distribution metadata;
    the umbrella's exact dependencies make those releases available after the
    normal development install.
    """
    repo_root = PROJECT_PATH.resolve().parent
    statuses: dict[str, str] = {}
    for package_name, expected_version in versions.items():
        source_metadata_path = (
            PROJECT_PATH
            if package_name == "design-research"
            else repo_root.parent / package_name / "pyproject.toml"
        )
        if source_metadata_path.exists():
            project = tomllib.loads(source_metadata_path.read_text(encoding="utf-8"))["project"]
            actual_version = project.get("version", expected_version)
            classifiers = project.get("classifiers", [])
        else:
            try:
                package_metadata = metadata(package_name)
            except PackageNotFoundError as exc:
                raise ValueError(
                    f"Cannot verify {package_name} metadata; install the umbrella development "
                    "environment or use adjacent component checkouts."
                ) from exc
            actual_version = package_metadata["Version"]
            classifiers = package_metadata.get_all("Classifier", [])
        if actual_version != expected_version:
            raise ValueError(
                f"{package_name} metadata is version {actual_version}; expected exact umbrella "
                f"pin {expected_version}."
            )
        statuses[package_name] = _development_status_label(classifiers)
    return statuses


def documented_compatibility_rows(path: Path) -> tuple[tuple[str, str, str], ...]:
    """Read package, version, and status associations from the compatibility table.

    Args:
        path: Compatibility page containing the exact-pin table.

    Returns:
        Package, version, and development-status tuples in documented order.
    """
    text = path.read_text(encoding="utf-8")
    return tuple(
        (match.group("package"), match.group("version"), match.group("status"))
        for match in COMPATIBILITY_ROW_PATTERN.finditer(text)
    )


def validate_compatibility_rows(
    *,
    versions: dict[str, str],
    statuses: dict[str, str],
    path: Path,
) -> list[str]:
    """Validate exact compatibility table associations.

    Args:
        versions: Expected package versions.
        statuses: Expected development-status labels.
        path: Compatibility page containing the table.

    Returns:
        Association and inventory errors.
    """
    errors: list[str] = []
    documented_rows = documented_compatibility_rows(path)
    documented_versions: dict[str, str] = {}
    documented_statuses: dict[str, str] = {}
    for package_name, version, status in documented_rows:
        if package_name in documented_versions:
            errors.append(f"docs/compatibility.rst repeats the {package_name} version row.")
        documented_versions[package_name] = version
        documented_statuses[package_name] = status

    for package_name, version in versions.items():
        documented_version = documented_versions.get(package_name)
        if documented_version is None:
            errors.append(f"docs/compatibility.rst omits {package_name} version {version}.")
        elif documented_version != version:
            errors.append(
                f"docs/compatibility.rst lists {package_name}=={documented_version}; "
                f"expected {version}."
            )
    for package_name in sorted(documented_versions.keys() - versions.keys()):
        errors.append(f"docs/compatibility.rst lists unexpected package {package_name}.")
    for package_name, expected_status in statuses.items():
        documented_status = documented_statuses.get(package_name)
        if documented_status is None:
            errors.append(
                f"docs/compatibility.rst omits {package_name} development status {expected_status}."
            )
        elif documented_status != expected_status:
            errors.append(
                f"docs/compatibility.rst lists {package_name} status {documented_status!r}; "
                f"expected {expected_status!r}."
            )
    return errors


def validate_documented_versions() -> list[str]:
    """Verify current install commands and compatibility rows against pins.

    The IDETC participant requirements are a frozen, independently tested environment
    lock and intentionally remain outside this release-candidate documentation check.
    """
    versions = expected_package_versions()
    errors: list[str] = []
    documented_paths = tuple(
        sorted(
            {
                README_PATH,
                Path("CONTRIBUTING.md"),
                Path("examples/README.md"),
                PROMPT_STUDY_PATH,
                WORKSHOP_SETUP_PATH,
                *DOCS_DIR.rglob("*.rst"),
                *Path("examples/tutorials").glob("*.ipynb"),
            },
            key=lambda path: path.as_posix(),
        )
    )
    for path in documented_paths:
        text = path.read_text(encoding="utf-8")
        for match in INSTALL_REQUIREMENT_PATTERN.finditer(text):
            package_name = match.group("package")
            documented_version = match.group("version")
            expected_version = versions[package_name]
            if documented_version != expected_version:
                errors.append(
                    f"{path} installs {package_name}=={documented_version}; "
                    f"expected {expected_version}."
                )

    try:
        statuses = expected_development_statuses(versions)
    except ValueError as exc:
        errors.append(str(exc))
    else:
        errors.extend(
            validate_compatibility_rows(
                versions=versions,
                statuses=statuses,
                path=COMPATIBILITY_PATH,
            )
        )
    return errors


def prompt_study_default_replicates() -> int:
    """Read the walkthrough's default replicate count from its source file."""
    module = ast.parse(PROMPT_STUDY_PATH.read_text(encoding="utf-8"))
    for node in module.body:
        if not isinstance(node, ast.Assign) or not isinstance(node.value, ast.Constant):
            continue
        if not isinstance(node.value.value, int):
            continue
        if any(
            isinstance(target, ast.Name) and target.id == "DEFAULT_REPLICATES_PER_CONDITION"
            for target in node.targets
        ):
            return node.value.value
    raise ValueError(f"{PROMPT_STUDY_PATH} omits integer DEFAULT_REPLICATES_PER_CONDITION.")


def validate_prompt_study_replicates() -> list[str]:
    """Keep the documented walkthrough default synchronized with the script."""
    documented = DEFAULT_REPLICATES_PATTERN.search(
        PROMPT_STUDY_DOC_PATH.read_text(encoding="utf-8")
    )
    if documented is None:
        return [f"{PROMPT_STUDY_DOC_PATH} omits the default prompt-study replicate count."]
    expected = prompt_study_default_replicates()
    observed = int(documented.group("count"))
    if observed != expected:
        return [
            f"{PROMPT_STUDY_DOC_PATH} documents {observed} default replicates; expected {expected}."
        ]
    return []


def main() -> int:
    """Run the docs consistency check.

    Returns:
        Process exit code: `0` on success and `1` on failure.
    """
    errors = validate_docs_tree()
    if errors:
        for error in errors:
            print(error)
        return 1
    print("Documentation checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
