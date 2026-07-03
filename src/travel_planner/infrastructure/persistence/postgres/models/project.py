from datetime import date
from uuid import UUID

from sqlalchemy import Boolean, Date, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from travel_planner.domain.entities.project import TravelProject
from travel_planner.infrastructure.persistence.postgres.models.base import BaseORM
from travel_planner.infrastructure.persistence.postgres.models.place import (
    TravelPlaceORM,
)


class TravelProjectORM(BaseORM):
    __tablename__ = "travel_projects"

    project_id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    places: Mapped[list[TravelPlaceORM]] = relationship(
        "TravelPlaceORM",
        back_populates="project",
        cascade="all, delete-orphan",
        primaryjoin="TravelProjectORM.project_id == foreign(TravelPlaceORM.project_id)",
    )

    def to_entity(self) -> TravelProject:
        return TravelProject(
            project_id=self.project_id,
            name=self.name,
            description=self.description,
            start_date=self.start_date,
            is_completed=self.is_completed,
            places=[place.to_entity() for place in self.places],
        )

    @classmethod
    def from_entity(cls, entity: TravelProject) -> "TravelProjectORM":
        return cls(
            project_id=entity.project_id,
            name=entity.name,
            description=entity.description,
            start_date=entity.start_date,
            is_completed=entity.is_completed,
            places=[TravelPlaceORM.from_entity(place) for place in entity.places],
        )
