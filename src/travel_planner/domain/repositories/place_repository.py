from abc import ABC, abstractmethod
from uuid import UUID

from travel_planner.domain.entities.place import TravelPlace


class TravelPlaceRepository(ABC):
    """Abstract Base Class for the TravelPlace repository (read operations mainly)."""

    @abstractmethod
    async def get_by_project_id(self, project_id: UUID) -> list[TravelPlace]:
        """Retrieve all TravelPlaces associated with a project.

        Args:
            project_id (UUID): The ID of the project.

        Returns:
            list[TravelPlace]: A list of places in the project.
            
        Raises:
            PersistenceError: If a persistence error occurs.
        """
        pass

    @abstractmethod
    async def get_by_id(self, place_id: UUID) -> TravelPlace | None:
        """Retrieve a TravelPlace by its ID.

        Args:
            place_id (UUID): The ID of the place.

        Returns:
            TravelPlace | None: The found place or None.
            
        Raises:
            PersistenceError: If a persistence error occurs.
        """
        pass
