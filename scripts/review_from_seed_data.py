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

from app.services.ai_reviewer import AIReviewOutput, AIReviewer


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Load a seed application JSON file, run AI screening evaluation, "
            "and print AIReviewOutput as JSON."
        )
    )
    parser.add_argument(
        "seed_file",
        type=Path,
        help="Path to a seed application JSON file (for example scripts/db/seed_data/jane_doe.json)",
    )
    return parser.parse_args()


def _pick(data: dict, snake_key: str, camel_key: str) -> str | None:
    value = data.get(snake_key)
    if value is None:
        value = data.get(camel_key)
    if isinstance(value, str):
        value = value.strip()
    return value or None


def _build_review_prompt(application_data: dict) -> str:
    first_name = _pick(application_data, "first_name", "firstName") or ""
    last_name = _pick(application_data, "last_name", "lastName") or ""
    email = _pick(application_data, "email", "email") or ""
    job_title = _pick(application_data, "job_title", "jobTitle") or ""
    seniority = _pick(application_data, "seniority_level", "seniorityLevel") or ""
    linkedin_url = _pick(application_data, "linkedin_url", "linkedinUrl") or ""
    department = _pick(application_data, "department", "department") or ""
    region = _pick(application_data, "region", "region") or ""

    company = application_data.get("company") or {}
    company_name = _pick(company, "name", "name") or ""
    company_site = _pick(company, "site_url", "siteUrl") or ""
    company_type = _pick(company, "type", "type") or ""

    app_id = _pick(application_data, "id", "id") or "seed-data"
    updates = application_data.get("updates")
    updates_count = len(updates) if isinstance(updates, list) else 0

    return (
        f"Application ID: {app_id}\n"
        f"Candidate: {first_name} {last_name}\n"
        f"Email: {email}\n"
        f"Job title: {job_title}\n"
        f"Seniority: {seniority}\n"
        f"Company: {company_name}\n"
        f"Company site: {company_site}\n"
        f"Company type: {company_type}\n"
        f"LinkedIn URL: {linkedin_url}\n"
        f"Department: {department}\n"
        f"Region: {region}\n"
        f"Number of prior updates: {updates_count}\n"
        "\nPlease screen this candidate using the screen_candidate skill."
    )


async def _run(seed_file: Path) -> int:
    if not seed_file.exists() or not seed_file.is_file():
        print(f"ERROR: Seed file not found: {seed_file}", file=sys.stderr)
        return 1

    with seed_file.open(encoding="utf-8") as file:
        application_data = json.load(file)

    reviewer = AIReviewer()
    prompt = _build_review_prompt(application_data)
    result = await reviewer.run(prompt)
    output: AIReviewOutput = result.output

    print(output.model_dump_json(indent=2))
    return 0


def main() -> None:
    args = _parse_args()
    exit_code = asyncio.run(_run(args.seed_file))
    raise SystemExit(exit_code)


if __name__ == "__main__":
    main()
