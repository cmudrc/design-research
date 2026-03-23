"""Thin wrapper mirroring the sibling analysis package public API."""

from __future__ import annotations

import sys
from importlib import import_module
from typing import Final

from ._lazy import module_dir, public_module_exports, resolve_lazy_export

_EXPORTS: Final[dict[str, str]] = public_module_exports("design_research_analysis")

__all__ = list(_EXPORTS.keys())


def __getattr__(name: str) -> object:
    """Resolve a deferred export from ``design_research_analysis``."""
    if name == "integration":
        value = sys.modules.get("design_research_analysis.integration")
        if value is None:
            value = import_module("design_research_analysis.integration")
        globals()[name] = value
        return value
    return resolve_lazy_export(__name__, _EXPORTS, name)


def __dir__() -> list[str]:
    """Expose lazy exports in interactive discovery."""
    return module_dir(globals(), __all__)
