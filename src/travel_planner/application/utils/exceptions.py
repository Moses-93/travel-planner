from collections.abc import Awaitable, Callable
from functools import wraps

from travel_planner.application.dtos.result import Failure
from travel_planner.application.enums.error import AppError
from travel_planner.application.exceptions.persistence import (
    PersistenceConnectionError,
    PersistenceConstraintError,
    PersistenceError,
    PersistenceInvalidDataError,
    PersistenceOperationalError,
    PersistenceQueryError,
)
from travel_planner.application.messages.errors import ErrorMessages


def process_application_exceptions[**P, R](
    func: Callable[P, Awaitable[R]],
) -> Callable[P, Awaitable[R | Failure]]:
    """Translates Domain and Persistence exceptions into Failure objects."""

    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | Failure:
        try:
            return await func(*args, **kwargs)
        except (PersistenceConnectionError, PersistenceOperationalError):
            return Failure(
                message=ErrorMessages.service_unavailable(),
                error=AppError.SERVICE_UNAVAILABLE,
            )
        except PersistenceConstraintError:
            return Failure(
                message=ErrorMessages.constraint_violation(), error=AppError.CONFLICT
            )
        except PersistenceInvalidDataError:
            return Failure(
                message=ErrorMessages.invalid_data(), error=AppError.INTERNAL_ERROR
            )
        except (PersistenceQueryError, PersistenceError):
            return Failure(
                message=ErrorMessages.service_unavailable(),
                error=AppError.INTERNAL_ERROR,
            )

    return wrapper
