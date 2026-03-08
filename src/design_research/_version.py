"""Package version resolution for ``design_research``."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("design-research")
except PackageNotFoundError:
    __version__ = "0+unknown"
