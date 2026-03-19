from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def get_project_root() -> Path:
    # server/misc/config_loader.py -> parents[2] == repo root (shawarmys)
    return Path(__file__).resolve().parents[2]


# Fixed location inside repo
FINGERPRINTS_DIR = get_project_root() / "server" / "misc" / "config" / "goldFingerPrints"


def load_fingerprints() -> dict[str, dict[str, Any]]:
    """
    Load all fingerprint JSON files from the fixed repo folder.

    Returns:
        dict keyed by filename stem, e.g.:
        {
          "synthetic_cases_icd10_ops_fingerprint": {...},
          "target_table_fingerprint": {...}
        }
    """
    if not FINGERPRINTS_DIR.exists():
        raise FileNotFoundError(f"Fingerprint directory not found: {FINGERPRINTS_DIR}")

    files = sorted(FINGERPRINTS_DIR.glob("*.json"))
    if not files:
        raise FileNotFoundError(f"No fingerprint JSON files found in: {FINGERPRINTS_DIR}")

    fingerprints: dict[str, dict[str, Any]] = {}
    for file_path in files:
        with file_path.open("r", encoding="utf-8") as f:
            fingerprints[file_path.stem] = json.load(f)

    return fingerprints
