from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from infra.core.config import settings
from infra.core.logger import setup_logging
from infra.di.ioc import build_container

WIRED_MODULES = [
    "presentation.http.authentication",
    "presentation.http.v1.handlers.auth",
    "presentation.http.v1.handlers.users",
    "presentation.http.v1.handlers.admin",
    "presentation.http.v1.handlers.webhooks",
]


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    setup_logging(level=settings.log_level)

    container = build_container()
    container.wire(modules=WIRED_MODULES)
    app.container = container

    logger.info("Service P started")
    yield

    db_manager = container.db.db_manager()
    await db_manager.dispose()
    logger.info("Service P stopped")
