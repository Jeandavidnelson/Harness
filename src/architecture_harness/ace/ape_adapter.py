from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


def ape_available() -> bool:
    return shutil.which("ape") is not None


def validate_with_ape(path: Path) -> dict[str, object]:
    executable = shutil.which("ape")
    if not executable:
        return {"status": "UNAVAILABLE", "parse": "NOT_RUN", "reason": "APE executable not installed"}
    process = subprocess.run([executable, str(path)], text=True, capture_output=True)
    return {
        "status": "AVAILABLE",
        "parse": "PASS" if process.returncode == 0 else "FAIL",
        "returncode": process.returncode,
        "stdout": process.stdout,
        "stderr": process.stderr,
    }

