from collections.abc import Callable
from typing import Any, NoReturn

from fastapi import HTTPException, status

from travel_planner.application.dtos import Failure, Result, Success
from travel_planner.application.enums import AppError

ERROR_MAPPING: dict[str | int, int] = {
    AppError.NOT_FOUND: status.HTTP_404_NOT_FOUND,
    AppError.CONFLICT: status.HTTP_409_CONFLICT,
    AppError.VALIDATION_ERROR: status.HTTP_400_BAD_REQUEST,
    AppError.BAD_REQUEST: status.HTTP_400_BAD_REQUEST,
    AppError.UNPROCESSABLE_ENTITY: status.HTTP_422_UNPROCESSABLE_CONTENT,
    AppError.TOO_MANY_REQUESTS: status.HTTP_429_TOO_MANY_REQUESTS,
    AppError.SERVICE_UNAVAILABLE: status.HTTP_503_SERVICE_UNAVAILABLE,
    AppError.UNAUTHORIZED: status.HTTP_401_UNAUTHORIZED,
    AppError.FORBIDDEN: status.HTTP_403_FORBIDDEN,
    AppError.INTERNAL_ERROR: status.HTTP_500_INTERNAL_SERVER_ERROR,
}


def void(value: Any) -> None:
    """Explicitly ignores the value and returns None."""
    return None


def process_result[T, R](
    result: Result[T], on_success: Callable[[T], R], on_failure: Callable[[Failure], R]
) -> R:
    """Universal `Result` handler.
    :param result: The Result object (Success or Failure).
    :param on_success: Function to be executed on success.
    :param on_failure: Function to be executed if an error occurs.
    :return: The result of executing one of the functions (type R).
    """
    match result:
        case Success(data):
            return on_success(data)
        case Failure() as fail:
            return on_failure(fail)


def raise_http_exception(fail: Failure) -> NoReturn:
    """Maps a Failure object to an HTTP exception using a dictionary lookup.
    """
    status_code = ERROR_MAPPING.get(fail.error, status.HTTP_500_INTERNAL_SERVER_ERROR)

    raise HTTPException(
        status_code=status_code, detail=fail.message or "An unexpected error occurred."
    )
