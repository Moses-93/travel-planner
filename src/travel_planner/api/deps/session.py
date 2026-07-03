from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession


async def get_db_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    sessionmaker = request.app.state.sessionmaker
    async with sessionmaker() as session:
        yield session


SessionDependency = Annotated[AsyncSession, Depends(get_db_session)]
