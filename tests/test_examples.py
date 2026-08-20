"""Tests for bundled umbrella examples."""

from __future__ import annotations

import json
import runpy
import subprocess
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest
from tests._subprocess_support import REPO_ROOT, run_python_script, subprocess_env

EXAMPLES_DIR = REPO_ROOT / "examples"
TUTORIALS_DIR = EXAMPLES_DIR / "tutorials"
TUTORIAL_NOTEBOOKS = (
    "problems_text_map.ipynb",
    "problems_truss_grammar.ipynb",
    "agents_propose_critic.ipynb",
    "agents_workflow.ipynb",
    "experiments_monty_hall.ipynb",
    "analysis_reliability.ipynb",
)


def _run_example(example_name: str, *, tmp_path: Path) -> subprocess.CompletedProcess[str]:
    """Execute one example script in an isolated subprocess."""
    return run_python_script(
        EXAMPLES_DIR / example_name,
        cwd=tmp_path,
        env=subprocess_env(workspace_root=REPO_ROOT.parent),
    )


def _load_notebook(notebook_name: str) -> dict[str, Any]:
    """Load a committed tutorial notebook without requiring Jupyter at test time."""
    return json.loads((TUTORIALS_DIR / notebook_name).read_text(encoding="utf-8"))


def _notebook_output_text(notebook_name: str) -> str:
    """Collect stored text outputs from a committed tutorial notebook."""
    notebook = _load_notebook(notebook_name)
    output_parts: list[str] = []
    for cell in notebook["cells"]:
        for output in cell.get("outputs", []):
            text = output.get("text")
            if text is None:
                text = output.get("data", {}).get("text/plain")
            if isinstance(text, list):
                output_parts.extend(text)
            elif isinstance(text, str):
                output_parts.append(text)
    return "".join(output_parts)


def _notebook_has_png(notebook_name: str) -> bool:
    """Return whether a notebook contains a stored PNG display result."""
    notebook = _load_notebook(notebook_name)
    return any(
        "image/png" in output.get("data", {})
        for cell in notebook["cells"]
        for output in cell.get("outputs", [])
    )


def _prompt_study_result(strategy_id: str, *, status: str) -> SimpleNamespace:
    """Build the minimal run-result shape consumed by the live semantic guard."""
    return SimpleNamespace(
        status=SimpleNamespace(value=status),
        run_spec=SimpleNamespace(agent_spec_ref=strategy_id),
    )


def test_canonical_artifact_flow_example_executes(tmp_path: Path) -> None:
    """The canonical flow should exercise the full public umbrella handoff."""
    completed = _run_example("canonical_artifact_flow.py", tmp_path=tmp_path)
    assert "Canonical artifact flow: canonical_artifact_flow" in completed.stdout
    assert "Package path: problems -> agents -> experiments -> analysis" in completed.stdout
    assert "Problem: Decision Problem - Student Laptop Design Under Choice-Based Demand" in (
        completed.stdout
    )
    assert "Agent: SeededRandomBaselineAgent" in completed.stdout
    assert "Runs: 2 (2 success)" in completed.stdout
    assert "Mean primary_outcome:" in completed.stdout
    assert "Event rows valid: True" in completed.stdout


def test_student_laptop_design_study_example_executes(tmp_path: Path) -> None:
    """The student laptop study should report real packaged benchmark results."""
    completed = _run_example("student_laptop_design_study.py", tmp_path=tmp_path)
    assert "Study: student_laptop_design_study" in completed.stdout
    assert "Application: Decision Problem - Student Laptop Design Under Choice-Based Demand" in (
        completed.stdout
    )
    assert "Runs: 1 (success)" in completed.stdout
    assert "Observed results:" in completed.stdout
    assert "Event rows valid: True" in completed.stdout


def test_pump_and_battery_design_portfolio_example_executes(tmp_path: Path) -> None:
    """The engineering portfolio example should report real benchmark results."""
    completed = _run_example("pump_and_battery_design_portfolio.py", tmp_path=tmp_path)
    assert "Executed study: pump_and_battery_design_portfolio" in completed.stdout
    assert "Runs: 3 (" in completed.stdout
    assert "Observed benchmark results:" in completed.stdout
    assert "Event rows valid: True" in completed.stdout


