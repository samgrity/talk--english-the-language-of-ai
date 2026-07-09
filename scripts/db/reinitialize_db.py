#!/usr/bin/env python3

import asyncio
import json
import sys
from copy import deepcopy
from datetime import datetime
from pathlib import Path

from sqlalchemy import delete

REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND_DIR = REPO_ROOT / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from app.db.base import Base
from app.db.models.application import ApplicationModel
from app.db.models.company import CompanyModel
from app.db.models.recruiter import RecruiterModel
from app.db.models.update import UpdateModel
from app.db.session import SessionLocal, engine

SEED_RECRUITERS = [
    {"id": "rev1", "name": "John Berryman"},
    {"id": "rev2", "name": "Josh Carter"},
    {"id": "rev3", "name": "Pete Mitchell"},
]

SEED_DATA_DIR = Path(__file__).resolve().parent / "seed_data"


def _parse_application_dates(application_data: dict) -> dict:
    app_entry = dict(application_data)
    app_entry["created_at"] = datetime.fromisoformat(app_entry["created_at"])
    app_entry["updated_at"] = datetime.fromisoformat(app_entry["updated_at"])

    updates = []
    for update in app_entry["updates"]:
        parsed_update = dict(update)
        parsed_update["timestamp"] = datetime.fromisoformat(parsed_update["timestamp"])
        updates.append(parsed_update)

    app_entry["updates"] = updates
    return app_entry


def _load_seed_applications() -> list[dict]:
    application_files = sorted(SEED_DATA_DIR.glob("*.json"))
    if not application_files:
        raise FileNotFoundError(f"No seed files found in {SEED_DATA_DIR}")

    applications = []
    for seed_file in application_files:
        with seed_file.open(encoding="utf-8") as file:
            app_data = json.load(file)
        applications.append(_parse_application_dates(app_data))

    return applications


SEED_APPLICATIONS = _load_seed_applications()


async def reinitialize_database() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    async with SessionLocal() as session:
        await session.execute(delete(UpdateModel))
        await session.execute(delete(ApplicationModel))
        await session.execute(delete(CompanyModel))
        await session.execute(delete(RecruiterModel))

        for recruiter_data in SEED_RECRUITERS:
            session.add(RecruiterModel(**recruiter_data))

        companies_by_id: dict[str, CompanyModel] = {}

        for app_data in SEED_APPLICATIONS:
            app_entry = deepcopy(app_data)
            job_opening_data = app_entry.pop("job_opening")
            company_data = job_opening_data.pop("company")
            locale_data = app_entry.pop("locale")
            updates_data = app_entry.pop("updates")

            company = companies_by_id.get(company_data["id"])
            if company is None:
                company = CompanyModel(**company_data)
                companies_by_id[company.id] = company
                session.add(company)

            application = ApplicationModel(
                **app_entry,
                job_title=job_opening_data["title"],
                seniority_level=job_opening_data["seniority_level"],
                department=job_opening_data["department"],
                sub_departments=job_opening_data["sub_departments"],
                job_description=job_opening_data["job_description"],
                company_id=company.id,
                locale_country=locale_data["country"],
                locale_preferred_language=locale_data["preferred_language"],
                locale_region=locale_data["region"],
                locale_store_id=locale_data["store_id"],
            )
            session.add(application)

            for update_data in updates_data:
                session.add(UpdateModel(application_id=application.id, **update_data))

        await session.commit()


def main() -> None:
    asyncio.run(reinitialize_database())
    print("Database reinitialized with seed data.")


if __name__ == "__main__":
    main()
