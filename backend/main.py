"""Compatibility entrypoint for uvicorn main:app."""

import os
from pathlib import Path

# Load .env from the repo root before any app modules are imported.
# If ANTHROPIC_API_KEY is not present after this, AIReviewer instantiation
# will raise immediately and the process will not start.
_env_file = Path(__file__).resolve().parents[1] / ".env"
if _env_file.exists():
    for _line in _env_file.read_text().splitlines():
        _line = _line.strip()
        if _line and not _line.startswith("#") and "=" in _line:
            _key, _, _val = _line.partition("=")
            os.environ.setdefault(_key.strip(), _val.strip())

from agent.logging import configure_agent_logging
configure_agent_logging()

from app.main import app
