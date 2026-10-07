"""Tests for example execution evidence, inventory, and metrics tooling."""

from __future__ import annotations

import importlib
import json
import subprocess
from pathlib import Path
from types import ModuleType
from zipfile import ZIP_DEFLATED, ZipFile

import nbformat
import pytest
from pytest import MonkeyPatch
from tests._subprocess_support import REPO_ROOT, run_python_script, subprocess_env

SCRIPTS_DIR = REPO_ROOT / "scripts"
METRICS_SCRIPT = SCRIPTS_DIR / "generate_examples_metrics.py"
RESULTS_PATH = REPO_ROOT / "artifacts" / "examples" / "example_results.json"
METRICS_PATH = REPO_ROOT / "artifacts" / "examples" / "examples_metrics.json"
OLLAMA_ENV = "RUN_OLLAMA_EXAMPLES"
LLAMA_CPP_ENV = "RUN_LLAMA_CPP_EXAMPLES"
OPT_IN_BY_NAME = {
    "agents_propose_critic.ipynb": OLLAMA_ENV,
    "prompt_framing_study.py": LLAMA_CPP_ENV,
}


def _discover_example_paths() -> tuple[Path, ...]:
    """Return the example inventory using the production discovery rules."""
    discovered: list[Path] = []
    for pattern in ("*.py", "*.ipynb"):
        for path in sorted((REPO_ROOT / "examples").rglob(pattern)):
            relative_parts = path.relative_to(REPO_ROOT / "examples").parts
            if "__pycache__" in relative_parts or any(
                part.startswith("_") for part in relative_parts
            ):
                continue
            discovered.append(path)
    return tuple(sorted(discovered))


def _write_evidence(
    *,
    ollama: bool = False,
    llama_cpp: bool = False,
    failed_path: Path | None = None,
) -> None:
    """Write internally consistent execution evidence for one selection state."""
    selection = {OLLAMA_ENV: ollama, LLAMA_CPP_ENV: llama_cpp}
    results: list[dict[str, object]] = []
    for path in _discover_example_paths():
        relative_path = str(path.relative_to(REPO_ROOT))
        opt_in_environment = OPT_IN_BY_NAME.get(path.name)
        selected = opt_in_environment is None or selection[opt_in_environment]
        if not selected:
            results.append(
                {
                    "path": relative_path,
                    "status": "skipped",
                    "reason": f"{opt_in_environment}=1 was not selected",
                }
            )
        elif path == failed_path:
            results.append({"path": relative_path, "status": "failed", "returncode": 1})
        else:
            results.append({"path": relative_path, "status": "passed", "returncode": 0})

    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_PATH.write_text(
        json.dumps({"schema_version": 1, "selection": selection, "results": results}),
        encoding="utf-8",
    )


def _run_metrics(*, ollama: bool = False, llama_cpp: bool = False) -> dict[str, object]:
    """Generate example metrics and return the parsed artifact."""
    run_python_script(
        METRICS_SCRIPT,
        cwd=REPO_ROOT,
        env=subprocess_env(
            updates={
                OLLAMA_ENV: "1" if ollama else None,
                LLAMA_CPP_ENV: "1" if llama_cpp else None,
            },
        ),
    )
    return json.loads(METRICS_PATH.read_text(encoding="utf-8"))


def _load_script_module(monkeypatch: MonkeyPatch, name: str) -> ModuleType:
    """Import one script module after exposing the scripts directory."""
    monkeypatch.syspath_prepend(str(SCRIPTS_DIR))
    return importlib.import_module(name)


def _write_metadata_wheel(directory: Path, name: str, version: str) -> Path:
    """Write the minimal metadata needed for candidate-wheel inventory tests."""
    filename_name = name.replace("-", "_")
    wheel_path = directory / f"{filename_name}-{version}-py3-none-any.whl"
    metadata_path = f"{filename_name}-{version}.dist-info/METADATA"
    with ZipFile(wheel_path, mode="w", compression=ZIP_DEFLATED) as archive:
        archive.writestr(
            metadata_path, f"Metadata-Version: 2.4\nName: {name}\nVersion: {version}\n"
        )
    return wheel_path


