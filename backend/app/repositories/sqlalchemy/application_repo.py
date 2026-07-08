from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func
from sqlalchemy.orm import selectinload

from app.core.enums import FilterStatus
from app.db.models.application import ApplicationModel
from app.db.models.company import CompanyModel
from app.db.models.recruiter import RecruiterModel


class SqlAlchemyApplicationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_all(
        self,
        filter_status: FilterStatus,
        search: str | None,
        assignee_id: str | None,
    ) -> list[ApplicationModel]:
        statement = (
            select(ApplicationModel)
            .join(CompanyModel, ApplicationModel.company_id == CompanyModel.id)
            .outerjoin(RecruiterModel, ApplicationModel.assignee_id == RecruiterModel.id)
            .options(
                selectinload(ApplicationModel.company),
                selectinload(ApplicationModel.updates),
            )
        )

        pending_statuses = ["waiting_for_recruiter", "waiting_for_ai", "waiting_for_candidate"]
        completed_statuses = ["advanced", "declined", "withdrawn"]

        if filter_status == FilterStatus.PENDING:
            statement = statement.where(ApplicationModel.screening_status.in_(pending_statuses))
        elif filter_status == FilterStatus.COMPLETED:
            statement = statement.where(ApplicationModel.screening_status.in_(completed_statuses))
        elif filter_status == FilterStatus.WITHDRAWN:
            statement = statement.where(ApplicationModel.screening_status == "withdrawn")
        elif filter_status in {
            FilterStatus.WAITING_FOR_RECRUITER,
            FilterStatus.WAITING_FOR_AI,
            FilterStatus.WAITING_FOR_CANDIDATE,
            FilterStatus.ADVANCED,
            FilterStatus.DECLINED,
        }:
            statement = statement.where(ApplicationModel.screening_status == filter_status.value)

        if assignee_id:
            statement = statement.where(ApplicationModel.assignee_id == assignee_id)

        if search and search.strip():
            search_term = f"%{search.strip().lower()}%"
            full_name = func.lower(ApplicationModel.first_name + " " + ApplicationModel.last_name)
            statement = statement.where(
                or_(
                    full_name.like(search_term),
                    func.lower(ApplicationModel.email).like(search_term),
                    func.lower(CompanyModel.name).like(search_term),
                    func.lower(ApplicationModel.job_title).like(search_term),
                    func.lower(ApplicationModel.department).like(search_term),
                    func.lower(func.coalesce(ApplicationModel.region, "")).like(search_term),
                    func.lower(func.coalesce(RecruiterModel.name, "unassigned")).like(search_term),
                )
            )

        result = await self.session.execute(statement)
        return list(result.scalars().unique().all())

    async def get_by_id(self, application_id: str) -> ApplicationModel | None:
        statement = (
            select(ApplicationModel)
            .where(ApplicationModel.id == application_id)
            .options(
                selectinload(ApplicationModel.company),
                selectinload(ApplicationModel.updates),
            )
        )
        result = await self.session.execute(statement)
        return result.scalars().first()

    async def update(self, application: ApplicationModel) -> None:
        self.session.add(application)
        await self.session.commit()
        await self.session.refresh(application)
