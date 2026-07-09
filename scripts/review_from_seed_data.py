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
        help="Path to a seed application JSON file (for example scripts/db/seed_data/john_berryman.json)",
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
    mobile = _pick(application_data, "mobile", "mobile") or ""
    bio = _pick(application_data, "bio", "bio") or ""
    linkedin_url = _pick(application_data, "linkedin_url", "linkedinUrl") or ""
    region = _pick(application_data, "region", "region") or ""

    job_opening = application_data.get("job_opening") or application_data.get("jobOpening") or {}
    job_title = _pick(job_opening, "title", "title") or _pick(application_data, "job_title", "jobTitle") or ""
    seniority = _pick(job_opening, "seniority_level", "seniorityLevel") or _pick(application_data, "seniority_level", "seniorityLevel") or ""
    department = _pick(job_opening, "department", "department") or _pick(application_data, "department", "department") or ""
    job_description = _pick(job_opening, "job_description", "jobDescription") or ""
    sub_departments = job_opening.get("sub_departments") or job_opening.get("subDepartments") or application_data.get("sub_departments") or application_data.get("subDepartments") or []

    company = job_opening.get("company") or application_data.get("company") or {}
    company_name = _pick(company, "name", "name") or ""
    company_site = _pick(company, "site_url", "siteUrl") or ""
    company_size = _pick(company, "size", "size") or ""

    app_id = _pick(application_data, "id", "id") or "seed-data"
    updates = application_data.get("updates")
    updates_count = len(updates) if isinstance(updates, list) else 0
    sub_department_text = ", ".join(sub_departments) if isinstance(sub_departments, list) else str(sub_departments)

    return (
        f"Application ID: {app_id}\n"
        f"Candidate: {first_name} {last_name}\n"
        f"Email: {email}\n"
        f"Phone: {mobile}\n"
        f"Bio: {bio}\n"
        f"LinkedIn URL: {linkedin_url}\n"
        f"Job opening title: {job_title}\n"
        f"Job opening seniority: {seniority}\n"
        f"Job opening department: {department}\n"
        f"Job opening sub-departments: {sub_department_text}\n"
        f"Job opening description: {job_description}\n"
        f"Hiring company: {company_name}\n"
        f"Hiring company site: {company_site}\n"
        f"Hiring company size: {company_size}\n"
        f"Candidate region: {region}\n"
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
