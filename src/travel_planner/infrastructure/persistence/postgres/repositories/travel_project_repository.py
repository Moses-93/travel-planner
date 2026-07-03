from uuid import UUID

from sqlalchemy import delete, exists, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from travel_planner.domain.entities.project import TravelProject
from travel_planner.domain.repositories.project_repository import (
    TravelProjectRepository,
)
from travel_planner.infrastructure.persistence.postgres.error_mapping import (
    process_sqlalchemy_error,
)
from travel_planner.infrastructure.persistence.postgres.models import (
    TravelPlaceORM,
    TravelProjectORM,
)


class PostgresTravelProjectRepository(TravelProjectRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @process_sqlalchemy_error
    async def save(self, project: TravelProject) -> None:
        is_existing = await self._session.scalar(
            select(exists().where(TravelProjectORM.project_id == project.project_id))
        )
        if is_existing:
            await self._update(project)
        else:
            await self._create(project)

    async def _create(self, project: TravelProject) -> None:
        orm_project = TravelProjectORM.from_entity(project)
        self._session.add(orm_project)
        await self._session.flush()

    async def _update(self, project: TravelProject) -> None:
        project_stmt = (
            insert(TravelProjectORM)
            .values(
                project_id=project.project_id,
                name=project.name,
                description=project.description,
                start_date=project.start_date,
                is_completed=project.is_completed,
            )
            .on_conflict_do_update(
                index_elements=["project_id"],
                set_={
                    "name": project.name,
                    "description": project.description,
                    "start_date": project.start_date,
                    "is_completed": project.is_completed,
                },
            )
        )
        await self._session.execute(project_stmt)

        if project.places:
            place_dicts = [
                {
                    "place_id": p.place_id,
                    "external_id": p.external_id,
                    "project_id": p.project_id,
                    "notes": p.notes,
                    "is_visited": p.is_visited,
                }
                for p in project.places
            ]
            places_stmt = insert(TravelPlaceORM).values(place_dicts)
            places_stmt = places_stmt.on_conflict_do_update(
                index_elements=["project_id", "external_id"],
                set_={
                    "notes": places_stmt.excluded.notes,
                    "is_visited": places_stmt.excluded.is_visited,
                },
            )
            await self._session.execute(places_stmt)

        place_ids = [p.place_id for p in project.places]
        delete_stmt = delete(TravelPlaceORM).where(
            TravelPlaceORM.project_id == project.project_id
        )
        if place_ids:
            delete_stmt = delete_stmt.where(TravelPlaceORM.place_id.notin_(place_ids))
        await self._session.execute(delete_stmt)
        await self._session.flush()

    @process_sqlalchemy_error
    async def remove(self, project_id: UUID) -> None:
        project = await self._session.get(TravelProjectORM, project_id)
        if project:
            await self._session.delete(project)
            await self._session.flush()

    @process_sqlalchemy_error
    async def get_all(self, limit: int = 10, offset: int = 0) -> list[TravelProject]:
        stmt = (
            select(TravelProjectORM)
            .options(selectinload(TravelProjectORM.places))
            .limit(limit)
            .offset(offset)
        )
        models = (await self._session.scalars(stmt)).all()
        return [m.to_entity() for m in models]

    @process_sqlalchemy_error
    async def get_by_id(self, project_id: UUID) -> TravelProject | None:
        stmt = (
            select(TravelProjectORM)
            .options(selectinload(TravelProjectORM.places))
            .where(TravelProjectORM.project_id == project_id)
        )
        orm_project = await self._session.scalar(stmt)
        if orm_project:
            return orm_project.to_entity()
        return None
