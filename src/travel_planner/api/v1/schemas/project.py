from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from travel_planner.application.dtos.project import CreateProject, UpdateProject

from .place import PlaceResponse


class ProjectBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    name: str = Field(..., max_length=255, description="The name of the travel project")
    description: str | None = Field(default=None, description="Detailed description of the travel project")
    start_date: date | None = Field(default=None, description="The start date of the travel project")


class ProjectCreateRequest(ProjectBase):
    external_place_ids: list[int] | None = Field(
        default=None, min_length=1, max_length=10, description="List of external place IDs to add to the project"
    )

    def to_dto(self) -> CreateProject:
        return CreateProject(
            name=self.name,
            description=self.description,
            start_date=self.start_date,
            external_place_ids=self.external_place_ids,
        )


class ProjectUpdateRequest(BaseModel):
    name: str | None = Field(default=None, max_length=255, description="The new name of the project")
    description: str | None = Field(default=None, description="The new description of the project")
    start_date: date | None = Field(default=None, description="The new start date of the project")

    def to_dto(self, project_id: UUID) -> UpdateProject:
        return UpdateProject(
            project_id=project_id,
            name=self.name,
            description=self.description,
            start_date=self.start_date,
        )


class ProjectResponse(ProjectBase):
    project_id: UUID = Field(..., description="The unique identifier of the project")
    is_completed: bool = Field(..., description="Whether the project is completed")
    places: list[PlaceResponse] = Field(..., description="List of places associated with the project")
