from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends

from travel_planner.api.deps.session import SessionDependency
from travel_planner.application.interfaces.uow import UnitOfWork
from travel_planner.infrastructure.persistence.postgres.uow import PostgresUnitOfWork


async def get_uow(session: SessionDependency) -> AsyncGenerator[UnitOfWork, None]:
    async with PostgresUnitOfWork(session=session) as uow:
        yield uow

UoWDependency = Annotated[UnitOfWork, Depends(get_uow)]
