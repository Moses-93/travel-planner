from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from travel_planner.domain.entities.place import TravelPlace
from travel_planner.domain.repositories.place_repository import TravelPlaceRepository
from travel_planner.infrastructure.persistence.postgres.error_mapping import (
    process_sqlalchemy_error,
)
from travel_planner.infrastructure.persistence.postgres.models.place import (
    TravelPlaceORM,
)


class PostgresTravelPlaceRepository(TravelPlaceRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @process_sqlalchemy_error
    async def get_by_project_id(self, project_id: UUID) -> list[TravelPlace]:
        stmt = select(TravelPlaceORM).where(TravelPlaceORM.project_id == project_id)
        models = (await self._session.scalars(stmt)).all()
        return [m.to_entity() for m in models]

    @process_sqlalchemy_error
    async def get_by_id(self, place_id: UUID) -> TravelPlace | None:
        orm_place = await self._session.get(TravelPlaceORM, place_id)
        if orm_place:
            return orm_place.to_entity()
        return None
