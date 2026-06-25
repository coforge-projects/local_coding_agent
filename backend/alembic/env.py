from logging.config import fileConfig
import os

from alembic import context
import asyncio
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlalchemy import pool, create_engine
from alembic import context

from dotenv import load_dotenv
load_dotenv()

from src.agentic_codex.db.models import Base

# Alembic config
config = context.config

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata (models)
target_metadata = Base.metadata




def get_sync_database_url():
  
    db_url = os.getenv("DATABASE_URL")

    if not db_url:
        raise ValueError("DATABASE_URL is not set")

    # convert async URL → sync driver for alembic
    return db_url.replace("aioodbc", "pyodbc")


# ✅ OFFLINE MODE
def run_migrations_offline() -> None:
    url = get_sync_database_url()

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# ✅ ONLINE MODE (FIXED → sync engine)
def run_migrations_online() -> None:
    connectable = create_engine(
        get_sync_database_url(),
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


# ✅ Entry point
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
