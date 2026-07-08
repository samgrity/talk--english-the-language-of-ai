from typing import Protocol

from app.core.enums import UpdateActor, UpdateType
from app.db.models.application import ApplicationModel


class UpdateRepository(Protocol):
    def create_for_application(
        self,
        application: ApplicationModel,
        actor: UpdateActor,
        update_type: UpdateType,
        internal_notes: str,
        correspondence: str | None,
        recruiter_id: str | None,
    ) -> None: ...
