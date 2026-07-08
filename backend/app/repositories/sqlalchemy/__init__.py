from app.repositories.sqlalchemy.application_repo import SqlAlchemyApplicationRepository
from app.repositories.sqlalchemy.recruiter_repo import SqlAlchemyRecruiterRepository
from app.repositories.sqlalchemy.update_repo import SqlAlchemyUpdateRepository

__all__ = [
    "SqlAlchemyApplicationRepository",
    "SqlAlchemyRecruiterRepository",
    "SqlAlchemyUpdateRepository",
]
