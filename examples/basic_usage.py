"""Minimal example usage for the umbrella package."""

from __future__ import annotations

import design_research as dr


def main() -> None:
    """Print top-level discovery information for the ecosystem wrapper."""
    print("Submodules:", ", ".join(name for name in dr.__all__ if name != "__version__"))
    print("Agents module:", dr.agents.__name__)
    print("Analysis module:", dr.analysis.__name__)
    print("Experiments module:", dr.experiments.__name__)
    print("Problems module:", dr.problems.__name__)
    print("Version:", dr.__version__)


if __name__ == "__main__":
    main()
