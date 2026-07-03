from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class AddProjectPlace:
    """Data transfer object for adding a place to a project."""

    project_id: UUID
    external_id: int
    notes: str = ""


@dataclass(frozen=True, slots=True)
class UpdatePlaceNotes:
    """Data transfer object for updating place notes."""

    project_id: UUID
    place_id: UUID
    notes: str


@dataclass(frozen=True, slots=True)
class RemoveProjectPlaceCommand:
    """Data transfer object for removing a place."""

    project_id: UUID
    place_id: UUID


@dataclass(frozen=True, slots=True)
class MarkPlaceVisitedCommand:
    """Data transfer object for marking a place as visited."""

    project_id: UUID
    place_id: UUID


@dataclass(frozen=True, slots=True)
class GetProjectPlacesQuery:
    """Data transfer object for getting project places."""

    project_id: UUID


@dataclass(frozen=True, slots=True)
class GetPlaceQuery:
    """Data transfer object for getting a single place."""

    place_id: UUID
