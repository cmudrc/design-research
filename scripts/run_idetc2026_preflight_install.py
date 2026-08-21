"""Exercise the workshop participant install in a clean temporary directory."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.request import urlretrieve

REPO_ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = REPO_ROOT / "docs" / "_static"


def run(command: list[str], *, cwd: Path) -> None:
    """Run one participant command and fail immediately on an error."""
    subprocess.run(command, cwd=cwd, check=True)


def main() -> int:
    """Create a clean environment, install the public requirements, and preflight it."""
    with tempfile.TemporaryDirectory(prefix="workshop-preflight-") as temporary:
        setup_dir = Path(temporary) / "design-research-workshop"
        setup_dir.mkdir()
        urlretrieve(
            (ASSET_ROOT / "workshop-requirements.txt").as_uri(),
            setup_dir / "requirements.txt",
        )
        urlretrieve(
            (ASSET_ROOT / "workshop-preflight.py").as_uri(),
            setup_dir / "preflight.py",
        )

        environment_dir = setup_dir / ".venv"
        run([sys.executable, "-m", "venv", str(environment_dir)], cwd=setup_dir)
        python = environment_dir / ("Scripts/python.exe" if os.name == "nt" else "bin/python")

        run([str(python), "-m", "pip", "install", "--upgrade", "pip"], cwd=setup_dir)
        run([str(python), "-m", "pip", "install", "-r", "requirements.txt"], cwd=setup_dir)
        run([str(python), "preflight.py"], cwd=setup_dir)

    print("Clean workshop participant preflight passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
