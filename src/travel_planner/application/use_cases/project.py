from collections.abc import Sequence
from uuid import UUID

from travel_planner.application.dtos import (
    CreateProject,
    Failure,
    GetProjectQuery,
    GetProjectsQuery,
    RemoveProjectCommand,
    Result,
    Success,
    UpdateProject,
)
from travel_planner.application.enums import AppError
from travel_planner.application.interfaces import PlaceGateway
from travel_planner.application.utils import process_application_exceptions
from travel_planner.domain.entities import TravelPlace, TravelProject
from travel_planner.domain.exceptions.base import DomainException
from travel_planner.domain.repositories import TravelProjectRepository


class CreateProjectUseCase:
    def __init__(
        self,
        projects: TravelProjectRepository,
        place_gateway: PlaceGateway,
    ) -> None:
        self._projects = projects
        self._place_gateway = place_gateway

    @process_application_exceptions
    async def execute(self, command: CreateProject) -> Result[TravelProject]:
        """Create a new travel project.

        Args:
            command (CreateProject): The data transfer object containing project details.

        Returns:
            Result[TravelProject]: A Result containing the created TravelProject on success, or Failure otherwise.
        """
        project = TravelProject(
            name=command.name,
            description=command.description,
            start_date=command.start_date,
        )

        try:
            for external_id in command.external_place_ids:
                is_valid = await self._place_gateway.validate_place(external_id)
                    if not is_valid:
                        return Failure(
                            error=AppError.UNPROCESSABLE_ENTITY,
                            message=f"Place with external ID {external_id} is invalid or not found.",
                        )
                    place = TravelPlace(
                        external_id=external_id,
                        project_id=project.project_id,
                    )
                    project.add_place(place)
        except DomainException as e:
            return Failure(error=AppError.BAD_REQUEST, message=str(e))

        await self._projects.save(project)
        return Success(project)


class GetTravelProjectUseCase:
    def __init__(self, projects: TravelProjectRepository) -> None:
        self._projects = projects

    @process_application_exceptions
    async def execute(self, query: GetProjectQuery) -> Result[TravelProject]:
        """Retrieve a travel project by its ID.

        Args:
            query (GetProjectQuery): The query object containing the project ID.

        Returns:
            Result[TravelProject]: A Result containing the TravelProject on success, or Failure if not found.
        """
        project = await self._projects.get_by_id(query.project_id)
        if not project:
            return Failure(error=AppError.NOT_FOUND, message="Project not found.")
        return Success(project)


class GetTravelProjectsUseCase:
    def __init__(self, projects: TravelProjectRepository) -> None:
        self._projects = projects

    @process_application_exceptions
    async def execute(self, query: GetProjectsQuery) -> Result[Sequence[TravelProject]]:
        """Retrieve a list of travel projects with pagination.

        Args:
            query (GetProjectsQuery): The query object containing limit and offset.

        Returns:
            Result[Sequence[TravelProject]]: A Result containing a list of TravelProjects.
        """
        projects = await self._projects.get_all(limit=query.limit, offset=query.offset)
        return Success(projects)


class RemoveProjectUseCase:
    def __init__(self, projects: TravelProjectRepository) -> None:
        self._projects = projects

    @process_application_exceptions
    async def execute(self, command: RemoveProjectCommand) -> Result[None]:
        """Remove a travel project by its ID.

        Args:
            command (RemoveProjectCommand): The command object containing the project ID.

        Returns:
            Result[None]: Success if the project was removed, Failure otherwise.
        """
        project = await self._projects.get_by_id(command.project_id)
        if not project:
            return Failure(error=AppError.NOT_FOUND, message="Project not found.")

        try:
            project.check_can_be_deleted()
        except DomainException as e:
            return Failure(error=AppError.BAD_REQUEST, message=str(e))

        await self._projects.remove(command.project_id)
        return Success(None)


class UpdateProjectDetailsUseCase:
    def __init__(self, projects: TravelProjectRepository) -> None:
        self._projects = projects

    @process_application_exceptions
    async def execute(self, command: UpdateProject) -> Result[TravelProject]:
        """Update the details of a travel project.

        Args:
            command (UpdateProject): The data transfer object containing updated details.

        Returns:
            Result[TravelProject]: A Result containing the updated TravelProject on success, or Failure otherwise.
        """
        project = await self._projects.get_by_id(command.project_id)
        if not project:
            return Failure(error=AppError.NOT_FOUND, message="Project not found.")

        try:
            project.update_details(
                name=command.name,
                description=command.description,
                start_date=command.start_date,
            )
        except DomainException as e:
            return Failure(error=AppError.BAD_REQUEST, message=str(e))

        await self._projects.save(project)
        return Success(project)
