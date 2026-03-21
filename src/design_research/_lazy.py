"""Utilities for lazy re-export wrappers."""

from __future__ import annotations

from importlib import import_module


def public_module_exports(module_path: str) -> dict[str, str]:
    """Build lazy-export targets from a sibling module's public API.

    Args:
        module_path: Import path for the sibling module.

    Returns:
        Mapping of public name to ``module:attribute`` target.
    """
    module = import_module(module_path)
    public_names = getattr(module, "__all__", None)
    if public_names is None:
        public_names = [name for name in dir(module) if not name.startswith("_")]
        return {
            str(name): f"{module_path}:{name}"
            for name in public_names
            if isinstance(name, str) and not name.startswith("_")
        }
    return {str(name): f"{module_path}:{name}" for name in public_names if isinstance(name, str)}


def resolve_lazy_export(module_name: str, exports: dict[str, str], name: str) -> object:
    """Resolve one deferred export and cache it on the module.

    Args:
        module_name: Module containing the wrapper export map.
        exports: Mapping of export name to ``module:attribute`` target.
        name: Requested export name.

    Returns:
        The resolved object.

    Raises:
        AttributeError: If ``name`` is not a known public export.
    """
    target = exports.get(name)
    if target is None:
        raise AttributeError(f"module {module_name!r} has no attribute {name!r}")
    module_path, attribute = target.split(":", maxsplit=1)
    value = getattr(import_module(module_path), attribute)
    globals_dict = import_module(module_name).__dict__
    globals_dict[name] = value
    return value


def module_dir(module_globals: dict[str, object], public_names: list[str]) -> list[str]:
    """Return sorted attributes including deferred export names.

    Args:
        module_globals: Global namespace dictionary for the module.
        public_names: Public attribute names defined by ``__all__``.

    Returns:
        Sorted attribute names for interactive discovery.
    """
    return sorted(set(module_globals.keys()) | set(public_names))
