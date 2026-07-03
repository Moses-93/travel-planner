from dataclasses import dataclass, field
from datetime import date
from uuid import UUID, uuid4

from travel_planner.domain.entities.place import TravelPlace
from travel_planner.domain.exceptions.project import (
    CountPlacesError,
    DuplicatePlaceError,
    ProjectHasVisitedPlacesError,
)


@dataclass(kw_only=True)
class TravelProject:
    """Aggregate Root representing a travel project."""

    name: str
    description: str | None = None
    start_date: date | None = None
    places: list[TravelPlace] = field(default_factory=list[TravelPlace])
    is_completed: bool = field(default=False)
    project_id: UUID = field(default_factory=uuid4)

    def add_place(self, place: TravelPlace) -> None:
        """Add a place to the project, enforcing business rules.

        Raises:
            CountPlacesError: If the project already has the maximum allowed places.
            DuplicatePlaceError: If a place with the same external ID is already in the project.
        """
        if len(self.places) >= 10:
            raise CountPlacesError()

        if any(p.external_id == place.external_id for p in self.places):
            raise DuplicatePlaceError(place.external_id)

        self.places.append(place)
        self._update_completion_status()

    def remove_place(self, place_id: UUID) -> None:
        """Remove a place from the project.

        Raises:
            ProjectHasVisitedPlacesError: If the place has been visited.
        """
        place = next((p for p in self.places if p.place_id == place_id), None)
        if place is None:
            return

        if place.is_visited:
            raise ProjectHasVisitedPlacesError(
                "Cannot remove a place that has been visited."
            )

        self.places.remove(place)
        self._update_completion_status()

    def update_details(
        self,
        name: str | None = None,
        description: str | None = None,
        start_date: date | None = None,
    ) -> None:
        """Update the project's details."""
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if start_date is not None:
            self.start_date = start_date

    def mark_place_visited(self, place_id: UUID) -> None:
        """Mark a specific place as visited and update project status.

        Raises:
            PlaceAlreadyVisitedError: If the place has already been marked as visited.
        """
        place = next((p for p in self.places if p.place_id == place_id), None)
        if place is None:
            return

        place.mark_visited()
        self._update_completion_status()

    def check_can_be_deleted(self) -> None:
        """Verify if the project can be safely deleted.

        Raises:
            ProjectHasVisitedPlacesError: If the project has visited places.
        """
        if any(p.is_visited for p in self.places):
            raise ProjectHasVisitedPlacesError()

    def _update_completion_status(self) -> None:
        """Update the is_completed flag based on places."""
        if not self.places:
            self.is_completed = False
            return

        self.is_completed = all(p.is_visited for p in self.places)
