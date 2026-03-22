"""Backward-compatible live-walkthrough bootstrap wrapper."""

from __future__ import annotations

from _future_stack import bootstrap_future_stack


def bootstrap_sibling_sources() -> tuple[str, ...]:
    """Add sibling repository ``src/`` directories to ``sys.path`` when available."""
    return bootstrap_future_stack()


__all__ = ["bootstrap_sibling_sources"]
