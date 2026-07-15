"""Umbrella API for the CMU Design Research Collective ecosystem.

The ``design_research`` package is a thin, canonical entry point over four
modular libraries:

- ``design_research_problems`` for benchmark design tasks and registries.
- ``design_research_agents`` for executable AI participants and patterns.
- ``design_research_experiments`` for hypothesis-first study orchestration.
- ``design_research_analysis`` for unified-table analysis and reporting.

Philosophy
----------
We build tools to amplify design research, not automate it away. Progress comes
from tight loops between messy reality and clear evidence: framing problems
with people, testing ideas quickly, making assumptions explicit, and iterating
with humility. The ecosystem is built to support human-first judgment,
traceable evidence, end-to-end process rigor, practical constraints, and
collaborative impact.
"""

from __future__ import annotations

from importlib import import_module
from types import ModuleType
from typing import Final

from ._version import __version__

__all__ = ["__version__", "agents", "analysis", "experiments", "problems"]

_COMPONENTS: Final[dict[str, str]] = {
    "agents": "design_research.agents",
    "analysis": "design_research.analysis",
    "experiments": "design_research.experiments",
    "problems": "design_research.problems",
}


def __getattr__(name: str) -> ModuleType:
    """Import one component wrapper on first access.

    Args:
        name: Root attribute requested by the caller.

    Returns:
        Imported component wrapper module.

    Raises:
        AttributeError: If ``name`` is not a public component.
    """
    module_path = _COMPONENTS.get(name)
    if module_path is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module = import_module(module_path)
    globals()[name] = module
    return module


def __dir__() -> list[str]:
    """Return root attributes including deferred component names."""
    return sorted(set(globals()) | set(__all__))
