from uuid import UUID

from fastapi import APIRouter, status

from travel_planner.api.deps import (
    AddProjectPlaceDependency,
    GetPlaceDependency,
    GetPlacesByProjectDependency,
    MarkPlaceVisitedDependency,
    RemoveProjectPlaceDependency,
    UpdatePlacesNotesDependency,
)
from travel_planner.api.utils.result import (
    process_result,
    raise_http_exception,
)
from travel_planner.api.v1.schemas.place import (
    PlaceAddRequest,
    PlaceResponse,
    PlaceUpdateRequest,
)
from travel_planner.api.v1.schemas.project import ProjectResponse
from travel_planner.application.dtos.place import (
    GetPlaceQuery,
    GetProjectPlacesQuery,
    MarkPlaceVisitedCommand,
    RemoveProjectPlaceCommand,
)

router = APIRouter()


@router.post(
    "/{project_id}/places",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add a place to a travel project",
    responses={
        400: {"description": "Place is already in project"},
        404: {"description": "Project not found or place does not exist"}
    },
)
async def add_place_to_project(
    project_id: UUID,
    request: PlaceAddRequest,
    place_adder: AddProjectPlaceDependency,
) -> ProjectResponse:
    command = request.to_dto(project_id)
    result = await place_adder.execute(command)
    return process_result(result, ProjectResponse.model_validate, raise_http_exception)


@router.get(
    "/{project_id}/places",
    response_model=list[PlaceResponse],
    summary="Get all places for a project",
    responses={404: {"description": "Travel project not found"}},
)
async def get_project_places(
    project_id: UUID,
    places_provider: GetPlacesByProjectDependency,
) -> list[PlaceResponse]:
    query = GetProjectPlacesQuery(project_id=project_id)
    result = await places_provider.execute(query)
    return process_result(
        result,
        lambda places: [PlaceResponse.model_validate(p) for p in places],
        raise_http_exception,
    )


@router.get(
    "/{project_id}/places/{place_id}",
    response_model=PlaceResponse,
    summary="Get a single place by ID",
    responses={404: {"description": "Travel place not found"}},
)
async def get_place(
    project_id: UUID,
    place_id: UUID,
    place_provider: GetPlaceDependency,
) -> PlaceResponse:
    query = GetPlaceQuery(place_id=place_id)
    result = await place_provider.execute(query)
    return process_result(result, PlaceResponse.model_validate, raise_http_exception)


@router.put(
    "/{project_id}/places/{place_id}/notes",
    response_model=ProjectResponse,
    summary="Update notes for a place",
    responses={404: {"description": "Project or place not found"}},
)
async def update_place_notes(
    project_id: UUID,
    place_id: UUID,
    request: PlaceUpdateRequest,
    notes_updater: UpdatePlacesNotesDependency,
) -> ProjectResponse:
    command = request.to_dto(project_id, place_id)
    result = await notes_updater.execute(command)
    return process_result(result, ProjectResponse.model_validate, raise_http_exception)


@router.post(
    "/{project_id}/places/{place_id}/visited",
    response_model=ProjectResponse,
    summary="Mark a place as visited",
    responses={404: {"description": "Project or place not found"}},
)
async def mark_place_visited(
    project_id: UUID,
    place_id: UUID,
    place_marker: MarkPlaceVisitedDependency,
) -> ProjectResponse:
    command = MarkPlaceVisitedCommand(project_id=project_id, place_id=place_id)
    result = await place_marker.execute(command)
    return process_result(result, ProjectResponse.model_validate, raise_http_exception)


@router.delete(
    "/{project_id}/places/{place_id}",
    response_model=ProjectResponse,
    summary="Remove a place from a project",
    responses={404: {"description": "Project or place not found"}},
)
async def remove_place_from_project(
    project_id: UUID,
    place_id: UUID,
    place_remover: RemoveProjectPlaceDependency,
) -> ProjectResponse:
    command = RemoveProjectPlaceCommand(project_id=project_id, place_id=place_id)
    result = await place_remover.execute(command)
    return process_result(result, ProjectResponse.model_validate, raise_http_exception)
