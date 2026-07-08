from typing import Protocol

from app.core.enums import FilterStatus
from app.db.models.application import ApplicationModel


class ApplicationRepository(Protocol):
    async def list_all(
        self,
        filter_status: FilterStatus,
        search: str | None,
        assignee_id: str | None,
    ) -> list[ApplicationModel]: ...

    async def get_by_id(self, application_id: str) -> ApplicationModel | None: ...

    async def update(self, application: ApplicationModel) -> None: ...
