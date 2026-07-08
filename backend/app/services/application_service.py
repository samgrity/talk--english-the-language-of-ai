from datetime import datetime
from enum import Enum
from typing import Awaitable, Callable, Protocol

from fastapi import HTTPException

from app.services.ai_reviewer import AIReviewOutput, AIReviewer
from app.core.enums import FilterStatus, SubDepartment, UpdateActor, UpdateType
from app.db.models.application import ApplicationModel
from app.integrations.email_service import send_recruiter_message_to_candidate
from app.repositories.application_repository import ApplicationRepository
from app.repositories.recruiter_repository import RecruiterRepository
from app.repositories.update_repository import UpdateRepository
from app.schemas.application import (
    Address,
    Application,
    ApplicationSummary,
    ApplicationUpdateRequest,
    Company,
    LocaleInfo,
    StatusUpdateRequest,
    Update,
)


class AgentApplicationService(Protocol):
    async def get_application(self, application_id: str): ...

    async def add_update(
        self,
        application_id: str,
        actor: UpdateActor,
        update_type: UpdateType,
        internal_notes: str,
        correspondence: str | None,
        recruiter_id: str | None,
    ) -> dict[str, str | bool]: ...


class AIReviewerProtocol(Protocol):
    async def review(self, application_id: str, service: AgentApplicationService) -> None: ...


# Module-level singleton – shared across all requests.
# Requires ANTHROPIC_API_KEY to be set in the environment (loaded from .env at startup).
# Use `with ai_reviewer.override(model=TestModel(...)):` in tests.
ai_reviewer = AIReviewer()


