import datetime
import enum
import typing
from random import randint

import click
from sqlalchemy import create_engine, MetaData, inspect, DateTime, Enum, Table
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, scoped_session
from sqlalchemy_utils import database_exists, create_database

from config.load import settings

engine: Engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, echo=settings.SQLALCHEMY_TRACK_MODIFICATIONS)

if not database_exists(engine.url):
    try:
        create_database(engine.url)
    except Exception as e:
        click.secho(f"Error creating database: {e}")
        raise e

session = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=True, expire_on_commit=False))
inspector = inspect(engine)


class Base(DeclarativeBase):
    __allow_unmapped__ = True

    type_annotation_map = {
        enum.Enum: Enum(enum.Enum, native_enum=False),
        typing.Literal: Enum(enum.Enum, native_enum=False),
        datetime.datetime: DateTime(timezone=True),
    }


Base.metadata.bind = engine
inspector = inspect(engine)


def clear_db(base_metadata: MetaData = Base.metadata):
    if not database_exists(engine.url):
        try:
            create_database(engine.url)
        except Exception as e:
            click.secho(f"Error creating database: {e}")
            raise e

    # Delete all tables in reverse dependency order
    Base.metadata.bind = engine

    # Clear out any tables that may have been created
    for table in reversed(base_metadata.sorted_tables):
        try:
            # Delete all rows in the table
            with engine.begin() as conn:
                conn.execute(table.delete())
        except Exception as e:
            click.secho(f"Error cleaning table {table.name}: {e}")

    # Delete the database itself to reset any auto-increment id values
    try:
        base_metadata.drop_all(bind=engine, checkfirst=False)
    except Exception as e:
        click.secho(f"Error deleting database: {e}")

    try:
        # Recreate the database
        base_metadata.create_all(bind=engine)
    except Exception as e:
        click.secho(f"Error connecting to database: {e}")


def migrate_db():
    """Runs Alembic database migrations"""
    import os
    from alembic.command import revision
    from alembic.config import Config
    from inspect import getsourcefile

    current_dir = os.path.dirname(getsourcefile(lambda: 0))
    alembic_cfg = Config(current_dir + "/../migrations/alembic.ini")
    alembic_cfg.set_main_option("script_location", current_dir + "/../migrations")
    revision(config=alembic_cfg, autogenerate=True, message="auto")


def upgrade_db():
    """Runs Alembic database migrations"""
    import os
    from alembic.command import upgrade
    from alembic.config import Config
    from inspect import getsourcefile

    current_dir = os.path.dirname(getsourcefile(lambda: 0))
    alembic_cfg = Config(current_dir + "/../migrations/alembic.ini")
    alembic_cfg.set_main_option("script_location", current_dir + "/../migrations")
    upgrade(config=alembic_cfg, revision="head")


def random_integer(context):
    """
    Generates a random integer for use as ids for users, participants and the like
    where we want to avoid incremental ids that might be easy to guess.
    The context here is passed in by SQLAlchemy and allows us to check details of
    the query to make sure the id doesn't exist, though this is highly unlikely.
    """
    min_ = 100
    max_ = 1000000000
    rand = randint(min_, max_)

    # possibility of same random number is very low.
    # but if you want to make sure, here you can check id exists in database.
    while session.query(context.current_column.table).filter(id == rand).limit(1).first() is not None:
        rand = randint(min_, max_)

    return rand


def get_class_for_table(table: Table):
    """Gets Python class matching the given SQLAlchemy table's name"""
    from sqlalchemy_utils import get_class_by_table

    return get_class_by_table(Base, table)


def get_class(class_name: str):
    """Gets Python class matching the given class name"""

    for c in Base.registry._class_registry.values():
        if hasattr(c, "__name__") and c.__name__ == class_name:
            return c
