"""Run a few lightweight consistency checks for the docs tree."""

from __future__ import annotations

import ast
import re
import tomllib
from pathlib import Path

DOCS_DIR = Path("docs")
INDEX_PATH = DOCS_DIR / "index.rst"
API_PATH = DOCS_DIR / "api.rst"
README_PATH = Path("README.md")
PROJECT_PATH = Path("pyproject.toml")
VERSION_PATH = Path("src/design_research/_version.py")
COMPATIBILITY_PATH = DOCS_DIR / "compatibility.rst"
INSTALL_REQUIREMENT_PATTERN = re.compile(
    r"design-research(?:-(?:problems|agents|experiments|analysis))?==(?P<version>[0-9.]+)"
)


def extract_toctree_entries(index_path: Path) -> tuple[str, ...]:
    """Extract document entries from the first toctree in `index.rst`.

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
        if stripped.startswith(":"):
            continue
        if line.startswith("   "):
            entries.append(stripped)
            continue
        break
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
    errors.extend(validate_documented_versions())
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


def validate_documented_versions() -> list[str]:
    """Verify tutorial install commands and compatibility docs against pins."""
    versions = expected_package_versions()
    errors: list[str] = []
    tutorial_paths = tuple(sorted((DOCS_DIR / "tutorials").glob("*.rst"))) + tuple(
        sorted(Path("examples/tutorials").glob("*.ipynb"))
    )
    for path in tutorial_paths:
        text = path.read_text(encoding="utf-8")
        for match in INSTALL_REQUIREMENT_PATTERN.finditer(text):
            requirement = match.group(0)
            package_name = requirement.split("==", maxsplit=1)[0]
            documented_version = match.group("version")
            expected_version = versions[package_name]
            if documented_version != expected_version:
                errors.append(
                    f"{path} installs {package_name}=={documented_version}; "
                    f"expected {expected_version}."
                )

    compatibility = COMPATIBILITY_PATH.read_text(encoding="utf-8")
    for package_name, version in versions.items():
        if f"``{version}``" not in compatibility:
            errors.append(f"docs/compatibility.rst omits {package_name} version {version}.")
    return errors


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
