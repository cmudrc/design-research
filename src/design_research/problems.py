"""Thin wrappers for stable problem-catalog and contract APIs."""

from __future__ import annotations

from typing import TYPE_CHECKING, Final

from ._lazy import module_dir, resolve_lazy_export

_EXPORTS: Final[dict[str, str]] = {
    "Problem": "design_research_problems:Problem",
    "ComputableProblem": "design_research_problems:ComputableProblem",
    "ProblemKind": "design_research_problems:ProblemKind",
    "ProblemMetadata": "design_research_problems:ProblemMetadata",
    "ProblemTaxonomy": "design_research_problems:ProblemTaxonomy",
    "ProblemRegistry": "design_research_problems:ProblemRegistry",
    "get_problem": "design_research_problems:get_problem",
    "get_problem_as": "design_research_problems:get_problem_as",
    "list_problems": "design_research_problems:list_problems",
    "get_ideation_catalog": "design_research_problems:get_ideation_catalog",
}

__all__ = list(_EXPORTS.keys())


def __getattr__(name: str) -> object:
    """Resolve a deferred export from ``design_research_problems``."""
    return resolve_lazy_export(__name__, _EXPORTS, name)


def __dir__() -> list[str]:
    """Expose lazy exports in interactive discovery."""
    return module_dir(globals(), __all__)


if TYPE_CHECKING:
    from design_research_problems import ComputableProblem as ComputableProblem
    from design_research_problems import Problem as Problem
    from design_research_problems import ProblemKind as ProblemKind
    from design_research_problems import ProblemMetadata as ProblemMetadata
    from design_research_problems import ProblemRegistry as ProblemRegistry
    from design_research_problems import ProblemTaxonomy as ProblemTaxonomy
    from design_research_problems import get_ideation_catalog as get_ideation_catalog
    from design_research_problems import get_problem as get_problem
    from design_research_problems import get_problem_as as get_problem_as
    from design_research_problems import list_problems as list_problems