def test_subprocess_env_removes_source_paths_for_wheel_only_runs(
    monkeypatch: MonkeyPatch, tmp_path: Path
) -> None:
    """Candidate-wheel checks must not inherit any editable source override."""
    monkeypatch.setenv("PYTHONPATH", "/tmp/inherited-source")
    monkeypatch.setenv("DESIGN_RESEARCH_PROBLEMS_SRC", "/tmp/problems-source")
    monkeypatch.setenv("DESIGN_RESEARCH_AGENTS_ROOT", "/tmp/agents-source")

    env = subprocess_env(
        workspace_root=tmp_path,
        updates={"DESIGN_RESEARCH_WHEEL_ONLY": "1"},
    )

    assert "PYTHONPATH" not in env
    assert "DESIGN_RESEARCH_WORKSPACE_ROOT" not in env
    assert "DESIGN_RESEARCH_PROBLEMS_SRC" not in env
    assert "DESIGN_RESEARCH_AGENTS_ROOT" not in env
    assert env["DESIGN_RESEARCH_WHEEL_ONLY"] == "1"


def test_candidate_family_inventory_requires_exact_versions(
    monkeypatch: MonkeyPatch, tmp_path: Path
) -> None:
    """The release gate should accept one wheel at every coordinated version."""
    checker = _load_script_module(monkeypatch, "check_candidate_family")
    for name, (version, _module_name) in checker.EXPECTED_DISTRIBUTIONS.items():
        _write_metadata_wheel(tmp_path, name, version)

    discovered = checker.discover_candidate_wheels(tmp_path)

    assert set(discovered) == set(checker.EXPECTED_DISTRIBUTIONS)


def test_candidate_family_inventory_rejects_one_wrong_version(
    monkeypatch: MonkeyPatch, tmp_path: Path
) -> None:
    """A single stale family wheel must fail before environment creation."""
    checker = _load_script_module(monkeypatch, "check_candidate_family")
    for name, (version, _module_name) in checker.EXPECTED_DISTRIBUTIONS.items():
        candidate_version = "9.9.9" if name == "design-research-analysis" else version
        _write_metadata_wheel(tmp_path, name, candidate_version)

    with pytest.raises(ValueError, match=r"Expected design-research-analysis==0\.4\.0"):
        checker.discover_candidate_wheels(tmp_path)


def test_candidate_family_artifacts_must_stay_under_repo_artifacts(
    monkeypatch: MonkeyPatch, tmp_path: Path
) -> None:
    """The overwrite option must never target an unbounded directory."""
    checker = _load_script_module(monkeypatch, "check_candidate_family")
    monkeypatch.setattr(checker, "ARTIFACTS_ROOT", tmp_path / "artifacts")

    with pytest.raises(ValueError, match="must be a child"):
        checker._prepare_artifacts_dir(tmp_path / "outside", overwrite=True)


def test_execute_examples_records_pass_failure_and_skip(monkeypatch: MonkeyPatch) -> None:
    """The runner should retain evidence for every discovered example."""
    support = _load_script_module(monkeypatch, "_example_support")
    runner = _load_script_module(monkeypatch, "run_examples")
    monkeypatch.delenv(OLLAMA_ENV, raising=False)
    monkeypatch.delenv(LLAMA_CPP_ENV, raising=False)
    examples = support.discover_examples()
    offline_examples = support.default_examples(examples)
    selected_examples = (
        offline_examples[0],
        offline_examples[1],
        *support.opt_in_examples(examples),
    )

    def command_runner(command: list[str], **_kwargs: object) -> subprocess.CompletedProcess[str]:
        returncode = 1 if str(offline_examples[1]) in command else 0
        return subprocess.CompletedProcess(command, returncode)

    results = runner.execute_examples(
        selected_examples,
        env={},
        command_runner=command_runner,
    )

    assert [result["status"] for result in results] == [
        "passed",
        "failed",
        "skipped",
        "skipped",
    ]
    assert results[1]["returncode"] == 1
    assert all("reason" in result for result in results[2:])


