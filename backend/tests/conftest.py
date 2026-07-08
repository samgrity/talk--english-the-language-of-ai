import asyncio
import contextlib
import os
import sys
from pathlib import Path

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from pydantic_ai.capabilities.combined import CombinedCapability
from pydantic_ai._utils import Some

REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = REPO_ROOT / "backend"
TEST_DB_PATH = BACKEND_ROOT / "test_hireflow.db"
sys.path.insert(0, str(BACKEND_ROOT))
sys.path.insert(0, str(REPO_ROOT / "scripts" / "db"))
    
os.environ.setdefault("TESTING", "true")
os.environ.setdefault("ANTHROPIC_API_KEY", "test-dummy-key")
os.environ.setdefault("AI_MODEL", "anthropic:claude-sonnet-4-6")
os.environ["DATABASE_URL"] = f"sqlite+aiosqlite:///{TEST_DB_PATH}"

from app.db.session import SessionLocal
from main import app
from reinitialize_db import reinitialize_database


@pytest.fixture(autouse=True)
def reset_database() -> None:
    asyncio.run(reinitialize_database())


@pytest.fixture
def client() -> TestClient:
    with TestClient(app) as api_client:
        yield api_client


@pytest_asyncio.fixture
async def db_session():
    async with SessionLocal() as session:
        yield session


@contextlib.contextmanager
def override_no_capabilities(agent):
    """Temporarily strip all capabilities from *agent*.

    Needed in tests that use TestModel, which rejects built-in tools
    (WebSearch, WebFetch, Thinking all register as built-in tools).
    """
    token = agent._override_root_capability.set(Some(CombinedCapability([])))
    try:
        yield
    finally:
        agent._override_root_capability.reset(token)