def test_long_agent_markov_comparison_example_executes(tmp_path: Path) -> None:
    """The long-process example should compare condition-specific Markov chains."""
    completed = _run_example("long_agent_markov_comparison.py", tmp_path=tmp_path)
    assert "Long agent Markov comparison: long_agent_markov_comparison" in completed.stdout
    assert "Actions per run: 30" in completed.stdout
    assert "Runs: 20" in completed.stdout
    assert "Event rows valid: True" in completed.stdout
    assert "Transition matrix delta:" in completed.stdout


def test_model_size_sweep_regression_example_executes(tmp_path: Path) -> None:
    """The model-size example should regress outcomes from artifacts."""
    completed = _run_example("model_size_sweep_regression.py", tmp_path=tmp_path)
    assert "Model size sweep regression: model_size_sweep_regression" in completed.stdout
    assert "Model class: scripted-open-class" in completed.stdout
    assert "Runs: 20" in completed.stdout
    assert "Regression samples: 20" in completed.stdout
    assert "Coefficient model_size_b:" in completed.stdout


def test_partial_factorial_ideation_regression_example_executes(tmp_path: Path) -> None:
    """The partial-factorial example should fit a linear model from artifacts."""
    completed = _run_example("partial_factorial_ideation_regression.py", tmp_path=tmp_path)
    assert (
        "Partial factorial ideation regression: partial_factorial_ideation_regression"
        in completed.stdout
    )
    assert "Conditions: 12" in completed.stdout
    assert "Runs: 24" in completed.stdout
    assert "Regression samples: 24" in completed.stdout
    assert "Model size coefficient:" in completed.stdout


@pytest.mark.parametrize("notebook_name", TUTORIAL_NOTEBOOKS)
def test_tutorial_notebook_commits_results_for_every_step(notebook_name: str) -> None:
    """Every tutorial code cell should have a committed execution result."""
    notebook = _load_notebook(notebook_name)
    code_cells = [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]

    assert code_cells
    assert notebook["metadata"]["nbsphinx"]["execute"] == "never"
    assert all(cell["execution_count"] is not None for cell in code_cells)
    assert all(cell["outputs"] for cell in code_cells)


def test_problems_text_map_tutorial_records_catalog_projection() -> None:
    """The text-problem tutorial should retain its catalog and projection results."""
    output = _notebook_output_text("problems_text_map.ipynb")
    assert "Packaged text problems: 126" in output
    assert "TF-IDF matrix: 126 problems x 508 features" in output
    assert "Projection shape: (126, 2)" in output
    assert "Bicycle Safety Lock neighborhood:" in output
    assert _notebook_has_png("problems_text_map.ipynb")


def test_problems_truss_grammar_tutorial_records_manual_rule_application() -> None:
    """The truss tutorial should retain its manual grammar walkthrough."""
    output = _notebook_output_text("problems_truss_grammar.ipynb")
    assert "Seed state: 3 joints, 0 members" in output
    assert "Rule counts: {'add_joint': 3, 'add_member': 3}" in output
    assert "Final state: 3 joints, 3 members" in output
    assert "Seed members remain: 0" in output
    assert _notebook_has_png("problems_truss_grammar.ipynb")


def test_agents_propose_critic_tutorial_records_llm_result() -> None:
    """The simple Agents tutorial should retain an approved LLM-backed result."""
    output = _notebook_output_text("agents_propose_critic.ipynb")
    assert "Model: qwen3:8b" in output
    assert "Success: True" in output
    assert "Termination: approved" in output
    assert "Approved: True" in output
    assert "tradeoff" in output


def test_agents_propose_critic_tutorial_enforces_successful_approval() -> None:
    """The Ollama tutorial should fail when its final result is not usable."""
    notebook = _load_notebook("agents_propose_critic.ipynb")
    source = "\n".join(
        "".join(cell.get("source", [])) for cell in notebook["cells"] if cell["cell_type"] == "code"
    )

    assert "if not result.success or not result.approved:" in source
    assert "raise RuntimeError(" in source


def test_agents_workflow_tutorial_records_deterministic_result() -> None:
    """The advanced Agents tutorial should retain its dependency-graph result."""
    output = _notebook_output_text("agents_workflow.ipynb")
    assert "Handlers: scale_scores -> summarize_scores" in output
    assert "Workflow success: True" in output
    assert "Execution order: scale_scores -> summarize_scores" in output
    assert "Mean: 5.0" in output


