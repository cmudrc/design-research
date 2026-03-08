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

from . import agents, analysis, experiments, problems
from ._version import __version__

__all__ = ["__version__", "agents", "analysis", "experiments", "problems"]