def test_generate_examples_metrics_matches_default_execution_policy() -> None:
    """Default metrics should reflect saved deterministic execution evidence."""
    _write_evidence()
    metrics = _run_metrics()

    examples = metrics["examples"]
    inventory = metrics["inventory"]
    public_api = metrics["public_api"]

    assert examples["passed"] == inventory["default_example_count"]
    assert examples["failed"] == 0
    assert examples["total"] == inventory["default_example_count"]
    assert examples["available"] == inventory["example_file_count"]
    assert examples["skipped"] == inventory["opt_in_example_count"]
    assert examples["selection"] == {OLLAMA_ENV: False, LLAMA_CPP_ENV: False}
    assert inventory["opt_in_example_count"] == 2
    assert inventory["opt_in_examples"] == [
        "examples/prompt_framing_study.py",
        "examples/tutorials/agents_propose_critic.ipynb",
    ]
    assert inventory["example_file_count"] == (
        inventory["default_example_count"] + inventory["opt_in_example_count"]
    )
    assert public_api == {
        "covered_exports": 4,
        "total_exports": 4,
        "coverage_percent": 100.0,
    }


@pytest.mark.parametrize(
    ("ollama", "llama_cpp"),
    [(True, False), (False, True), (True, True)],
)
def test_generate_examples_metrics_selects_live_runtimes_independently(
    *, ollama: bool, llama_cpp: bool
) -> None:
    """Each live runtime should add only its independently selected example."""
    _write_evidence(ollama=ollama, llama_cpp=llama_cpp)
    metrics = _run_metrics(ollama=ollama, llama_cpp=llama_cpp)
    examples = metrics["examples"]
    inventory = metrics["inventory"]
    selected_count = int(ollama) + int(llama_cpp)

    assert examples["passed"] == inventory["default_example_count"] + selected_count
    assert examples["failed"] == 0
    assert examples["skipped"] == inventory["opt_in_example_count"] - selected_count
    assert examples["selection"] == {OLLAMA_ENV: ollama, LLAMA_CPP_ENV: llama_cpp}


def test_generate_examples_metrics_reports_failed_execution() -> None:
    """A failed example should reduce the evidence-backed pass rate."""
    failed_path = next(
        path for path in _discover_example_paths() if path.name not in OPT_IN_BY_NAME
    )
    _write_evidence(failed_path=failed_path)
    metrics = _run_metrics()
    examples = metrics["examples"]

    assert examples["failed"] == 1
    assert examples["passed"] == examples["total"] - 1
    assert examples["pass_percent"] < 100.0


def test_generate_examples_metrics_rejects_stale_selection_evidence() -> None:
    """Metrics should reject evidence produced under another live selection."""
    _write_evidence()
    with pytest.raises(subprocess.CalledProcessError):
        _run_metrics(ollama=True)


def test_notebook_freshness_detects_source_and_output_drift(
    monkeypatch: MonkeyPatch,
) -> None:
    """Freshness stamps should bind both notebook inputs and displayed results."""
    freshness = _load_script_module(monkeypatch, "_notebook_freshness")
    notebook = nbformat.v4.new_notebook(
        cells=[
            nbformat.v4.new_code_cell(
                "print('original')",
                execution_count=1,
                outputs=[nbformat.v4.new_output("stream", name="stdout", text="original\n")],
            )
        ]
    )

    freshness.stamp_notebook(notebook)
    assert freshness.validate_notebook(notebook) == []

    notebook.cells[0].source = "print('changed')"
    assert freshness.validate_notebook(notebook) == [
        "source changed after the saved outputs were recorded"
    ]

    freshness.stamp_notebook(notebook)
    notebook.cells[0].outputs[0].text = "changed\n"
    assert freshness.validate_notebook(notebook) == [
        "saved outputs changed after freshness metadata was recorded"
    ]


