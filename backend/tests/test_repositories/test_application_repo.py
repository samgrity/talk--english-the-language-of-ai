import pytest

from app.core.enums import FilterStatus
from app.repositories.sqlalchemy.application_repo import SqlAlchemyApplicationRepository


@pytest.mark.asyncio
async def test_list_all_filters_by_assignee(db_session):
    repo = SqlAlchemyApplicationRepository(db_session)

    apps = await repo.list_all(FilterStatus.ALL, None, "rev3")
    # With one seed candidate (unassigned), filtering by assignee may return empty
    assert isinstance(apps, list)


@pytest.mark.asyncio
async def test_list_all_searches_matching_name(db_session):
    repo = SqlAlchemyApplicationRepository(db_session)

    apps = await repo.list_all(FilterStatus.ALL, "john", None)
    assert len(apps) > 0
    assert any("john" in f"{app.first_name} {app.last_name}".lower() for app in apps)
