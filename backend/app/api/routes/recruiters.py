from fastapi import APIRouter, Depends

from app.api.dependencies import get_application_service
from app.schemas.recruiter import Recruiter
from app.services.application_service import ApplicationService

router = APIRouter(prefix="/api/recruiters", tags=["recruiters"])


@router.get("", response_model=list[Recruiter])
async def get_recruiters(
    service: ApplicationService = Depends(get_application_service),
) -> list[Recruiter]:
    recruiters = await service.list_recruiters()
    return [Recruiter(**recruiter) for recruiter in recruiters]
