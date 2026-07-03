from uuid import UUID

from sqlalchemy import Boolean, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import UniqueConstraint

from travel_planner.domain.entities.place import TravelPlace
from travel_planner.infrastructure.persistence.postgres.models.base import BaseORM


class TravelPlaceORM(BaseORM):
    __tablename__ = "travel_places"
    __table_args__ = (
        UniqueConstraint("project_id", "external_id", name="uq_project_external_place"),
    )

    place_id: Mapped[UUID] = mapped_column(primary_key=True)
    external_id: Mapped[int] = mapped_column(nullable=False)
    project_id: Mapped[UUID] = mapped_column(ForeignKey("travel_projects.project_id", ondelete="CASCADE"), nullable=False)
    notes: Mapped[str] = mapped_column(Text, default="", nullable=False)
    is_visited: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    project: Mapped["TravelProjectORM"] = relationship(
        "TravelProjectORM",
        back_populates="places",
    )

    def to_entity(self) -> TravelPlace:
        return TravelPlace(
            place_id=self.place_id,
            external_id=self.external_id,
            project_id=self.project_id,
            notes=self.notes,
            is_visited=self.is_visited,
        )

    @classmethod
    def from_entity(cls, entity: TravelPlace) -> "TravelPlaceORM":
        return cls(
            place_id=entity.place_id,
            external_id=entity.external_id,
            project_id=entity.project_id,
            notes=entity.notes,
            is_visited=entity.is_visited,
        )
