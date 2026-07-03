import logging
from collections.abc import Awaitable, Callable
from functools import wraps
from typing import Any

from sqlalchemy import exc

from travel_planner.application.exceptions import (
    PersistenceConnectionError,
    PersistenceConstraintError,
    PersistenceError,
    PersistenceInvalidDataError,
    PersistenceOperationalError,
    PersistenceQueryError,
)

logger = logging.getLogger(__name__)


def process_sqlalchemy_error[**P, R: Awaitable[Any]](
    func: Callable[P, R],
) -> Callable[P, R]:
    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> Any:
        try:
            return await func(*args, **kwargs)
        except exc.IntegrityError as e:
            logger.error(
                "Database integrity constraint violated: %s", e.orig, exc_info=True
            )
            raise PersistenceConstraintError(str(e.orig)) from e
        except exc.DataError as e:
            logger.error(
                "Invalid data encountered during database operation: %s",
                e.orig,
                exc_info=True,
            )
            raise PersistenceInvalidDataError(str(e.orig)) from e
        except exc.OperationalError as e:
            err_str = str(e.orig).lower() if e.orig else str(e).lower()

            if "connection" in err_str:
                logger.error("Database connection error: %s", err_str, exc_info=True)
                raise PersistenceConnectionError(err_str) from e
            logger.error("Operational error in database: %s", err_str, exc_info=True)
            raise PersistenceOperationalError(err_str) from e
        except exc.ProgrammingError as e:
            logger.error("Programming error in SQL query: %s", e.orig, exc_info=True)
            raise PersistenceQueryError(str(e.orig)) from e
        except exc.SQLAlchemyError as e:
            logger.error("Unexpected SQLAlchemy error: %s", e, exc_info=True)
            raise PersistenceError(f"Unexpected SQLAlchemy error: {e}") from e

    return wrapper  # type: ignore
