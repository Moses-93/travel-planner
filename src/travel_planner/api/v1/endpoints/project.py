from uuid import UUID

from fastapi import APIRouter, status

from travel_planner.api.deps import (
    CreateProjectDependency,
    GetTravelProjectDependency,
    GetTravelProjectsDependency,
    RemoveProjectDependency,
    UpdateProjectDetailsDependency,
)
from travel_planner.api.utils.result import (
    process_result,
    raise_http_exception,
    void,
)
from travel_planner.api.v1.schemas.project import (
    ProjectCreateRequest,
    ProjectResponse,
    ProjectUpdateRequest,
)
from travel_planner.application.dtos.project import (
    GetProjectQuery,
    GetProjectsQuery,
    RemoveProjectCommand,
)

router = APIRouter()


@router.post(
    "/",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new travel project",
    responses={
        400: {"description": "Project data validation failed"},
        422: {"description": "Provided places are invalid or unavailable"},
    },
)
async def create_project(
    request: ProjectCreateRequest,
    project_creator: CreateProjectDependency,
) -> ProjectResponse:
    result = await project_creator.execute(request.to_dto())
    return process_result(result, ProjectResponse.model_validate, raise_http_exception)


@router.get(
    "/",
    response_model=list[ProjectResponse],
    summary="Get all travel projects",
)
async def get_projects(
    projects_provider: GetTravelProjectsDependency,
    limit: int = 10,
    offset: int = 0,
) -> list[ProjectResponse]:
    query = GetProjectsQuery(limit=limit, offset=offset)
    result = await projects_provider.execute(query)
    return process_result(
        result,
        lambda projects: [ProjectResponse.model_validate(p) for p in projects],
        raise_http_exception,
    )


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Get a travel project by ID",
    responses={404: {"description": "Travel project not found"}},
)
async def get_project(
    project_id: UUID,
    project_provider: GetTravelProjectDependency,
) -> ProjectResponse:
    query = GetProjectQuery(project_id=project_id)
    result = await project_provider.execute(query)
    return process_result(result, ProjectResponse.model_validate, raise_http_exception)


@router.patch(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Update a travel project",
    responses={
        404: {"description": "Travel project not found"},
        422: {"description": "Update data is invalid"},
    },
)
async def update_project(
    project_id: UUID,
    request: ProjectUpdateRequest,
    project_updater: UpdateProjectDetailsDependency,
) -> ProjectResponse:
    command = request.to_dto(project_id)
    result = await project_updater.execute(command)
    return process_result(result, ProjectResponse.model_validate, raise_http_exception)


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a travel project",
    responses={404: {"description": "Travel project not found"}},
)
async def delete_project(
    project_id: UUID,
    project_remover: RemoveProjectDependency,
) -> None:
    command = RemoveProjectCommand(project_id=project_id)
    result = await project_remover.execute(command)
    return process_result(result, void, raise_http_exception)
