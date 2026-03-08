"""Thin wrappers for study-definition and orchestration APIs."""

from __future__ import annotations

from typing import TYPE_CHECKING, Final

from ._lazy import module_dir, resolve_lazy_export

_EXPORTS: Final[dict[str, str]] = {
    "Study": "design_research_experiments:Study",
    "Hypothesis": "design_research_experiments:Hypothesis",
    "OutcomeSpec": "design_research_experiments:OutcomeSpec",
    "AnalysisPlan": "design_research_experiments:AnalysisPlan",
    "Factor": "design_research_experiments:Factor",
    "Level": "design_research_experiments:Level",
    "Condition": "design_research_experiments:Condition",
    "Constraint": "design_research_experiments:Constraint",
    "Block": "design_research_experiments:Block",
    "build_design": "design_research_experiments:build_design",
    "generate_doe": "design_research_experiments:generate_doe",
    "materialize_conditions": "design_research_experiments:materialize_conditions",
    "run_study": "design_research_experiments:run_study",
    "resume_study": "design_research_experiments:resume_study",
    "validate_study": "design_research_experiments:validate_study",
    "export_analysis_tables": "design_research_experiments:export_analysis_tables",
}

__all__ = list(_EXPORTS.keys())


def __getattr__(name: str) -> object:
    """Resolve a deferred export from ``design_research_experiments``."""
    return resolve_lazy_export(__name__, _EXPORTS, name)


def __dir__() -> list[str]:
    """Expose lazy exports in interactive discovery."""
    return module_dir(globals(), __all__)


if TYPE_CHECKING:
    from design_research_experiments import AnalysisPlan as AnalysisPlan
    from design_research_experiments import Block as Block
    from design_research_experiments import Condition as Condition
    from design_research_experiments import Constraint as Constraint
    from design_research_experiments import Factor as Factor
    from design_research_experiments import Hypothesis as Hypothesis
    from design_research_experiments import Level as Level
    from design_research_experiments import OutcomeSpec as OutcomeSpec
    from design_research_experiments import Study as Study
    from design_research_experiments import build_design as build_design
    from design_research_experiments import export_analysis_tables as export_analysis_tables
    from design_research_experiments import generate_doe as generate_doe
    from design_research_experiments import materialize_conditions as materialize_conditions
    from design_research_experiments import resume_study as resume_study
    from design_research_experiments import run_study as run_study
    from design_research_experiments import validate_study as validate_study
