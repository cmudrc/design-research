"""Family-level acceptance tests for evidence-to-paper workflows."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest
from tests._subprocess_support import REPO_ROOT, subprocess_env

import design_research as dr

EXAMPLES_DIR = REPO_ROOT / "examples"
PAPER_EXAMPLES = (
    "ideation_evidence_to_paper.py",
    "computational_design_evidence_to_paper.py",
)


def _run_phase(script_name: str, phase: str, output_dir: Path) -> subprocess.CompletedProcess[str]:
    """Run one example lifecycle phase in its own interpreter."""
    return subprocess.run(
        [
            sys.executable,
            str(EXAMPLES_DIR / script_name),
            "--phase",
            phase,
            "--output-dir",
            str(output_dir),
        ],
        cwd=output_dir.parent,
        env=subprocess_env(),
        check=True,
        capture_output=True,
        text=True,
        timeout=120,
    )


@pytest.mark.parametrize("script_name", PAPER_EXAMPLES)
def test_paper_examples_use_a_fresh_process_and_verify_the_bundle(
    script_name: str,
    tmp_path: Path,
) -> None:
    """Execution must stop before explicit draft and bundle reconstruction."""
    output_dir = tmp_path / script_name.removesuffix(".py")
    run_phase = _run_phase(script_name, "run", output_dir)

    assert "Paper draft created during execution: False" in run_phase.stdout
    assert not (output_dir / "paper-draft").exists()

    draft_phase = _run_phase(script_name, "draft", output_dir)
    assert "Fresh-process draft: paper-draft/main.tex" in draft_phase.stdout
    assert "Bundle verified: True" in draft_phase.stdout

    draft_dir = output_dir / "paper-draft"
    manifest = json.loads((draft_dir / "paper_draft_manifest.json").read_text(encoding="utf-8"))
    assert manifest["document_status"] == "paper-draft"
    assert manifest["author_review_required"] is True
    assert manifest["tables"]
    assert manifest["figures"]
    assert (draft_dir / "main.tex").is_file()
    assert (draft_dir / "paper_draft.md").is_file()
    assert (output_dir / "study-paper-draft.zip").is_file()
    assert dr.analysis.verify_research_bundle(output_dir / "study-paper-draft.zip")["valid"]
    _assert_citations_resolve(draft_dir)
    with zipfile.ZipFile(output_dir / "study-paper-draft.zip") as archive:
        assert not any("participant-private-note" in name for name in archive.namelist())


def test_ideation_example_preserves_failure_and_exclusion_accounting(tmp_path: Path) -> None:
    """The ideation draft must distinguish attempts, failures, analysis, and exclusions."""
    output_dir = tmp_path / "ideation"
    _run_phase("ideation_evidence_to_paper.py", "run", output_dir)
    _run_phase("ideation_evidence_to_paper.py", "draft", output_dir)

    manifest = json.loads(
        (output_dir / "paper-draft" / "paper_draft_manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["run_accounting"] == {
        "planned": 24,
        "attempted": 24,
        "terminal": 24,
        "successful": 23,
        "failed": 1,
        "skipped": 0,
        "incomplete": 0,
        "analyzed": 21,
        "excluded": 2,
    }
    assert manifest["citation_count"] > 0
    assert manifest["completeness"] == "partial"
    assert "TODO (evidence)" in (output_dir / "paper-draft" / "paper_draft.md").read_text(
        encoding="utf-8"
    )


def test_canonical_forty_run_accounting_fixture_reconciles(tmp_path: Path) -> None:
    """Preserve the release-authority 40/37/3/35/2 accounting fixture."""
    levels = tuple(
        dr.experiments.Level(name=f"trial-{index:02d}", value=index) for index in range(40)
    )
    study = dr.experiments.Study(
        study_id="forty-run-accounting",
        title="Forty-run accounting fixture",
        description="Exercise exact lifecycle and analysis accounting.",
        factors=(
            dr.experiments.Factor(
                name="trial",
                description="Deterministic fixture trial.",
                levels=levels,
            ),
        ),
        run_budget=dr.experiments.RunBudget(replicates=1, parallelism=1, max_runs=40),
        output_dir=tmp_path / "forty-run-accounting",
    )

    def condition_runner(_run_spec: object, condition: object) -> object:
        trial = int(condition.factor_assignments["trial"])
        if trial >= 37:
            raise RuntimeError("intentional accounting failure")
        return dr.experiments.RunOutput(
            outputs={"trial": trial},
            metrics={"primary_outcome": float(trial)},
        )

    results = dr.experiments.run_study(
        study,
        conditions=dr.experiments.build_design(study),
        condition_runner=condition_runner,
        checkpoint=False,
        show_progress=False,
    )
    successful = [result for result in results if result.status.value == "success"]
    included = successful[:35]
    excluded = successful[35:]
    regression = dr.analysis.fit_regression(
        [[float(index)] for index in range(35)],
        [float(index) for index in range(35)],
        feature_names=("trial",),
    )
    record = dr.analysis.build_analysis_result(
        regression,
        analysis_id="forty-run-regression",
        candidate_run_ids=tuple(result.run_id for result in successful),
        included_run_ids=tuple(result.run_id for result in included),
        exclusions=tuple(
            {"run_id": result.run_id, "reason": "Prespecified reporting exclusion."}
            for result in excluded
        ),
        evidence_refs=tuple(f"artifacts/runs/{result.run_id}/run.json" for result in included),
    )
    packet = dr.analysis.collect_analysis_paper_contributions(record)
    support = dr.experiments.collect_paper_support(study, component_packets=(packet,))

    assert support.run_accounting == {
        "planned": 40,
        "attempted": 40,
        "terminal": 40,
        "successful": 37,
        "failed": 3,
        "skipped": 0,
        "incomplete": 0,
        "analyzed": 35,
        "excluded": 2,
    }


@pytest.mark.parametrize("script_name", PAPER_EXAMPLES)
def test_extracted_paper_drafts_compile_independently(
    script_name: str,
    tmp_path: Path,
) -> None:
    """A verified bundle must retain a draft that compiles after extraction."""
    tectonic = shutil.which("tectonic")
    if tectonic is None:
        pytest.skip("tectonic is not installed")
    output_dir = tmp_path / script_name.removesuffix(".py")
    _run_phase(script_name, "run", output_dir)
    _run_phase(script_name, "draft", output_dir)
    bundle = output_dir / "study-paper-draft.zip"
    assert dr.analysis.verify_research_bundle(bundle)["valid"]

    extracted = tmp_path / f"extracted-{script_name.removesuffix('.py')}"
    with zipfile.ZipFile(bundle) as archive:
        archive.extractall(extracted)
    draft_dir = extracted / "study-paper-draft" / "paper-draft"
    completed = subprocess.run(
        [tectonic, "main.tex"],
        cwd=draft_dir,
        check=False,
        capture_output=True,
        text=True,
        timeout=90,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert (draft_dir / "main.pdf").is_file()


def _assert_citations_resolve(draft_dir: Path) -> None:
    """Require every emitted citation key to exist in the curated bibliography."""
    tex = "\n".join(
        path.read_text(encoding="utf-8") for path in sorted((draft_dir / "sections").glob("*.tex"))
    )
    cited = {
        key.strip() for group in re.findall(r"\\cite\{([^}]+)\}", tex) for key in group.split(",")
    }
    bibliography = (draft_dir / "references.bib").read_text(encoding="utf-8")
    available = set(re.findall(r"@[A-Za-z]+\{([^,]+),", bibliography))
    assert cited <= available
