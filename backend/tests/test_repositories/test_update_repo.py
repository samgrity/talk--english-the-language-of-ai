import pytest

from app.core.enums import FilterStatus
from app.core.enums import UpdateActor, UpdateType
from app.repositories.sqlalchemy.application_repo import SqlAlchemyApplicationRepository
from app.repositories.sqlalchemy.update_repo import SqlAlchemyUpdateRepository


@pytest.mark.asyncio
async def test_create_for_application_appends_update(db_session):
    app_repo = SqlAlchemyApplicationRepository(db_session)
    update_repo = SqlAlchemyUpdateRepository()

    app = (await app_repo.list_all(FilterStatus.ALL, None, None))[0]
    before_count = len(app.updates)

    update_repo.create_for_application(
        application=app,
        actor=UpdateActor.HUMAN_RECRUITER,
        update_type=UpdateType.GENERAL_UPDATE,
        internal_notes="Repository update append test",
        correspondence="Message to candidate",
        recruiter_id="rev1",
    )
    await app_repo.update(app)

    refreshed = await app_repo.get_by_id(app.id)
    assert refreshed is not None
    assert len(refreshed.updates) == before_count + 1
    assert refreshed.updates[-1].recruiter_id == "rev1"
    assert refreshed.updates[-1].update_type == UpdateType.GENERAL_UPDATE.value