def test_experiments_monty_hall_tutorial_records_simulation_result() -> None:
    """The Experiments tutorial should retain its seeded Monty Hall result."""
    output = _notebook_output_text("experiments_monty_hall.ipynb")
    assert "Study valid: True" in output
    assert "stay: 35/100 = 0.35" in output
    assert "switch: 65/100 = 0.65" in output
    assert "Observed lift: 0.30" in output


def test_analysis_reliability_tutorial_records_all_metrics() -> None:
    """The Analysis tutorial should retain all nominal IRR results."""
    output = _notebook_output_text("analysis_reliability.ipynb")
    assert "cohen_kappa: coefficient=0.500" in output
    assert "fleiss_kappa: coefficient=0.583" in output
    assert "krippendorff_alpha: coefficient=0.667" in output
    assert "missing=1" in output


def test_prompt_framing_walkthrough_uses_public_prompt_workflow_agent() -> None:
    """The live walkthrough should use the sibling-owned prompt workflow agent."""
    source = (EXAMPLES_DIR / "prompt_framing_study.py").read_text(encoding="utf-8")
    assert "_future_stack" not in source
    assert "_workspace_bootstrap" not in source
    assert "build_json_model_workflow" not in source
    assert "read_csv_rows" not in source
    assert "build_json_prompt_workflow" in source
    assert "PromptWorkflowAgent" in source
    assert "agent_bindings" in source


def test_prompt_framing_walkthrough_rejects_baseline_only_success() -> None:
    """A deterministic baseline must not masquerade as a passing live smoke test."""
    namespace = runpy.run_path(str(EXAMPLES_DIR / "prompt_framing_study.py"))
    require_successes = namespace["_require_successful_model_strategies"]
    results = [
        _prompt_study_result("SeededRandomBaselineAgent", status="success"),
        _prompt_study_result("neutral_prompt", status="failed"),
        _prompt_study_result("profit_focus_prompt", status="failed"),
    ]

    with pytest.raises(
        RuntimeError,
        match="Missing successful strategies: neutral_prompt, profit_focus_prompt",
    ):
        require_successes(results)


def test_prompt_framing_walkthrough_requires_each_model_strategy() -> None:
    """Every model-backed strategy should contribute an observed successful result."""
    namespace = runpy.run_path(str(EXAMPLES_DIR / "prompt_framing_study.py"))
    require_successes = namespace["_require_successful_model_strategies"]
    results = [
        _prompt_study_result("SeededRandomBaselineAgent", status="success"),
        _prompt_study_result("neutral_prompt", status="success"),
        _prompt_study_result("profit_focus_prompt", status="failed"),
    ]

    with pytest.raises(
        RuntimeError,
        match="Missing successful strategies: profit_focus_prompt",
    ):
        require_successes(results)


def test_prompt_framing_walkthrough_accepts_both_model_strategies() -> None:
    """The guard should pass after both live prompt strategies succeed."""
    namespace = runpy.run_path(str(EXAMPLES_DIR / "prompt_framing_study.py"))
    require_successes = namespace["_require_successful_model_strategies"]
    results = [
        _prompt_study_result("SeededRandomBaselineAgent", status="failed"),
        _prompt_study_result("neutral_prompt", status="success"),
        _prompt_study_result("profit_focus_prompt", status="success"),
    ]

    assert require_successes(results) == results[1:]


def test_prompt_framing_metrics_match_pinned_problem_integration() -> None:
    """Analysis metric names should match the evaluator's exported rows."""
    from design_research_problems.integration import (
        evaluate_problem_output,
        resolve_problem_binding,
    )

    namespace = runpy.run_path(str(EXAMPLES_DIR / "prompt_framing_study.py"))
    binding = resolve_problem_binding(namespace["PROBLEM_ID"])
    problem = binding.problem_object
    candidate = {factor.key: factor.levels[0] for factor in problem.option_factors}
    rows = evaluate_problem_output(
        binding,
        candidate,
    )
    metric_names = {row["metric_name"] for row in rows}

    assert namespace["PRIMARY_METRIC"] in metric_names
    assert namespace["SECONDARY_METRIC"] in metric_names


def test_examples_stay_on_public_artifact_helpers() -> None:
    """Tutorial examples should not ask users to load raw analysis tables."""
    combined_source = "\n".join(
        path.read_text(encoding="utf-8") for path in sorted(EXAMPLES_DIR.glob("*.py"))
    )

    assert "analysis.integration" not in combined_source
    assert "load_experiment_artifacts" not in combined_source
    assert "build_condition_metric_table(" not in combined_source
    assert "agent_result(" in combined_source
