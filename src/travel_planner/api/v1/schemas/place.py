from uuid import UUID

from pydantic import BaseModel

from travel_planner.application.dtos.place import AddProjectPlace, UpdatePlaceNotes


class PlaceBase(BaseModel):
    notes: str = ""


class PlaceAddRequest(PlaceBase):
    external_id: int

    def to_dto(self, project_id: UUID) -> AddProjectPlace:
        return AddProjectPlace(
            project_id=project_id,
            external_id=self.external_id,
            notes=self.notes,
        )


class PlaceUpdateRequest(PlaceBase):
    def to_dto(self, project_id: UUID, place_id: UUID) -> UpdatePlaceNotes:
        return UpdatePlaceNotes(
            project_id=project_id,
            place_id=place_id,
            notes=self.notes
        )


class PlaceResponse(PlaceBase):
    place_id: UUID
    external_id: int
    project_id: UUID
    is_visited: bool
