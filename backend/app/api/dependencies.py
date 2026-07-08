from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.repositories.sqlalchemy.application_repo import SqlAlchemyApplicationRepository
from app.repositories.sqlalchemy.recruiter_repo import SqlAlchemyRecruiterRepository
from app.repositories.sqlalchemy.update_repo import SqlAlchemyUpdateRepository
from app.services.application_service import ApplicationService


async def get_session(session: AsyncSession = Depends(get_db_session)) -> AsyncSession:
    return session


async def get_application_service(
    session: AsyncSession = Depends(get_session),
) -> ApplicationService:
    app_repo = SqlAlchemyApplicationRepository(session)
    recruiter_repo = SqlAlchemyRecruiterRepository(session)
    update_repo = SqlAlchemyUpdateRepository()
    return ApplicationService(app_repo, recruiter_repo, update_repo)
