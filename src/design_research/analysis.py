"""Thin wrappers for unified-table analysis entry points."""

from __future__ import annotations

from typing import TYPE_CHECKING, Final

from ._lazy import module_dir, resolve_lazy_export

_EXPORTS: Final[dict[str, str]] = {
    "UnifiedTableConfig": "design_research_analysis:UnifiedTableConfig",
    "UnifiedTableValidationReport": "design_research_analysis:UnifiedTableValidationReport",
    "coerce_unified_table": "design_research_analysis:coerce_unified_table",
    "derive_columns": "design_research_analysis:derive_columns",
    "validate_unified_table": "design_research_analysis:validate_unified_table",
    "profile_dataframe": "design_research_analysis:profile_dataframe",
    "validate_dataframe": "design_research_analysis:validate_dataframe",
    "generate_codebook": "design_research_analysis:generate_codebook",
    "fit_markov_chain_from_table": "design_research_analysis:fit_markov_chain_from_table",
    "fit_discrete_hmm_from_table": "design_research_analysis:fit_discrete_hmm_from_table",
    "compute_language_convergence": "design_research_analysis:compute_language_convergence",
    "reduce_dimensions": "design_research_analysis:reduce_dimensions",
    "compare_groups": "design_research_analysis:compare_groups",
    "fit_regression": "design_research_analysis:fit_regression",
    "fit_mixed_effects": "design_research_analysis:fit_mixed_effects",
}

__all__ = list(_EXPORTS.keys())


def __getattr__(name: str) -> object:
    """Resolve a deferred export from ``design_research_analysis``."""
    return resolve_lazy_export(__name__, _EXPORTS, name)


def __dir__() -> list[str]:
    """Expose lazy exports in interactive discovery."""
    return module_dir(globals(), __all__)


if TYPE_CHECKING:
    from design_research_analysis import UnifiedTableConfig as UnifiedTableConfig
    from design_research_analysis import (
        UnifiedTableValidationReport as UnifiedTableValidationReport,
    )
    from design_research_analysis import coerce_unified_table as coerce_unified_table
    from design_research_analysis import compare_groups as compare_groups
    from design_research_analysis import (
        compute_language_convergence as compute_language_convergence,
    )
    from design_research_analysis import derive_columns as derive_columns
    from design_research_analysis import fit_discrete_hmm_from_table as fit_discrete_hmm_from_table
    from design_research_analysis import fit_markov_chain_from_table as fit_markov_chain_from_table
    from design_research_analysis import fit_mixed_effects as fit_mixed_effects
    from design_research_analysis import fit_regression as fit_regression
    from design_research_analysis import generate_codebook as generate_codebook
    from design_research_analysis import profile_dataframe as profile_dataframe
    from design_research_analysis import reduce_dimensions as reduce_dimensions
    from design_research_analysis import validate_dataframe as validate_dataframe
    from design_research_analysis import validate_unified_table as validate_unified_table
