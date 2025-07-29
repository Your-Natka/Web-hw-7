# pylint: disable=no-member, wrong-import-order, missing-module-docstring, missing-function-docstring

from logging.config import fileConfig
import sys
import os

from sqlalchemy import engine_from_config, pool
from alembic import context 

# Додаємо корінь проєкту до PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.models import Base
# Імпортуємо Base з твоїх моделей


# Alembic Config
config = context.config

# URL до бази даних
DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/students_db"

config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Налаштування логування
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Встановлюємо metadata для автогенерації
target_metadata = Base.metadata

# Два режими: offline/online
def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        url=DATABASE_URL  # Додаємо явно URL
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()

# Запуск
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()