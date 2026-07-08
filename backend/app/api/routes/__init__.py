from app.api.routes.applications import router as applications_router
from app.api.routes.hooks import router as hooks_router
from app.api.routes.recruiters import router as recruiters_router

__all__ = [
    "applications_router",
    "hooks_router",
    "recruiters_router",
]
