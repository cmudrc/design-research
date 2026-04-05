"""Thin wrapper mirroring the sibling problems package public API."""

from __future__ import annotations

from importlib import import_module
from typing import Final

from ._lazy import module_dir, public_module_exports, resolve_lazy_export

_EXPORTS: Final[dict[str, str]] = public_module_exports("design_research_problems")
_OPTIONAL_MODULE_EXPORTS: Final[dict[str, str]] = {
    "integration": "design_research_problems.integration",
}

__all__ = list(_EXPORTS.keys())
for export_name in _OPTIONAL_MODULE_EXPORTS:
    if export_name not in __all__:
        __all__.append(export_name)


def __getattr__(name: str) -> object:
    """Resolve a deferred export from ``design_research_problems``."""
    module_path = _OPTIONAL_MODULE_EXPORTS.get(name)
    if module_path is not None:
        try:
            module = import_module(module_path)
        except ModuleNotFoundError as exc:
            raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from exc
        globals()[name] = module
        return module

    return resolve_lazy_export(__name__, _EXPORTS, name)


def __dir__() -> list[str]:
    """Expose lazy exports in interactive discovery."""
    return module_dir(globals(), __all__)
