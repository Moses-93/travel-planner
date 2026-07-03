from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from travel_planner.application.dtos.place import AddProjectPlace, UpdatePlaceNotes


class PlaceBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    notes: str = Field(default="", description="Notes added by the user for the place")


class PlaceAddRequest(PlaceBase):
    external_id: int = Field(..., description="The external identifier of the place from the third-party API")

    def to_dto(self, project_id: UUID) -> AddProjectPlace:
        return AddProjectPlace(
            project_id=project_id,
            external_id=self.external_id,
            notes=self.notes,
        )


class PlaceUpdateRequest(PlaceBase):
    def to_dto(self, project_id: UUID, place_id: UUID) -> UpdatePlaceNotes:
        return UpdatePlaceNotes(
            project_id=project_id, place_id=place_id, notes=self.notes
        )


class PlaceResponse(PlaceBase):
    place_id: UUID = Field(..., description="The unique identifier of the place")
    external_id: int = Field(..., description="The external identifier of the place from the third-party API")
    project_id: UUID = Field(..., description="The unique identifier of the project this place belongs to")
    is_visited: bool = Field(..., description="Indicates whether the place has been marked as visited")
