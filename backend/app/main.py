from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.applications import router as applications_router
from app.api.routes.hooks import router as hooks_router
from app.api.routes.recruiters import router as recruiters_router
from app.core.config import settings


app = FastAPI(title="HireFlow Candidate Screening API", version="0.3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["GET", "POST", "PUT"],
    allow_headers=["Content-Type"],
)

app.include_router(applications_router)
app.include_router(recruiters_router)
app.include_router(hooks_router)
