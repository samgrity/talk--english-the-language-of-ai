import pytest
from fastapi import HTTPException
from pydantic_ai.models.test import TestModel

from app.core.enums import FilterStatus, UpdateActor, UpdateType
from app.repositories.sqlalchemy.application_repo import SqlAlchemyApplicationRepository
from app.repositories.sqlalchemy.recruiter_repo import SqlAlchemyRecruiterRepository
from app.repositories.sqlalchemy.update_repo import SqlAlchemyUpdateRepository
from app.services.application_service import ApplicationService, ai_reviewer
from tests.conftest import override_no_capabilities


@pytest.mark.asyncio
async def test_add_update_follow_up_moves_status(db_session):
    outbound_calls: list[tuple[str, str, str]] = []

    async def fake_sender(application_id: str, recruiter_id: str, correspondence: str) -> None:
        outbound_calls.append((application_id, recruiter_id, correspondence))

    service = ApplicationService(
        SqlAlchemyApplicationRepository(db_session),
        SqlAlchemyRecruiterRepository(db_session),
        SqlAlchemyUpdateRepository(),
        correspondence_sender=fake_sender,
    )

    apps = await service.list_applications(FilterStatus.ALL, None, None)
    app_id = apps[0].id

    result = await service.add_update(
        application_id=app_id,
        actor=UpdateActor.HUMAN_RECRUITER,
        update_type=UpdateType.FOLLOW_UP,
        internal_notes="Need one more document",
        recruiter_id="rev1",
        correspondence="Please send your missing document.",
    )
    assert result["success"] is True

    updated = await service.get_application(app_id)
    assert updated.screeningStatus == "waiting_for_candidate"
    assert updated.updates[-1].recruiter_id == "rev1"
    assert outbound_calls[-1] == (app_id, "rev1", "Please send your missing document.")


@pytest.mark.asyncio
async def test_add_update_follow_up_requires_correspondence(db_session):
    service = ApplicationService(
        SqlAlchemyApplicationRepository(db_session),
        SqlAlchemyRecruiterRepository(db_session),
        SqlAlchemyUpdateRepository(),
    )

    app_id = (await service.list_applications(FilterStatus.ALL, None, None))[0].id

    with pytest.raises(HTTPException) as exc_info:
        await service.add_update(
            application_id=app_id,
            actor=UpdateActor.HUMAN_RECRUITER,
            update_type=UpdateType.FOLLOW_UP,
            internal_notes="Need one more document",
            recruiter_id="rev1",
            correspondence="   ",
        )

    assert exc_info.value.status_code == 400


@pytest.mark.asyncio
async def test_add_update_advance_marks_application_advanced(db_session):
    service = ApplicationService(
        SqlAlchemyApplicationRepository(db_session),
        SqlAlchemyRecruiterRepository(db_session),
        SqlAlchemyUpdateRepository(),
    )

    app_id = (await service.list_applications(FilterStatus.ALL, None, None))[0].id
    result = await service.add_update(
        application_id=app_id,
        actor=UpdateActor.HUMAN_RECRUITER,
        update_type=UpdateType.ADVANCE,
        internal_notes="Looks good to advance",
        recruiter_id="rev1",
        correspondence=None,
    )

    assert result["success"] is True
    updated = await service.get_application(app_id)
    assert updated.screeningStatus == "advanced"


@pytest.mark.asyncio
async def test_add_update_rejects_invalid_recruiter(db_session):
    service = ApplicationService(
        SqlAlchemyApplicationRepository(db_session),
        SqlAlchemyRecruiterRepository(db_session),
        SqlAlchemyUpdateRepository(),
    )

    apps = await service.list_applications(FilterStatus.ALL, None, None)
    app_id = apps[0].id

    with pytest.raises(HTTPException) as exc_info:
        await service.add_update(
            application_id=app_id,
            actor=UpdateActor.HUMAN_RECRUITER,
            update_type=UpdateType.GENERAL_UPDATE,
            internal_notes="Invalid recruiter",
            recruiter_id="invalid",
        )

    assert exc_info.value.status_code == 400


@pytest.mark.asyncio
async def test_ingest_candidate_message_sets_waiting_for_ai_and_triggers_agent(db_session):
    service = ApplicationService(
        SqlAlchemyApplicationRepository(db_session),
        SqlAlchemyRecruiterRepository(db_session),
        SqlAlchemyUpdateRepository(),
    )

    app_id = (await service.list_applications(FilterStatus.ALL, None, None))[0].id
    with ai_reviewer.override(model=TestModel(call_tools=[])), override_no_capabilities(ai_reviewer):
        result = await service.ingest_candidate_message(
            application_id=app_id,
            correspondence="Here is my updated information.",
        )

    assert result["success"] is True
    updated = await service.get_application(app_id)
    assert updated.screeningStatus == "waiting_for_recruiter"
    assert updated.updates[-1].actor == "ai_agent"


