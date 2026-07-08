from fastapi import APIRouter, Depends

from app.api.dependencies import get_application_service
from app.core.enums import FilterStatus, UpdateActor
from app.schemas.application import (
    Application,
    ApplicationSummary,
    ApplicationUpdateRequest,
    NewUpdateRequest,
    StatusUpdateRequest,
)

DEFAULT_RECRUITER_ID = "rev1"
from app.services.application_service import ApplicationService

router = APIRouter(prefix="/api/applications", tags=["applications"])


@router.get("", response_model=list[ApplicationSummary])
async def get_applications(
    filter: FilterStatus = FilterStatus.PENDING,
    search: str | None = None,
    assignee_id: str | None = None,
    service: ApplicationService = Depends(get_application_service),
) -> list[ApplicationSummary]:
    return await service.list_applications(filter, search, assignee_id)


@router.get("/{application_id}", response_model=Application)
async def get_application(
    application_id: str,
    service: ApplicationService = Depends(get_application_service),
) -> Application:
    return await service.get_application(application_id)


@router.put("/{application_id}")
async def update_application(
    application_id: str,
    request: ApplicationUpdateRequest,
    service: ApplicationService = Depends(get_application_service),
) -> dict[str, str | bool]:
    return await service.update_application(application_id, request)


@router.put("/{application_id}/status")
async def update_application_status(
    application_id: str,
    request: StatusUpdateRequest,
    service: ApplicationService = Depends(get_application_service),
) -> dict[str, str | bool]:
    return await service.update_status(application_id, request)


@router.post("/{application_id}/updates")
async def add_update(
    application_id: str,
    request: NewUpdateRequest,
    service: ApplicationService = Depends(get_application_service),
) -> dict[str, str | bool]:
    return await service.add_update(
        application_id=application_id,
        actor=UpdateActor.HUMAN_RECRUITER,
        update_type=request.update_type,
        internal_notes=request.internal_notes,
        correspondence=request.correspondence,
        recruiter_id=request.recruiter_id or DEFAULT_RECRUITER_ID,
    )
