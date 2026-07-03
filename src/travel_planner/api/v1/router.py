from fastapi import APIRouter

from .endpoints import place, project


def v1() -> APIRouter:
    router = APIRouter(prefix="/v1")

    router.include_router(project.router, prefix="/projects", tags=["projects"])
    router.include_router(place.router, prefix="/projects", tags=["places"])
    return router
