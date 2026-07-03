from abc import ABC, abstractmethod
from uuid import UUID

from travel_planner.domain.entities.project import TravelProject


class TravelProjectRepository(ABC):
    """Abstract Base Class for the TravelProject repository."""

    @abstractmethod
    async def save(self, project: TravelProject) -> None:
        """Save a TravelProject aggregate.

        Args:
            project (TravelProject): The project to save.
        
        Raises:
            PersistenceError: If a persistence error occurs.
        """
        pass

    @abstractmethod
    async def remove(self, project_id: UUID) -> None:
        """Remove a TravelProject by ID.

        Args:
            project_id (UUID): The ID of the project to remove.

        Raises:
            PersistenceError: If a persistence error occurs.
        """
        pass

    @abstractmethod
    async def get_all(self, limit: int = 10, offset: int = 0) -> list[TravelProject]:
        """Retrieve a list of TravelProjects.

        Args:
            limit (int): Maximum number of projects to retrieve. Defaults to 10.
            offset (int): Number of projects to skip. Defaults to 0.

        Returns:
            list[TravelProject]: A list of travel projects.
            
        Raises:
            PersistenceError: If a persistence error occurs.
        """
        pass

    @abstractmethod
    async def get_by_id(self, project_id: UUID) -> TravelProject | None:
        """Retrieve a TravelProject by its ID.

        Args:
            project_id (UUID): The ID of the project.

        Returns:
            TravelProject | None: The found project or None.
            
        Raises:
            PersistenceError: If a persistence error occurs.
        """
        pass