def test_docs_consistency_tracks_prompt_study_default(
    monkeypatch: MonkeyPatch, tmp_path: Path
) -> None:
    """Walkthrough prose should not drift from its executable default."""
    checker = _load_script_module(monkeypatch, "check_docs_consistency")
    study_path = tmp_path / "prompt_study.py"
    docs_path = tmp_path / "prompt_study.rst"
    study_path.write_text(
        "DEFAULT_REPLICATES_PER_CONDITION = 50\n",
        encoding="utf-8",
    )
    docs_path.write_text(
        "The default configuration uses 50 replicates per condition.\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(checker, "PROMPT_STUDY_PATH", study_path)
    monkeypatch.setattr(checker, "PROMPT_STUDY_DOC_PATH", docs_path)

    assert checker.validate_prompt_study_replicates() == []

    docs_path.write_text(
        "The default configuration uses 8 replicates per condition.\n",
        encoding="utf-8",
    )
    assert checker.validate_prompt_study_replicates() == [
        f"{docs_path} documents 8 default replicates; expected 50."
    ]


def test_docs_consistency_parses_pinned_install_with_extra(monkeypatch: MonkeyPatch) -> None:
    """An owning-package extra must not hide the package/version association."""
    checker = _load_script_module(monkeypatch, "check_docs_consistency")
    match = checker.INSTALL_REQUIREMENT_PATTERN.search(
        'python -m pip install "design-research-agents[llama_cpp]==0.7.0"'
    )

    assert match is not None
    assert match.group("package") == "design-research-agents"
    assert match.group("version") == "0.7.0"


def test_docs_consistency_binds_compatibility_rows_to_packages(
    monkeypatch: MonkeyPatch, tmp_path: Path
) -> None:
    """Compatibility versions should be parsed from their own package rows."""
    checker = _load_script_module(monkeypatch, "check_docs_consistency")
    compatibility_path = tmp_path / "compatibility.rst"
    compatibility_path.write_text(
        """\
   * - ``design-research``
     - ``0.4.0``
     - Alpha
   * - ``design-research-agents``
     - ``0.6.0``
     - Pre-Alpha
""",
        encoding="utf-8",
    )

    assert checker.documented_compatibility_rows(compatibility_path) == (
        ("design-research", "0.4.0", "Alpha"),
        ("design-research-agents", "0.6.0", "Pre-Alpha"),
    )

    errors = checker.validate_compatibility_rows(
        versions={"design-research": "0.4.0", "design-research-agents": "0.6.0"},
        statuses={"design-research": "Alpha", "design-research-agents": "Alpha"},
        path=compatibility_path,
    )
    assert errors == [
        "docs/compatibility.rst lists design-research-agents status 'Pre-Alpha'; expected 'Alpha'."
    ]


def test_docs_consistency_reads_component_status_from_source_metadata(
    monkeypatch: MonkeyPatch, tmp_path: Path
) -> None:
    """Adjacent component metadata should own the documented status label."""
    checker = _load_script_module(monkeypatch, "check_docs_consistency")
    umbrella_root = tmp_path / "design-research"
    component_root = tmp_path / "design-research-agents"
    umbrella_root.mkdir()
    component_root.mkdir()
    project_text = """\
[project]
name = "{name}"
version = "{version}"
classifiers = ["Development Status :: {number} - {status}"]
"""
    (umbrella_root / "pyproject.toml").write_text(
        project_text.format(name="design-research", version="0.4.0", number="3", status="Alpha"),
        encoding="utf-8",
    )
    (component_root / "pyproject.toml").write_text(
        project_text.format(
            name="design-research-agents",
            version="0.6.0",
            number="2",
            status="Pre-Alpha",
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(checker, "PROJECT_PATH", umbrella_root / "pyproject.toml")

    assert checker.expected_development_statuses(
        {"design-research": "0.4.0", "design-research-agents": "0.6.0"}
    ) == {
        "design-research": "Alpha",
        "design-research-agents": "Pre-Alpha",
    }
