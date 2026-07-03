from typing import Annotated

from fastapi import Depends

from travel_planner.api.deps.session import SessionDependency
from travel_planner.domain.repositories.place_repository import TravelPlaceRepository
from travel_planner.domain.repositories.project_repository import (
    TravelProjectRepository,
)
from travel_planner.infrastructure.persistence.postgres.repositories import (
    PostgresTravelPlaceRepository,
    PostgresTravelProjectRepository,
)


def get_project_repository(session: SessionDependency) -> TravelProjectRepository:
    return PostgresTravelProjectRepository(session=session)


def get_place_repository(session: SessionDependency) -> TravelPlaceRepository:
    return PostgresTravelPlaceRepository(session=session)


ProjectRepoDependency = Annotated[
    TravelProjectRepository, Depends(get_project_repository)
]
PlaceRepoDependency = Annotated[TravelPlaceRepository, Depends(get_place_repository)]
