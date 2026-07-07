from collections.abc import Sequence

from travel_planner.application.dtos import (
    AddProjectPlace,
    Failure,
    GetPlaceQuery,
    GetProjectPlacesQuery,
    MarkPlaceVisitedCommand,
    RemoveProjectPlaceCommand,
    Result,
    Success,
    UpdatePlaceNotes,
)
from travel_planner.application.enums import AppError
from travel_planner.application.interfaces import PlaceGateway, UnitOfWork
from travel_planner.application.utils import process_application_exceptions
from travel_planner.domain.entities import TravelPlace, TravelProject
from travel_planner.domain.exceptions.base import DomainException
from travel_planner.domain.repositories import (
    TravelPlaceRepository,
    TravelProjectRepository,
)


class AddProjectPlaceUseCase:
    def __init__(
        self,
        projects: TravelProjectRepository,
        place_gateway: PlaceGateway,
        uow: UnitOfWork,
    ) -> None:
        self._projects = projects
        self._place_gateway = place_gateway
        self._uow = uow

    @process_application_exceptions
    async def execute(self, command: AddProjectPlace) -> Result[TravelProject]:
        """Add a place to a travel project.

        Args:
            command (AddProjectPlace): The data transfer object containing place details.

        Returns:
            Result[TravelProject]: A Result containing the updated TravelProject on success, or Failure otherwise.
        """
        project = await self._projects.get_by_id(command.project_id)
        if not project:
            return Failure(error=AppError.NOT_FOUND, message="Project not found.")

        is_valid = await self._place_gateway.validate_place(command.external_id)
        if not is_valid:
            return Failure(
                error=AppError.UNPROCESSABLE_ENTITY,
                message=f"Place with external ID {command.external_id} is invalid or not found.",
            )

        try:
            place = TravelPlace(
                external_id=command.external_id,
                project_id=command.project_id,
                notes=command.notes,
            )
            project.add_place(place)
        except DomainException as e:
            return Failure(error=AppError.BAD_REQUEST, message=str(e))

        async with self._uow.transaction():
            await self._projects.save(project)
        return Success(project)


class RemoveProjectPlaceUseCase:
    def __init__(self, projects: TravelProjectRepository, uow: UnitOfWork) -> None:
        self._projects = projects
        self._uow = uow

    @process_application_exceptions
    async def execute(
        self, command: RemoveProjectPlaceCommand
    ) -> Result[TravelProject]:
        """Remove a place from a travel project.

        Args:
            command (RemoveProjectPlaceCommand): The data transfer object containing removal details.

        Returns:
            Result[TravelProject]: A Result containing the updated TravelProject on success, or Failure otherwise.
        """
        project = await self._projects.get_by_id(command.project_id)
        if not project:
            return Failure(error=AppError.NOT_FOUND, message="Project not found.")

        try:
            project.remove_place(command.place_id)
        except DomainException as e:
            return Failure(error=AppError.BAD_REQUEST, message=str(e))

        async with self._uow.transaction():
            await self._projects.save(project)
        return Success(project)


class UpdatePlacesNotesUseCase:
    def __init__(self, projects: TravelProjectRepository, uow: UnitOfWork) -> None:
        self._projects = projects
        self._uow = uow

    @process_application_exceptions
    async def execute(self, command: UpdatePlaceNotes) -> Result[TravelProject]:
        """Update the notes for a specific place in a project.

        Args:
            command (UpdatePlaceNotes): The data transfer object containing the new notes.

        Returns:
            Result[TravelProject]: A Result containing the updated TravelProject on success, or Failure otherwise.
        """
        project = await self._projects.get_by_id(command.project_id)
        if not project:
            return Failure(error=AppError.NOT_FOUND, message="Project not found.")

        place = next(
            (p for p in project.places if p.place_id == command.place_id), None
        )
        if not place:
            return Failure(
                error=AppError.NOT_FOUND, message="Place not found in this project."
            )

        try:
            place.update_notes(command.notes)
        except DomainException as e:
            return Failure(error=AppError.BAD_REQUEST, message=str(e))

        async with self._uow.transaction():
            await self._projects.save(project)
        return Success(project)


class MarkPlaceVisitedUseCase:
    def __init__(self, projects: TravelProjectRepository, uow: UnitOfWork) -> None:
        self._projects = projects
        self._uow = uow

    @process_application_exceptions
    async def execute(self, command: MarkPlaceVisitedCommand) -> Result[TravelProject]:
        """Mark a specific place in a project as visited.

        Args:
            command (MarkPlaceVisitedCommand): The data transfer object containing operation details.

        Returns:
            Result[TravelProject]: A Result containing the updated TravelProject on success, or Failure otherwise.
        """
        project = await self._projects.get_by_id(command.project_id)
        if not project:
            return Failure(error=AppError.NOT_FOUND, message="Project not found.")

        place = next(
            (p for p in project.places if p.place_id == command.place_id), None
        )
        if not place:
            return Failure(
                error=AppError.NOT_FOUND, message="Place not found in this project."
            )

        try:
            project.mark_place_visited(command.place_id)
        except DomainException as e:
            return Failure(error=AppError.BAD_REQUEST, message=str(e))

        async with self._uow.transaction():
            await self._projects.save(project)
        return Success(project)


class GetPlacesByProjectUseCase:
    def __init__(self, places: TravelPlaceRepository) -> None:
        self._places = places

    @process_application_exceptions
    async def execute(
        self, query: GetProjectPlacesQuery
    ) -> Result[Sequence[TravelPlace]]:
        """Retrieve all places associated with a travel project.

        Args:
            query (GetProjectPlacesQuery): The query containing the project ID.

        Returns:
            Result[Sequence[TravelPlace]]: A Result containing a list of TravelPlaces.
        """
        places = await self._places.get_by_project_id(query.project_id)
        return Success(places)


class GetPlaceUseCase:
    def __init__(self, places: TravelPlaceRepository) -> None:
        self._places = places

    @process_application_exceptions
    async def execute(self, query: GetPlaceQuery) -> Result[TravelPlace]:
        """Retrieve a specific place by its ID.

        Args:
            query (GetPlaceQuery): The query containing the place ID.

        Returns:
            Result[TravelPlace]: A Result containing the TravelPlace on success, or Failure if not found.
        """
        place = await self._places.get_by_id(query.place_id)
        if not place:
            return Failure(error=AppError.NOT_FOUND, message="Place not found.")
        return Success(place)
