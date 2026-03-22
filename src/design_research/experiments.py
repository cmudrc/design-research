"""Thin wrapper mirroring the sibling experiments package public API."""

from __future__ import annotations

from importlib import import_module
from typing import Any, Final

from ._experiments_compat import (
    make_seeded_random_baseline_factories as _make_seeded_random_baseline_factories,
)
from ._experiments_compat import (
    resolve_problem as _resolve_problem,
)
from ._lazy import module_dir, public_module_exports, resolve_lazy_export

_EXPORTS: Final[dict[str, str]] = public_module_exports("design_research_experiments")

__all__ = list(_EXPORTS.keys())


def _sibling_module() -> Any:
    """Return the eagerly imported sibling experiments module."""
    return import_module("design_research_experiments")


def __getattr__(name: str) -> object:
    """Resolve a deferred export from ``design_research_experiments``."""
    return resolve_lazy_export(__name__, _EXPORTS, name)


def __dir__() -> list[str]:
    """Expose lazy exports in interactive discovery."""
    return module_dir(globals(), __all__)


def resolve_problem(problem_id: str) -> object:
    """Resolve one packaged problem across sibling-version boundaries."""
    return _resolve_problem(_sibling_module(), problem_id=problem_id)


def make_seeded_random_baseline_factories() -> dict[str, Any]:
    """Return seeded-baseline factories across sibling-version boundaries."""
    return _make_seeded_random_baseline_factories(_sibling_module())
