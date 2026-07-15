"""Consumer-level checks for the advertised typed umbrella surface."""

from __future__ import annotations

from pathlib import Path

import pytest
from mypy import api as mypy_api


def test_wrapper_exports_keep_concrete_types(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Type-check representative wrapper imports as a downstream package would."""
    source = tmp_path / "consumer.py"
    source.write_text(
        """\
from collections.abc import Callable

from design_research.agents import MCPServerConfig, MultiStepAgent
from design_research.analysis import compute_interrater_reliability
from design_research.experiments import Study
from design_research.problems import Problem


def accepts_family(agent: MultiStepAgent, study: Study, problem: Problem) -> None:
    pass


factory: Callable[..., MCPServerConfig] = MCPServerConfig.python_module
irr_metric: Callable[..., object] = compute_interrater_reliability
""",
        encoding="utf-8",
    )
    package_src = Path(__file__).resolve().parents[1] / "src"
    monkeypatch.setenv("MYPYPATH", str(package_src))

    stdout, stderr, status = mypy_api.run(["--strict", "--no-incremental", str(source)])

    assert status == 0, stdout + stderr
