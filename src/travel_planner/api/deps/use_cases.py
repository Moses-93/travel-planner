from travel_planner.api.deps.gateways import PlaceGatewayDependency
from travel_planner.api.deps.repositories import (
    PlaceRepoDependency,
    ProjectRepoDependency,
)
from travel_planner.api.deps.uow import UoWDependency
from travel_planner.application.use_cases import (
    AddProjectPlaceUseCase,
    CreateProjectUseCase,
    GetPlacesByProjectUseCase,
    GetPlaceUseCase,
    GetTravelProjectsUseCase,
    GetTravelProjectUseCase,
    MarkPlaceVisitedUseCase,
    RemoveProjectPlaceUseCase,
    RemoveProjectUseCase,
    UpdatePlacesNotesUseCase,
    UpdateProjectDetailsUseCase,
)


def get_create_project_use_case(
    repo: ProjectRepoDependency, gateway: PlaceGatewayDependency, uow: UoWDependency
) -> CreateProjectUseCase:
    return CreateProjectUseCase(projects=repo, place_gateway=gateway, uow=uow)


def get_travel_project_use_case(repo: ProjectRepoDependency) -> GetTravelProjectUseCase:
    return GetTravelProjectUseCase(projects=repo)


def get_travel_projects_use_case(
    repo: ProjectRepoDependency,
) -> GetTravelProjectsUseCase:
    return GetTravelProjectsUseCase(projects=repo)


def get_remove_project_use_case(
    repo: ProjectRepoDependency, uow: UoWDependency
) -> RemoveProjectUseCase:
    return RemoveProjectUseCase(projects=repo, uow=uow)


def get_update_project_use_case(
    repo: ProjectRepoDependency, uow: UoWDependency
) -> UpdateProjectDetailsUseCase:
    return UpdateProjectDetailsUseCase(projects=repo, uow=uow)


def get_add_project_place_use_case(
    repo: ProjectRepoDependency, gateway: PlaceGatewayDependency, uow: UoWDependency
) -> AddProjectPlaceUseCase:
    return AddProjectPlaceUseCase(projects=repo, place_gateway=gateway, uow=uow)


def get_remove_project_place_use_case(
    repo: ProjectRepoDependency, uow: UoWDependency
) -> RemoveProjectPlaceUseCase:
    return RemoveProjectPlaceUseCase(projects=repo, uow=uow)


def get_update_places_notes_use_case(
    repo: ProjectRepoDependency, uow: UoWDependency
) -> UpdatePlacesNotesUseCase:
    return UpdatePlacesNotesUseCase(projects=repo, uow=uow)


def get_mark_place_visited_use_case(
    repo: ProjectRepoDependency, uow: UoWDependency
) -> MarkPlaceVisitedUseCase:
    return MarkPlaceVisitedUseCase(projects=repo, uow=uow)


def get_places_by_project_use_case(
    repo: PlaceRepoDependency,
) -> GetPlacesByProjectUseCase:
    return GetPlacesByProjectUseCase(places=repo)


def get_place_use_case(repo: PlaceRepoDependency) -> GetPlaceUseCase:
    return GetPlaceUseCase(places=repo)


from typing import Annotated

from fastapi import Depends

CreateProjectDependency = Annotated[
    CreateProjectUseCase, Depends(get_create_project_use_case)
]
GetTravelProjectDependency = Annotated[
    GetTravelProjectUseCase, Depends(get_travel_project_use_case)
]
GetTravelProjectsDependency = Annotated[
    GetTravelProjectsUseCase, Depends(get_travel_projects_use_case)
]
RemoveProjectDependency = Annotated[
    RemoveProjectUseCase, Depends(get_remove_project_use_case)
]
UpdateProjectDetailsDependency = Annotated[
    UpdateProjectDetailsUseCase, Depends(get_update_project_use_case)
]
AddProjectPlaceDependency = Annotated[
    AddProjectPlaceUseCase, Depends(get_add_project_place_use_case)
]
RemoveProjectPlaceDependency = Annotated[
    RemoveProjectPlaceUseCase, Depends(get_remove_project_place_use_case)
]
UpdatePlacesNotesDependency = Annotated[
    UpdatePlacesNotesUseCase, Depends(get_update_places_notes_use_case)
]
MarkPlaceVisitedDependency = Annotated[
    MarkPlaceVisitedUseCase, Depends(get_mark_place_visited_use_case)
]
GetPlacesByProjectDependency = Annotated[
    GetPlacesByProjectUseCase, Depends(get_places_by_project_use_case)
]
GetPlaceDependency = Annotated[GetPlaceUseCase, Depends(get_place_use_case)]