class ApplicationService:
    RECRUITER_ALLOWED_UPDATE_TYPES = {
        UpdateType.ADVANCE,
        UpdateType.DECLINE,
        UpdateType.FOLLOW_UP,
        UpdateType.REQUEST_AI_SCREEN,
        UpdateType.GENERAL_UPDATE,
        UpdateType.WITHDRAW,
    }
    AI_ALLOWED_UPDATE_TYPES = {
        UpdateType.RECOMMEND_ADVANCE,
        UpdateType.RECOMMEND_DECLINE,
        UpdateType.RECOMMEND_FOLLOW_UP,
    }
    CANDIDATE_ALLOWED_UPDATE_TYPES = {UpdateType.GENERAL_UPDATE}

    def __init__(
        self,
        app_repo: ApplicationRepository,
        recruiter_repo: RecruiterRepository,
        update_repo: UpdateRepository,
        correspondence_sender: Callable[[str, str, str], Awaitable[None]] = send_recruiter_message_to_candidate,
    ):
        self.app_repo = app_repo
        self.recruiter_repo = recruiter_repo
        self.update_repo = update_repo
        self.correspondence_sender = correspondence_sender
        self.ai_reviewer = ai_reviewer

    async def list_applications(
        self, filter_status: FilterStatus, search: str | None, assignee_id: str | None
    ) -> list[ApplicationSummary]:
        applications = await self.app_repo.list_all(filter_status, search, assignee_id)
        assignee_names = await self.recruiter_repo.get_name_map()
        ordered = self._order_applications(applications)
        return [self._to_summary(app, assignee_names) for app in ordered]

    async def get_application(self, application_id: str) -> Application:
        app = await self.app_repo.get_by_id(application_id)
        if not app:
            raise HTTPException(status_code=404, detail="Application not found")
        return self._to_detail(app)

    async def update_application(
        self, application_id: str, request: ApplicationUpdateRequest
    ) -> dict[str, str | bool]:
        app = await self.app_repo.get_by_id(application_id)
        if not app:
            raise HTTPException(status_code=404, detail="Application not found")

        updates = request.model_dump(exclude_none=True)
        for key, value in updates.items():
            self._apply_update(app, key, value)
        app.updated_at = datetime.now()
        await self.app_repo.update(app)
        return {"success": True, "message": "Application updated successfully"}

    async def update_status(
        self, application_id: str, request: StatusUpdateRequest
    ) -> dict[str, str | bool]:
        app = await self.app_repo.get_by_id(application_id)
        if not app:
            raise HTTPException(status_code=404, detail="Application not found")
        app.screening_status = request.status
        app.updated_at = datetime.now()
        await self.app_repo.update(app)
        return {"success": True, "message": "Status updated successfully"}

    async def add_update(
        self,
        application_id: str,
        actor: UpdateActor,
        update_type: UpdateType,
        internal_notes: str,
        correspondence: str | None = None,
        recruiter_id: str | None = None,
    ) -> dict[str, str | bool]:
        app = await self.app_repo.get_by_id(application_id)
        if not app:
            raise HTTPException(status_code=404, detail="Application not found")

        if actor == UpdateActor.HUMAN_RECRUITER:
            return await self._add_recruiter_update(
                app,
                update_type,
                internal_notes,
                correspondence,
                recruiter_id,
            )

        if actor == UpdateActor.AI_AGENT:
            return await self._add_ai_update(
                app,
                update_type,
                internal_notes,
                correspondence,
            )

        if actor == UpdateActor.CANDIDATE:
            return await self._add_candidate_update(
                app,
                update_type,
                internal_notes,
                correspondence,
            )

        raise HTTPException(status_code=400, detail="Unsupported actor")

    async def _add_recruiter_update(
        self,
        app: ApplicationModel,
        update_type: UpdateType,
        internal_notes: str,
        correspondence: str | None,
        recruiter_id: str | None,
    ) -> dict[str, str | bool]:
        if update_type not in self.RECRUITER_ALLOWED_UPDATE_TYPES:
            raise HTTPException(status_code=400, detail="Invalid update_type for human recruiter")

        recruiters = await self.recruiter_repo.get_name_map()
        if recruiter_id not in recruiters:
            raise HTTPException(status_code=400, detail="Invalid recruiter_id")

        normalized_correspondence = correspondence.strip() if correspondence else None
        if update_type == UpdateType.FOLLOW_UP and not normalized_correspondence:
            raise HTTPException(
                status_code=400,
                detail="correspondence is required for follow_up updates",
            )

        self._create_update(
            app,
            UpdateActor.HUMAN_RECRUITER,
            update_type,
            internal_notes,
            normalized_correspondence,
            recruiter_id,
        )

        should_trigger_ai_review = False

        if update_type == UpdateType.ADVANCE:
            app.screening_status = "advanced"
            app.company.verification_status = "verified"
        elif update_type == UpdateType.DECLINE:
            app.screening_status = "declined"
        elif update_type == UpdateType.WITHDRAW:
            app.screening_status = "withdrawn"
        elif update_type == UpdateType.REQUEST_AI_SCREEN:
            app.screening_status = "waiting_for_ai"
            should_trigger_ai_review = True
        elif update_type == UpdateType.FOLLOW_UP:
            app.screening_status = "waiting_for_candidate"
            await self.correspondence_sender(
                app.id,
                recruiter_id,
                normalized_correspondence,
            )

        await self.app_repo.update(app)

        if should_trigger_ai_review:
            await self.ai_reviewer.review(app.id, service=self)
            return {
                "success": True,
                "message": "Update added and AI screening triggered",
            }

        return {"success": True, "message": "Update added successfully"}

    async def _add_ai_update(
        self,
        app: ApplicationModel,
        update_type: UpdateType,
        internal_notes: str,
        correspondence: str | None,
    ) -> dict[str, str | bool]:
        if update_type not in self.AI_ALLOWED_UPDATE_TYPES:
            raise HTTPException(status_code=400, detail="Invalid update_type for ai_agent")

        normalized_correspondence = correspondence.strip() if correspondence else None
        self._create_update(
            app,
            UpdateActor.AI_AGENT,
            update_type,
            internal_notes,
            normalized_correspondence,
            None,
        )
        app.screening_status = "waiting_for_recruiter"
        await self.app_repo.update(app)
        return {"success": True, "message": "Update added successfully"}

    async def _add_candidate_update(
        self,
        app: ApplicationModel,
        update_type: UpdateType,
        internal_notes: str,
        correspondence: str | None,
    ) -> dict[str, str | bool]:
        if update_type not in self.CANDIDATE_ALLOWED_UPDATE_TYPES:
            raise HTTPException(status_code=400, detail="Invalid update_type for candidate")

        normalized_internal_notes = internal_notes.strip() if internal_notes else ""
        if normalized_internal_notes:
            raise HTTPException(status_code=400, detail="internal_notes are not allowed for candidate")

        normalized_correspondence = correspondence.strip() if correspondence else None
        if not normalized_correspondence:
            raise HTTPException(status_code=400, detail="correspondence is required")

        self._create_update(
            app,
            UpdateActor.CANDIDATE,
            update_type,
            "",
            normalized_correspondence,
            None,
        )
        app.screening_status = "waiting_for_ai"
        await self.app_repo.update(app)
        return {"success": True, "message": "Update added successfully"}

    def _create_update(
        self,
        app: ApplicationModel,
        actor: UpdateActor,
        update_type: UpdateType,
        internal_notes: str,
        correspondence: str | None,
        recruiter_id: str | None,
    ) -> None:
        self.update_repo.create_for_application(
            application=app,
            actor=actor,
            update_type=update_type,
            internal_notes=internal_notes,
            correspondence=correspondence,
            recruiter_id=recruiter_id,
        )
        app.updated_at = datetime.now()

    async def ingest_candidate_message(
        self,
        application_id: str,
        correspondence: str,
    ) -> dict[str, str | bool]:
        await self.add_update(
            application_id=application_id,
            actor=UpdateActor.CANDIDATE,
            update_type=UpdateType.GENERAL_UPDATE,
            internal_notes="",
            correspondence=correspondence,
            recruiter_id=None,
        )

        await self.ai_reviewer.review(application_id, service=self)
        return {
            "success": True,
            "message": "Candidate message ingested and AI screening triggered",
        }

    async def trigger_ai_screen(self, application_id: str) -> dict[str, str | bool]:
        app = await self.app_repo.get_by_id(application_id)
        if not app:
            raise HTTPException(status_code=404, detail="Application not found")

        app.screening_status = "waiting_for_ai"
        app.updated_at = datetime.now()
        await self.app_repo.update(app)

        await self.ai_reviewer.review(application_id, service=self)
        return {"success": True, "message": "AI screening triggered"}

    async def list_recruiters(self) -> list[dict[str, str]]:
        recruiters = await self.recruiter_repo.list_all()
        return [{"id": recruiter.id, "name": recruiter.name} for recruiter in recruiters]

    def _order_applications(self, apps: list[ApplicationModel]) -> list[ApplicationModel]:
        waiting_for_recruiter = [app for app in apps if app.screening_status == "waiting_for_recruiter"]
        waiting_for_ai = [app for app in apps if app.screening_status == "waiting_for_ai"]
        waiting_for_candidate = [app for app in apps if app.screening_status == "waiting_for_candidate"]
        completed = [
            app
            for app in apps
            if app.screening_status in {"advanced", "declined", "withdrawn"}
        ]

        waiting_for_recruiter.sort(key=lambda app: app.updated_at)
        waiting_for_ai.sort(key=lambda app: app.updated_at)
        waiting_for_candidate.sort(key=lambda app: app.updated_at)
        completed.sort(key=lambda app: app.updated_at, reverse=True)

        return waiting_for_recruiter + waiting_for_ai + waiting_for_candidate + completed

    def _to_summary(
        self, app: ApplicationModel, assignee_names: dict[str, str]
    ) -> ApplicationSummary:
        return ApplicationSummary(
            id=app.id,
            firstName=app.first_name,
            lastName=app.last_name,
            email=app.email,
            mobile=app.mobile,
            jobTitle=app.job_title,
            seniorityLevel=app.seniority_level,
            department=self._normalize_enum_string(app.department),
            companyName=app.company.name,
            companySize=app.company.size,
            companyType=self._normalize_enum_string(app.company.type),
            region=app.region or app.locale_region,
            assignee_id=app.assignee_id,
            assignee_name=assignee_names.get(app.assignee_id) if app.assignee_id else None,
            screeningStatus=app.screening_status,
            createdAt=app.created_at,
            updatedAt=app.updated_at,
        )

    def _to_detail(self, app: ApplicationModel) -> Application:
        return Application(
            id=app.id,
            firstName=app.first_name,
            lastName=app.last_name,
            email=app.email,
            mobile=app.mobile,
            bio=app.bio,
            linkedinUrl=app.linkedin_url,
            currentRole=app.current_role,
            seniorityLevel=app.seniority_level,
            jobTitle=app.job_title,
            department=self._normalize_enum_string(app.department),
            subDepartments=[
                SubDepartment(self._normalize_enum_string(value))
                for value in app.sub_departments
            ],
            companyId=app.company_id,
            company=Company(
                id=app.company.id,
                name=app.company.name,
                siteUrl=app.company.site_url,
                size=app.company.size,
                type=self._normalize_enum_string(app.company.type),
                verificationStatus=self._normalize_enum_string(app.company.verification_status),
                address=Address(
                    id=app.company.address_id,
                    address1=app.company.address1,
                    country=app.company.country,
                    locality=app.company.locality,
                    postalCode=app.company.postal_code,
                    region=app.company.region,
                ),
            ),
            assignee_id=app.assignee_id,
            region=app.region,
            screeningStatus=app.screening_status,
            createdAt=app.created_at,
            updatedAt=app.updated_at,
            locale=LocaleInfo(
                country=app.locale_country,
                preferredLanguage=app.locale_preferred_language,
                region=app.locale_region,
                storeId=app.locale_store_id,
            ),
            updates=[
                Update(
                    id=update.id,
                    timestamp=update.timestamp,
                    actor=update.actor,
                    internal_notes=update.internal_notes,
                    recruiter_id=update.recruiter_id,
                    update_type=update.update_type,
                    correspondence=update.correspondence,
                )
                for update in app.updates
            ],
        )

    def _apply_update(self, app: ApplicationModel, key: str, value: object) -> None:
        if key == "firstName":
            app.first_name = str(value)
        elif key == "lastName":
            app.last_name = str(value)
        elif key == "email":
            app.email = str(value)
        elif key == "mobile":
            app.mobile = str(value)
        elif key == "bio":
            app.bio = str(value)
        elif key == "linkedinUrl":
            app.linkedin_url = str(value)
        elif key == "jobTitle":
            app.job_title = str(value)
        elif key == "seniorityLevel":
            app.seniority_level = str(value)
        elif key == "department":
            app.department = self._enum_value(value)
        elif key == "subDepartments":
            app.sub_departments = [self._enum_value(item) for item in list(value)]
        elif key == "region":
            app.region = str(value)
        elif key == "assignee_id":
            app.assignee_id = str(value)
        elif key == "companyName":
            app.company.name = str(value)
        elif key == "companySize":
            app.company.size = str(value)
        elif key == "companyType":
            app.company.type = self._enum_value(value)
        elif key == "companyVerificationStatus":
            app.company.verification_status = self._enum_value(value)
        elif key == "companySiteUrl":
            app.company.site_url = str(value)

    def _enum_value(self, value: object) -> str:
        if isinstance(value, Enum):
            return str(value.value)
        return self._normalize_enum_string(str(value))

    def _normalize_enum_string(self, value: str) -> str:
        if "." in value:
            return value.split(".")[-1]
        return value
