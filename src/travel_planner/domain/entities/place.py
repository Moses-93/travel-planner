from dataclasses import dataclass, field
from uuid import UUID, uuid4

from travel_planner.domain.exceptions.project import PlaceAlreadyVisitedError


@dataclass(slots=True, kw_only=True)
class TravelPlace:
    """Entity representing a place within a travel project."""

    external_id: int
    project_id: UUID
    notes: str = ""
    is_visited: bool = False
    place_id: UUID = field(default_factory=uuid4)

    def update_notes(self, notes: str) -> None:
        """Update notes for the place."""
        self.notes = notes

    def mark_visited(self) -> None:
        """Mark the place as visited.

        Raises:
            PlaceAlreadyVisitedError: If the place has already been marked as visited.
        """
        if self.is_visited:
            raise PlaceAlreadyVisitedError()

        self.is_visited = True
