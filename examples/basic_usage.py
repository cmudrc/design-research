"""Minimal example usage for the umbrella package."""

from __future__ import annotations

import design_research as dr


def main() -> None:
    """Print top-level discovery information for the ecosystem wrapper."""
    print("Submodules:", ", ".join(name for name in dr.__all__ if name != "__version__"))
    print("Version:", dr.__version__)


if __name__ == "__main__":
    main()
