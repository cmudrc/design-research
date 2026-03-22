"""Shared helpers for bundled example inventory, policy, and API usage."""

from __future__ import annotations

import ast
import json
import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLES_ROOT = REPO_ROOT / "examples"
PUBLIC_API_INIT = REPO_ROOT / "src" / "design_research" / "__init__.py"
PACKAGE_NAME = "design_research"
RUN_LIVE_EXAMPLE_ENV = "RUN_LIVE_EXAMPLE"
OPT_IN_EXAMPLE_NAMES = frozenset({"prompt_framing_study.py"})


def discover_examples() -> tuple[Path, ...]:
    """Return runnable example files under ``examples/``."""
    discovered: list[Path] = []
    for pattern in ("*.py", "*.ipynb"):
        for path in sorted(EXAMPLES_ROOT.rglob(pattern)):
            relative_parts = path.relative_to(EXAMPLES_ROOT).parts
            if "__pycache__" in relative_parts or any(
                part.startswith("_") for part in relative_parts
            ):
                continue
            discovered.append(path)
    return tuple(sorted(discovered))


def default_examples(examples: tuple[Path, ...]) -> tuple[Path, ...]:
    """Return examples exercised by the default offline-focused checks."""
    return tuple(path for path in examples if path.name not in OPT_IN_EXAMPLE_NAMES)


def opt_in_examples(examples: tuple[Path, ...]) -> tuple[Path, ...]:
    """Return examples that require explicit opt-in to execute."""
    return tuple(path for path in examples if path.name in OPT_IN_EXAMPLE_NAMES)


def run_live_example_enabled() -> bool:
    """Return whether opt-in live examples should run in the current environment."""
    return os.getenv(RUN_LIVE_EXAMPLE_ENV, "").strip() == "1"


def active_examples(examples: tuple[Path, ...]) -> tuple[Path, ...]:
    """Return examples that should run for the current execution mode."""
    if run_live_example_enabled():
        return examples
    return default_examples(examples)


def example_path_text(path: Path) -> str:
    """Return a repo-relative example path for user-facing reporting."""
    return str(path.relative_to(REPO_ROOT))


def extract_exports(path: Path) -> tuple[str, ...]:
    """Extract public API symbol names from ``__all__`` in the package init module."""
    module = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in module.body:
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        if not isinstance(node.targets[0], ast.Name) or node.targets[0].id != "__all__":
            continue
        if not isinstance(node.value, (ast.List, ast.Tuple)):
            break

        exports: list[str] = []
        for element in node.value.elts:
            if (
                isinstance(element, ast.Constant)
                and isinstance(element.value, str)
                and element.value != "__version__"
            ):
                exports.append(element.value)
        return tuple(exports)

    raise ValueError(f"Failed to extract a static __all__ export list from {path}.")


def collect_covered_exports(
    examples: tuple[Path, ...], export_symbols: tuple[str, ...]
) -> set[str]:
    """Collect covered public exports across all discovered examples."""
    covered: set[str] = set()
    for example in examples:
        if example.suffix == ".py":
            covered.update(usage_from_source(example.read_text(encoding="utf-8"), export_symbols))
        elif example.suffix == ".ipynb":
            covered.update(usage_from_notebook(example, export_symbols))
    return covered


def usage_from_source(source: str, export_symbols: tuple[str, ...]) -> set[str]:
    """Collect covered public API symbols from one source string."""
    try:
        module = ast.parse(source)
    except SyntaxError:
        return set()

    export_set = set(export_symbols)
    package_aliases = collect_package_aliases(module)
    covered = collect_explicit_imported_exports(module, export_set)
    covered.update(collect_attribute_access_exports(module, export_set, package_aliases))
    return covered


def usage_from_notebook(path: Path, export_symbols: tuple[str, ...]) -> set[str]:
    """Collect covered public API symbols from one notebook example."""
    payload = json.loads(path.read_text(encoding="utf-8"))
    hits: set[str] = set()
    for cell in payload.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        source = cell.get("source", [])
        cell_source = "".join(source) if isinstance(source, list) else str(source)
        hits.update(usage_from_source(cell_source, export_symbols))
    return hits


