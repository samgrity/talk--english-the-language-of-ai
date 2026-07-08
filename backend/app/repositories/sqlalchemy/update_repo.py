from datetime import datetime

from app.core.enums import UpdateActor, UpdateType
from app.db.models.application import ApplicationModel
from app.db.models.update import UpdateModel


class SqlAlchemyUpdateRepository:
    def create_for_application(
        self,
        application: ApplicationModel,
        actor: UpdateActor,
        update_type: UpdateType,
        internal_notes: str,
        correspondence: str | None,
        recruiter_id: str | None,
    ) -> None:
        new_update = UpdateModel(
            id=f"update-{application.id}-{len(application.updates) + 1}",
            application_id=application.id,
            timestamp=datetime.now(),
            actor=actor.value,
            internal_notes=internal_notes,
            update_type=update_type.value,
            correspondence=correspondence,
            recruiter_id=recruiter_id,
        )
        application.updates.append(new_update)
