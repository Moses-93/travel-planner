import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from travel_planner.api.middleware.exceptions import GlobalExceptionMiddleware
from travel_planner.api.v1.router import v1
from travel_planner.config.settings import get_settings
from travel_planner.infrastructure.persistence.postgres.config import (
    init_engine,
    init_sessionmaker,
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manage the lifespan of the FastAPI application.

    This context manager handles setup and teardown events, such as
    initializing connections or cleaning up resources when the app shuts down.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None
    """
    logger.info("Starting up Travel Planner API")
    settings = get_settings()
    engine = init_engine(settings.database_url, settings.DB_POOL_SIZE)
    app.state.sessionmaker = init_sessionmaker(engine)
    yield
    await engine.dispose()
    logger.info("Shutting down Travel Planner API")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance.

    Configures CORS middleware and includes all API routers.

    Returns:
        FastAPI: The configured FastAPI application instance.
    """
    app = FastAPI(
        title="Travel Planner API",
        description="API for managing travel projects and places.",
        version="0.1.0",
        lifespan=lifespan,
    )

    app.add_middleware(GlobalExceptionMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(v1(), prefix="/api")

    return app


app = create_app()