@pytest.mark.asyncio
async def test_candidate_update_rejects_internal_notes(db_session):
    service = ApplicationService(
        SqlAlchemyApplicationRepository(db_session),
        SqlAlchemyRecruiterRepository(db_session),
        SqlAlchemyUpdateRepository(),
    )

    app_id = (await service.list_applications(FilterStatus.ALL, None, None))[0].id

    with pytest.raises(HTTPException) as exc_info:
        await service.add_update(
            application_id=app_id,
            actor=UpdateActor.CANDIDATE,
            update_type=UpdateType.GENERAL_UPDATE,
            internal_notes="Candidate side note",
            correspondence="Here is an update from the candidate.",
            recruiter_id=None,
        )

    assert exc_info.value.status_code == 400


@pytest.mark.asyncio
async def test_add_ai_update_sets_waiting_for_recruiter(db_session):
    service = ApplicationService(
        SqlAlchemyApplicationRepository(db_session),
        SqlAlchemyRecruiterRepository(db_session),
        SqlAlchemyUpdateRepository(),
    )

    app_id = (await service.list_applications(FilterStatus.ALL, None, None))[0].id
    result = await service.add_update(
        application_id=app_id,
        actor=UpdateActor.AI_AGENT,
        update_type=UpdateType.RECOMMEND_FOLLOW_UP,
        internal_notes="Random mock notes",
        correspondence="Random mock correspondence",
        recruiter_id=None,
    )

    assert result["success"] is True
    updated = await service.get_application(app_id)
    assert updated.screeningStatus == "waiting_for_recruiter"
    assert updated.updates[-1].actor == "ai_agent"


@pytest.mark.asyncio
async def test_request_ai_screen_adds_update_and_triggers_ai_screen(db_session):
    service = ApplicationService(
        SqlAlchemyApplicationRepository(db_session),
        SqlAlchemyRecruiterRepository(db_session),
        SqlAlchemyUpdateRepository(),
    )

    app_id = (await service.list_applications(FilterStatus.ALL, None, None))[0].id
    with ai_reviewer.override(model=TestModel(call_tools=[])), override_no_capabilities(ai_reviewer):
        result = await service.add_update(
            application_id=app_id,
            actor=UpdateActor.HUMAN_RECRUITER,
            update_type=UpdateType.REQUEST_AI_SCREEN,
            internal_notes="Need an updated AI recommendation after edits",
            recruiter_id="rev1",
            correspondence=None,
        )

    assert result["success"] is True
    updated = await service.get_application(app_id)
    assert updated.screeningStatus == "waiting_for_recruiter"
    assert updated.updates[-2].actor == "human_recruiter"
    assert updated.updates[-2].update_type == "request_ai_screen"
    assert updated.updates[-1].actor == "ai_agent"


@pytest.mark.asyncio
async def test_recruiter_cannot_submit_recommendation_update_type(db_session):
    service = ApplicationService(
        SqlAlchemyApplicationRepository(db_session),
        SqlAlchemyRecruiterRepository(db_session),
        SqlAlchemyUpdateRepository(),
    )

    app_id = (await service.list_applications(FilterStatus.ALL, None, None))[0].id

    with pytest.raises(HTTPException) as exc_info:
        await service.add_update(
            application_id=app_id,
            actor=UpdateActor.HUMAN_RECRUITER,
            update_type=UpdateType.RECOMMEND_FOLLOW_UP,
            internal_notes="Should not be allowed",
            recruiter_id="rev1",
            correspondence="Not valid",
        )

    assert exc_info.value.status_code == 400


@pytest.mark.asyncio
async def test_ai_cannot_submit_recruiter_decision_update_type(db_session):
    service = ApplicationService(
        SqlAlchemyApplicationRepository(db_session),
        SqlAlchemyRecruiterRepository(db_session),
        SqlAlchemyUpdateRepository(),
    )

    app_id = (await service.list_applications(FilterStatus.ALL, None, None))[0].id

    with pytest.raises(HTTPException) as exc_info:
        await service.add_update(
            application_id=app_id,
            actor=UpdateActor.AI_AGENT,
            update_type=UpdateType.ADVANCE,
            internal_notes="Should not be allowed",
            recruiter_id=None,
            correspondence="n/a",
        )

    assert exc_info.value.status_code == 400
