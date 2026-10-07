"""Validate the coordinated five-wheel candidate family in a clean environment."""

from __future__ import annotations

import argparse
import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import zipfile
from email.parser import BytesParser
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS_ROOT = REPO_ROOT / "artifacts"
EXPECTED_DISTRIBUTIONS = {
    "design-research": ("0.5.0", "design_research"),
    "design-research-problems": ("0.5.0", "design_research_problems"),
    "design-research-agents": ("0.7.0", "design_research_agents"),
    "design-research-experiments": ("0.4.0", "design_research_experiments"),
    "design-research-analysis": ("0.4.0", "design_research_analysis"),
}
PAPER_EXAMPLES = (
    "ideation_evidence_to_paper.py",
    "computational_design_evidence_to_paper.py",
)


def _normalized_name(name: str) -> str:
    """Return a distribution name in its comparison form."""
    return name.strip().lower().replace("_", "-").replace(".", "-")


def _wheel_identity(wheel_path: Path) -> tuple[str, str]:
    """Read the authoritative distribution name and version from wheel metadata."""
    with zipfile.ZipFile(wheel_path) as archive:
        metadata_names = [
            name for name in archive.namelist() if name.endswith(".dist-info/METADATA")
        ]
        if len(metadata_names) != 1:
            raise ValueError(
                f"{wheel_path.name} contains {len(metadata_names)} METADATA files; expected one."
            )
        metadata = BytesParser().parsebytes(archive.read(metadata_names[0]))
    name = metadata.get("Name")
    version = metadata.get("Version")
    if not name or not version:
        raise ValueError(f"{wheel_path.name} is missing Name or Version metadata.")
    return _normalized_name(name), version


def discover_candidate_wheels(wheelhouse: Path) -> dict[str, Path]:
    """Require exactly one correctly versioned wheel for every family package."""
    if not wheelhouse.is_dir():
        raise ValueError(f"Candidate wheelhouse does not exist: {wheelhouse}")
    wheel_paths = sorted(wheelhouse.glob("*.whl"))
    if len(wheel_paths) != len(EXPECTED_DISTRIBUTIONS):
        raise ValueError(
            f"Candidate wheelhouse contains {len(wheel_paths)} wheels; "
            f"expected exactly {len(EXPECTED_DISTRIBUTIONS)}."
        )

    discovered: dict[str, Path] = {}
    for wheel_path in wheel_paths:
        name, version = _wheel_identity(wheel_path)
        if name in discovered:
            raise ValueError(f"Candidate wheelhouse contains duplicate {name!r} wheels.")
        expected = EXPECTED_DISTRIBUTIONS.get(name)
        if expected is None:
            raise ValueError(f"Unexpected candidate distribution: {name}=={version}")
        if version != expected[0]:
            raise ValueError(f"Expected {name}=={expected[0]}, found {version}.")
        discovered[name] = wheel_path.resolve()

    missing = set(EXPECTED_DISTRIBUTIONS) - set(discovered)
    if missing:
        raise ValueError(f"Candidate wheelhouse is missing: {', '.join(sorted(missing))}")
    return discovered


def _clean_environment(runtime_root: Path) -> dict[str, str]:
    """Build an environment that cannot import the editable workspace family."""
    env = os.environ.copy()
    for key in tuple(env):
        is_source_override = key.startswith("DESIGN_RESEARCH_") and key.endswith(("_SRC", "_ROOT"))
        if key in {"PYTHONPATH", "DESIGN_RESEARCH_WORKSPACE_ROOT"} or is_source_override:
            env.pop(key)
    env["DESIGN_RESEARCH_WHEEL_ONLY"] = "1"
    env["MPLCONFIGDIR"] = str(runtime_root / "matplotlib")
    env["XDG_CACHE_HOME"] = str(runtime_root / "cache")
    return env


def _run(
    command: list[str],
    *,
    cwd: Path,
    env: dict[str, str],
    timeout: int = 600,
) -> subprocess.CompletedProcess[str]:
    """Run one visible candidate-family validation command."""
    print(f"+ {shlex.join(command)}", flush=True)
    return subprocess.run(
        command,
        cwd=cwd,
        env=env,
        check=True,
        text=True,
        timeout=timeout,
    )


def _prepare_artifacts_dir(path: Path, *, overwrite: bool) -> Path:
    """Create a bounded persistent output directory for candidate evidence."""
    resolved = path.expanduser().resolve()
    artifacts_root = ARTIFACTS_ROOT.resolve()
    if not resolved.is_relative_to(artifacts_root) or resolved == artifacts_root:
        raise ValueError(f"Artifacts directory must be a child of {artifacts_root}.")
    if resolved.exists():
        if not overwrite:
            raise ValueError(f"Artifacts directory already exists: {resolved}")
        shutil.rmtree(resolved)
    resolved.mkdir(parents=True)
    return resolved


