from sqlalchemy.exc import (
    ArgumentError,
    NoSuchModuleError,
)
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from travel_planner.application.exceptions.persistence import (
    PersistenceConfigurationError,
)


def init_engine(url: str, pool_size: int) -> AsyncEngine:
    try:
        return create_async_engine(
            url,
            echo=False,
            pool_pre_ping=True,
            pool_recycle=3600,
            pool_size=pool_size,
            max_overflow=10,
        )
    except (ArgumentError, NoSuchModuleError) as error:
        raise PersistenceConfigurationError(str(error)) from error


def init_sessionmaker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
