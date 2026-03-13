# -*- coding: utf-8 -*-
"""Configuration for DataHaven CLI."""
import os
from pathlib import Path

# Base path: parent of datahaven-cli (repo root)
DEFAULT_PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROJECT_ROOT = Path(os.environ.get("DATAHAVEN_PROJECT_ROOT", str(DEFAULT_PROJECT_ROOT)))

# Paths relative to project root (as in README)
PATHS = {
    "test": PROJECT_ROOT / "test",
    "contracts": PROJECT_ROOT / "contracts",
    "operator": PROJECT_ROOT / "operator",
    "deploy": PROJECT_ROOT / "deploy",
    "tools": PROJECT_ROOT / "tools",
}

# Optional env for CI
INJECT_CONTRACTS = os.environ.get("INJECT_CONTRACTS", "false").lower() == "true"
