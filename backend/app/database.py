import datetime
import enum
import typing
from random import randint

import click
from icecream import ic
from sqlalchemy import create_engine, MetaData, inspect, DateTime, Enum, Table
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, scoped_session
from sqlalchemy_utils import database_exists

from config.load import settings

engine: Engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    echo=settings.SQLALCHEMY_TRACK_MODIFICATIONS,
    pool_pre_ping=True,
)


def _create_db(engine_: Engine):
    from sqlalchemy_utils import create_database

    try:
        click.secho(f"Recreating database...")
        create_database(engine_.url)
        click.secho(f"\n*** Database {engine_.url.database} created. ***\n")

    except Exception as e:
        click.secho(f"Error creating database: {e}")
        raise e


def _create_tables(base_metadata: MetaData, engine_: Engine):
    try:
        click.secho(f"Adding tables from the model...")
        with engine_.begin() as conn:
            click.secho(f"Creating tables...")
            base_metadata.create_all(bind=conn)
            click.secho(f"Done.")
    except Exception as e:
        click.secho(f"Error connecting to database: {e}")


def _delete_tables(base_metadata: MetaData, engine_: Engine):
    # Delete all tables in reverse dependency order

    # Clear out any tables that may have been created
    click.secho(f"Deleting tables from database {engine_.url.database}...")
    for table in reversed(base_metadata.sorted_tables):
        try:
            # Delete all rows in the table
            with engine.begin() as conn:
                # Check if table exists
                if engine.dialect.has_table(conn, table.name):
                    conn.execute(table.delete())
        except Exception as e:
            click.secho(f"Error cleaning table {table.name}: {e}")


def _delete_db(base_metadata: MetaData, engine_: Engine):
    """Deletes the database to reset any auto-increment id values"""
    from sqlalchemy_utils import drop_database

    try:
        click.secho(f"Dropping database: {engine.url.database}...")
        drop_database(engine.url)
        click.secho(f"Dropped database: {engine.url.database}.")
    except Exception as e:
        click.secho(f"Error deleting database: {e}")


class Base(DeclarativeBase):
    __allow_unmapped__ = True
    type_annotation_map = {
        enum.Enum: Enum(enum.Enum, native_enum=False),
        typing.Literal: Enum(enum.Enum, native_enum=False),
        datetime.datetime: DateTime(),
    }


Base.metadata.bind = engine


if not database_exists(engine.url):

    _create_db(engine)
    _create_tables(Base.metadata, engine)

ic.configureOutput(includeContext=True, contextAbsPath=True)
ic(settings.SQLALCHEMY_DATABASE_URI)

session = scoped_session(
    sessionmaker(
        bind=engine,
        autoflush=True,
        expire_on_commit=False,
    )
)
inspector = inspect(engine)


def clear_db(base_metadata: MetaData = Base.metadata):
    base_metadata.bind = engine

    if database_exists(engine.url):
        # Delete all tables in reverse dependency order
        _delete_tables(base_metadata, engine)

        # Delete the database itself to reset any auto-increment id values
        _delete_db(base_metadata, engine)

    _create_db(engine)
    _create_tables(base_metadata, engine)


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
