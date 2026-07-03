import logging
from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from travel_planner.application.enums.error import AppError
from travel_planner.config.exception import TravelPlannerException

logger = logging.getLogger(__name__)


class GlobalExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        try:
            return await call_next(request)
        except TravelPlannerException as exc:
            logger.error("Project-level exception caught: %s", exc, exc_info=True)
            return JSONResponse(
                status_code=500,
                content={
                    "error": AppError.INTERNAL_ERROR,
                    "message": "An internal server error occurred.",
                },
            )
