import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

from travel_planner.config import get_settings
from travel_planner.infrastructure.persistence.postgres.models import *  # noqa
from travel_planner.infrastructure.persistence.postgres.models.base import BaseORM

config = context.config

url = get_settings().database_url
config.set_main_option("sqlalchemy.url", url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = BaseORM.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Apply migrations synchronously within a given connection.

    Intended to be called via :func:`AsyncConnection.run_sync` in async mode.

    :param connection: An active SQLAlchemy :class:`~sqlalchemy.engine.Connection`.
    """
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Create an async engine and run migrations against it.

    Uses :class:`~sqlalchemy.pool.NullPool` to avoid connection-pool
    conflicts during migration execution.
    """
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    Creates an async engine, acquires a connection and delegates to
    :func:`run_async_migrations`.  Guards against a ``RuntimeError``
    that would be raised by :func:`asyncio.run` when an event loop is
    already running (e.g. inside a ``pytest-asyncio`` test session).
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        loop.run_until_complete(run_async_migrations())
    else:
        asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()