def _verify_installed_family(
    python: Path,
    wheels: dict[str, Path],
    *,
    cwd: Path,
    env: dict[str, str],
) -> None:
    """Verify versions, import locations, and direct-wheel installation records."""
    probe = """
import importlib
import importlib.metadata
import json
payload = {{}}
for distribution_name, module_name in json.loads({mapping!r}).items():
    distribution = importlib.metadata.distribution(distribution_name)
    module = importlib.import_module(module_name)
    payload[distribution_name] = {{
        "version": distribution.version,
        "module_file": module.__file__,
        "direct_url": json.loads(distribution.read_text("direct_url.json") or "null"),
    }}
print(json.dumps(payload, sort_keys=True))
""".format(
        mapping=json.dumps(
            {name: module_name for name, (_version, module_name) in EXPECTED_DISTRIBUTIONS.items()}
        )
    )
    completed = subprocess.run(
        [str(python), "-c", probe],
        cwd=cwd,
        env=env,
        check=True,
        capture_output=True,
        text=True,
        timeout=60,
    )
    payload = json.loads(completed.stdout)
    for name, (expected_version, _module_name) in EXPECTED_DISTRIBUTIONS.items():
        installed = payload[name]
        if installed["version"] != expected_version:
            raise RuntimeError(
                f"Installed {name}=={installed['version']}; expected {expected_version}."
            )
        module_path = Path(installed["module_file"]).resolve()
        if "site-packages" not in module_path.parts:
            raise RuntimeError(f"{name} imported outside site-packages: {module_path}")
        direct_url = installed["direct_url"] or {}
        if not str(direct_url.get("url", "")).endswith(wheels[name].name):
            raise RuntimeError(f"{name} was not installed from {wheels[name]}.")
    print("Verified five installed candidate distributions and wheel origins.", flush=True)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wheelhouse", type=Path, required=True)
    parser.add_argument(
        "--artifacts-dir",
        type=Path,
        default=ARTIFACTS_ROOT / "candidate-family",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="replace an existing bounded candidate-family artifacts directory",
    )
    return parser.parse_args()


def main() -> int:
    """Install and exercise the coordinated candidate family."""
    args = parse_args()
    if sys.version_info[:2] != (3, 12):
        raise RuntimeError("Candidate-family validation requires Python 3.12 exactly.")
    if shutil.which("tectonic") is None:
        raise RuntimeError("Candidate-family validation requires Tectonic on PATH.")

    wheels = discover_candidate_wheels(args.wheelhouse.expanduser().resolve())
    artifacts_dir = _prepare_artifacts_dir(args.artifacts_dir, overwrite=args.overwrite)
    print("Candidate wheels:", flush=True)
    for name in EXPECTED_DISTRIBUTIONS:
        print(f"  {name}=={EXPECTED_DISTRIBUTIONS[name][0]}: {wheels[name]}", flush=True)

    with tempfile.TemporaryDirectory(prefix="design-research-candidate-") as temp_dir:
        runtime_root = Path(temp_dir)
        venv_dir = runtime_root / "venv"
        subprocess.run(
            [sys.executable, "-m", "venv", str(venv_dir)],
            check=True,
            timeout=120,
        )
        python = venv_dir / "bin" / "python"
        env = _clean_environment(runtime_root)
        install_requirements = [
            str(wheels["design-research-problems"]),
            str(wheels["design-research-agents"]),
            str(wheels["design-research-experiments"]),
            f"{wheels['design-research-analysis']}[stats]",
            f"{wheels['design-research']}[dev]",
        ]
        _run(
            [str(python), "-m", "pip", "install", *install_requirements],
            cwd=runtime_root,
            env=env,
            timeout=900,
        )
        _verify_installed_family(python, wheels, cwd=runtime_root, env=env)
        _run(
            [
                str(python),
                "-m",
                "pytest",
                "-q",
                "tests/test_family_smoke.py",
                "tests/test_paper_draft_acceptance.py",
            ],
            cwd=REPO_ROOT,
            env=env,
            timeout=900,
        )

        for script_name in PAPER_EXAMPLES:
            output_dir = artifacts_dir / script_name.removesuffix(".py")
            _run(
                [
                    str(python),
                    str(REPO_ROOT / "examples" / script_name),
                    "--output-dir",
                    str(output_dir),
                    "--require-tectonic",
                ],
                cwd=artifacts_dir,
                env=env,
                timeout=300,
            )
            required_outputs = (
                output_dir / "paper-draft" / "main.pdf",
                output_dir / "study-paper-draft.zip",
            )
            if not all(path.is_file() for path in required_outputs):
                raise RuntimeError(f"{script_name} did not produce its compiled draft and bundle.")

    print(f"Candidate-family validation passed. Evidence: {artifacts_dir}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
