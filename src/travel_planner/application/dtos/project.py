from dataclasses import dataclass
from datetime import date
from uuid import UUID


@dataclass(frozen=True, slots=True)
class CreateProject:
    """Data transfer object for creating a project."""
    name: str
    external_place_ids: list[int]
    description: str | None = None
    start_date: date | None = None


@dataclass(frozen=True, slots=True)
class UpdateProject:
    """Data transfer object for updating a project."""
    project_id: UUID
    name: str | None = None
    description: str | None = None
    start_date: date | None = None


@dataclass(frozen=True, slots=True)
class RemoveProjectCommand:
    """Data transfer object for removing a project."""
    project_id: UUID


@dataclass(frozen=True, slots=True)
class GetProjectQuery:
    """Data transfer object for getting a single project."""
    project_id: UUID


@dataclass(frozen=True, slots=True)
class GetProjectsQuery:
    """Data transfer object for getting multiple projects."""
    limit: int = 10
    offset: int = 0
