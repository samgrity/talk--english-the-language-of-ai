from fastapi import APIRouter, Depends

from app.api.dependencies import get_application_service
from app.schemas.hooks import (
    CandidateCorrespondenceHookRequest,
    TriggerAIScreenHookRequest,
)
from app.services.application_service import ApplicationService

router = APIRouter(prefix="/api/hooks", tags=["hooks"])


@router.post("/email/candidate-message")
async def ingest_candidate_message(
    request: CandidateCorrespondenceHookRequest,
    service: ApplicationService = Depends(get_application_service),
) -> dict[str, str | bool]:
    return await service.ingest_candidate_message(
        application_id=request.application_id,
        correspondence=request.correspondence,
    )


@router.post("/applications/trigger-ai-screen")
async def trigger_ai_screen(
    request: TriggerAIScreenHookRequest,
    service: ApplicationService = Depends(get_application_service),
) -> dict[str, str | bool]:
    return await service.trigger_ai_screen(request.application_id)
