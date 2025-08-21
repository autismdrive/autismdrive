import datetime
import enum
import typing

import click
from psycopg import OperationalError
from sqlalchemy import DateTime, Enum, MetaData, Select, Table, create_engine, inspect, select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, joinedload, scoped_session, sessionmaker
from sqlalchemy_utils import database_exists

from app.utils import get_random_integer
from config.load import settings

engine: Engine = create_engine(
    url=settings.SQLALCHEMY.get_uri(),
    echo=settings.SQLALCHEMY.track_modifications,
    pool_pre_ping=True,
)


def _create_db(engine_: Engine):
    from sqlalchemy_utils import create_database

    try:
        click.secho("Recreating database...")
        create_database(engine_.url)
        click.secho(f"\n*** Database {engine_.url.database} created. ***\n")

    except OperationalError as e:
        click.secho(f"Error creating database: {e}. Make sure the database server is running.", fg="red")


def _create_tables(base_metadata: MetaData, engine_: Engine):
    try:
        click.secho("Adding tables from the model...")
        with engine_.begin() as conn:
            click.secho("Creating tables...")
            base_metadata.create_all(bind=conn)
            click.secho("Done.")
    except Exception as e:
        click.secho(f"Error connecting to database: {e}")


def _delete_all_tables(base_metadata: MetaData, engine_: Engine):
    """Deletes all tables in the given database in reverse dependency order"""

    # Clear out any tables that may have been created
    click.secho(f"Deleting tables from database {engine_.url.database}...")
    try:
        # Delete all tables
        with engine.begin() as conn:
            for t in base_metadata.sorted_tables:
                conn.execute(t.delete())

        click.secho("Deleted all tables.")
    except Exception as e:
        click.secho(f"Error deleting tables: {e}", fg="red")


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

if len(inspect(engine).get_table_names()) == 0:
    click.secho(f"Database {engine.url.database} is empty, creating tables...")
    _create_tables(Base.metadata, engine)

session = scoped_session(
    sessionmaker(
        bind=engine,
        autoflush=True,
        expire_on_commit=False,
    )
)
inspector = inspect(engine)


def clear_db(base_metadata: MetaData = Base.metadata):
    from sqlalchemy_utils import drop_database

    drop_database(engine.url)

    _create_db(engine)
    _create_tables(base_metadata, engine)


def migrate_db():
    """Runs Alembic database migrations"""
    import os
    from inspect import getsourcefile

    from alembic.command import revision
    from alembic.config import Config

    current_dir = os.path.dirname(getsourcefile(lambda: 0))
    alembic_cfg = Config(current_dir + "/../migrations/alembic.ini")
    alembic_cfg.set_main_option("script_location", current_dir + "/../migrations")
    revision(config=alembic_cfg, autogenerate=True, message="auto")


def upgrade_db():
    """Runs Alembic database migrations"""
    import os
    from inspect import getsourcefile

    from alembic.command import upgrade
    from alembic.config import Config

    current_dir = os.path.dirname(getsourcefile(lambda: 0))
    alembic_cfg = Config(current_dir + "/../migrations/alembic.ini")
    alembic_cfg.set_main_option("script_location", current_dir + "/../migrations")

    # Check if the database is already populated, but has no Alembic version yet.
    # If so, we need to create the Alembic version table before we can upgrade.
    if not inspector.has_table("alembic_version"):
        from alembic.command import stamp

        # Check if the database is already populated
        num_tables = len(inspector.get_table_names())
        num_models = len(Base.metadata.tables)
        if num_tables >= num_models:
            # The database is already populated, but has no Alembic version yet.
            # Stamp it with the current revision.
            stamp(config=alembic_cfg, revision="head")

    upgrade(config=alembic_cfg, revision="head")


def random_integer(context) -> int:
    """
    Returns a random integer id that is not already in the database.

    Generates a random integer for use as ids for users, participants and the like
    where we want to avoid incremental ids that might be easy to guess.

    The context here is passed in by SQLAlchemy and allows us to check details of
    the query to make sure the id doesn't exist, though this is highly unlikely.
    """

    id_ = get_random_integer()

    while get_db_object_by_id(context.current_column.table, id_) is not None:
        id_ = get_random_integer()

    return id_


def get_class_for_table(table: Table):
    """Gets Python class matching the given SQLAlchemy table's name"""
    from sqlalchemy_utils import get_class_by_table

    return get_class_by_table(Base, table)


def get_class(class_name: str):
    """Gets Python class matching the given class name"""

    for c in Base.registry._class_registry.values():
        if hasattr(c, "__name__") and c.__name__ == class_name:
            return c


def _select_by_id(model, object_id: int, joins: list = None):
    """Selects a record by its id"""
    statement = _add_joins(select(model), joins)
    return statement.filter_by(id=object_id)


def _add_joins(statement: Select, joins: list = None):
    """Adds joins to a select statement"""
    joins = joins or []

    for join in joins:
        statement = statement.options(joinedload(join))

    return statement


def get_db_object_by_id(model, object_id: int, joins: list = None):
    """Gets a record from the given model by its id, closes the session, and returns the object."""
    statement = _select_by_id(model, object_id, joins)
    result = session.execute(statement).unique().scalar_one_or_none()
    # session.close()
    return result


def get_all_db_objects(model, order_by=None, joins: list = None):
    """Gets all records from the given model, closes the session, and returns the objects."""
    statement = select(model).order_by(order_by) if order_by else select(model)
    statement = _add_joins(statement, joins)
    result = session.execute(statement).unique().scalars().all()
    # session.close()
    return result
