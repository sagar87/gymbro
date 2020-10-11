import logging

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from tortoise.contrib.fastapi import register_tortoise

from app.config import get_settings, Settings
from app.api import ping
from app.api import projects
from app.api import tasks

from app.database import init_db
from app.config import get_settings

log = logging.getLogger(__name__)


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(ping.router)
    application.include_router(projects.router, prefix="/projects", tags=["projects"])
    application.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
    origins = [
        "http://localhost",
        "http://localhost:3007",
    ]
    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return application


app = create_application()
settings = get_settings()


@app.on_event("startup")
async def startup_event():
    log.info("Starting up...")
    init_db(app, settings)


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")
