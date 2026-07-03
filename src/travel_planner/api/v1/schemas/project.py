from datetime import date
from uuid import UUID

from pydantic import BaseModel, Field

from travel_planner.application.dtos.project import CreateProject, UpdateProject

from .place import PlaceResponse


class ProjectBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: str | None = None
    start_date: date | None = None


class ProjectCreateRequest(ProjectBase):
    external_place_ids: list[int] = Field(..., min_length=1, max_length=10)

    def to_dto(self) -> CreateProject:
        return CreateProject(
            name=self.name,
            description=self.description,
            start_date=self.start_date,
            external_place_ids=self.external_place_ids,
        )


class ProjectUpdateRequest(BaseModel):
    name: str | None = Field(None, max_length=255)
    description: str | None = None
    start_date: date | None = None

    def to_dto(self, project_id: UUID) -> UpdateProject:
        return UpdateProject(
            project_id=project_id,
            name=self.name,
            description=self.description,
            start_date=self.start_date,
        )


class ProjectResponse(ProjectBase):
    project_id: UUID
    is_completed: bool
    places: list[PlaceResponse]
