#!/usr/bin/env python3

import argparse
import asyncio
import json
import sys
from pathlib import Path

from dotenv import load_dotenv


REPO_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = REPO_ROOT / "backend"
TRACE_LOG_PATH = REPO_ROOT / "logs" / "agent_traces.jsonl"
sys.path.insert(0, str(BACKEND_DIR))

load_dotenv(REPO_ROOT / ".env")

from agent.logging import configure_agent_logging

configure_agent_logging(TRACE_LOG_PATH)

from app.services.linked_in_retriever import get_linkedin_profile


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Load a seed application JSON file, resolve LinkedIn profile data, "
            "and print formatted profile markdown."
        )
    )
    parser.add_argument(
        "seed_file",
        type=Path,
        help="Path to a seed application JSON file (for example scripts/db/seed_data/jane_doe.json)",
    )
    return parser.parse_args()


def _pick(application_data: dict, snake_key: str, camel_key: str) -> str | None:
    value = application_data.get(snake_key)
    if value is None:
        value = application_data.get(camel_key)
    if isinstance(value, str):
        value = value.strip()
    return value or None


async def _run(seed_file: Path) -> int:
    if not seed_file.exists() or not seed_file.is_file():
        print(f"ERROR: Seed file not found: {seed_file}", file=sys.stderr)
        return 1

    with seed_file.open(encoding="utf-8") as file:
        application_data = json.load(file)

    first_name = _pick(application_data, "first_name", "firstName")
    last_name = _pick(application_data, "last_name", "lastName")
    company = application_data.get("company") or {}
    company_name = _pick(company, "name", "name")
    company_url = _pick(company, "site_url", "siteUrl")

    if not first_name or not last_name:
        print(
            "ERROR: Seed file is missing candidate name fields (first_name/last_name or firstName/lastName).",
            file=sys.stderr,
        )
        return 2

    markdown = await get_linkedin_profile(
        first_name=first_name,
        last_name=last_name,
        company_name=company_name,
        company_url=company_url,
        message_history=None,
    )

    if markdown.startswith("ERROR:"):
        print(markdown, file=sys.stderr)
        return 2

    print(markdown)
    return 0


def main() -> None:
    args = _parse_args()
    exit_code = asyncio.run(_run(args.seed_file))
    raise SystemExit(exit_code)


if __name__ == "__main__":
    main()