def collect_package_aliases(module: ast.Module) -> set[str]:
    """Collect local aliases bound to the umbrella package."""
    aliases = collect_direct_package_aliases(module)
    aliases.update(collect_import_module_package_aliases(module))
    return aliases


def collect_direct_package_aliases(module: ast.Module) -> set[str]:
    """Collect aliases for direct ``import design_research`` statements."""
    aliases: set[str] = set()
    for node in ast.walk(module):
        if not isinstance(node, ast.Import):
            continue
        for alias in node.names:
            if alias.name == PACKAGE_NAME:
                aliases.add(alias.asname or PACKAGE_NAME)
    return aliases


def collect_import_module_package_aliases(module: ast.Module) -> set[str]:
    """Collect aliases bound via ``importlib.import_module('design_research')``."""
    importlib_aliases, import_module_aliases = collect_import_module_aliases(module)
    aliases: set[str] = set()
    for node in ast.walk(module):
        target_name = assignment_target_name(node)
        if target_name is None:
            continue
        value = assignment_value(node)
        if value is None or not is_package_import_module_call(
            value,
            importlib_aliases=importlib_aliases,
            import_module_aliases=import_module_aliases,
        ):
            continue
        aliases.add(target_name)
    return aliases


def collect_import_module_aliases(module: ast.Module) -> tuple[set[str], set[str]]:
    """Collect aliases for ``importlib`` and ``import_module`` imports."""
    importlib_aliases: set[str] = set()
    import_module_aliases: set[str] = set()
    for node in ast.walk(module):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "importlib":
                    importlib_aliases.add(alias.asname or "importlib")
        if isinstance(node, ast.ImportFrom) and node.module == "importlib":
            for alias in node.names:
                if alias.name == "import_module":
                    import_module_aliases.add(alias.asname or "import_module")
    return importlib_aliases, import_module_aliases


def assignment_target_name(node: ast.AST) -> str | None:
    """Return the bound name for simple assignment forms."""
    if (
        isinstance(node, ast.Assign)
        and len(node.targets) == 1
        and isinstance(node.targets[0], ast.Name)
    ):
        return node.targets[0].id
    if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
        return node.target.id
    return None


def assignment_value(node: ast.AST) -> ast.AST | None:
    """Return the assigned value for supported assignment forms."""
    if isinstance(node, ast.Assign):
        return node.value
    if isinstance(node, ast.AnnAssign):
        return node.value
    return None


def is_package_import_module_call(
    node: ast.AST,
    *,
    importlib_aliases: set[str],
    import_module_aliases: set[str],
) -> bool:
    """Return whether ``node`` imports the umbrella package via ``import_module``."""
    if not isinstance(node, ast.Call) or len(node.args) != 1:
        return False
    package_arg = node.args[0]
    if not isinstance(package_arg, ast.Constant) or package_arg.value != PACKAGE_NAME:
        return False

    if isinstance(node.func, ast.Name):
        return node.func.id in import_module_aliases
    if (
        isinstance(node.func, ast.Attribute)
        and node.func.attr == "import_module"
        and isinstance(node.func.value, ast.Name)
    ):
        return node.func.value.id in importlib_aliases
    return False


def collect_explicit_imported_exports(module: ast.Module, export_set: set[str]) -> set[str]:
    """Collect exported symbols imported from the package root or submodules."""
    covered: set[str] = set()
    for node in ast.walk(module):
        if not isinstance(node, ast.ImportFrom):
            continue
        module_name = node.module or ""
        if module_name != PACKAGE_NAME and not module_name.startswith(f"{PACKAGE_NAME}."):
            continue
        for alias in node.names:
            if alias.name == "*":
                covered.update(export_set)
                continue
            if alias.name in export_set:
                covered.add(alias.name)
    return covered


def collect_attribute_access_exports(
    module: ast.Module,
    export_set: set[str],
    package_aliases: set[str],
) -> set[str]:
    """Collect exported symbols accessed as attributes on package aliases."""
    covered: set[str] = set()
    for node in ast.walk(module):
        if not isinstance(node, ast.Attribute) or not isinstance(node.value, ast.Name):
            continue
        if node.value.id in package_aliases and node.attr in export_set:
            covered.add(node.attr)
    return covered
