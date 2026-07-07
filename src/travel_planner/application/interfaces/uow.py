from __future__ import annotations

from types import TracebackType
from typing import AsyncContextManager, Protocol, Self


class UnitOfWork(Protocol):
    """Interface for the Unit of Work pattern.
    Defines the contract for managing database transactions.
    """

    def transaction(self) -> AsyncContextManager[Self]:
        """Return an asynchronous context manager for managing transactions.
        Commits automatically on successful exit, and rolls back on an exception.
        """
        ...

    async def __aenter__(self) -> Self:
        """Enter the context manager.
        Returns the unit of work.
        """
        ...

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
        /
    ) -> None:
        """Exit the context manager.
        Commits the transaction if no exception is raised, otherwise rolls back.
        """
        ...
