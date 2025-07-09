import datetime
import enum
import typing

import click
from sqlalchemy import create_engine, MetaData, inspect, DateTime, Enum, Table, select, Select, text
from sqlalchemy.engine import Engine
from sqlalchemy.engine.reflection import Inspector as EngineInspector
from sqlalchemy.orm import DeclarativeBase, sessionmaker, scoped_session, joinedload
from sqlalchemy_utils import database_exists

from app.utils import get_random_integer
from app.utils.decorators import handle_db_connection_errors
from config.load import settings


@handle_db_connection_errors
def _get_db_engine():
    return create_engine(
        settings.SQLALCHEMY_DATABASE_URI,
        echo=settings.SQLALCHEMY_TRACK_MODIFICATIONS,
        pool_pre_ping=True,
    )


engine: Engine = _get_db_engine()


@handle_db_connection_errors
def _create_db(engine_: Engine):
    from sqlalchemy_utils import create_database

    click.secho(f"Recreating database...")
    create_database(engine_.url)
    click.secho(f"\n*** Database {engine_.url.database} created. ***\n")


@handle_db_connection_errors
def _create_tables(base_metadata: MetaData, engine_: Engine):
    click.secho(f"Adding tables from the model...")
    with engine_.begin() as conn:
        click.secho(f"Creating tables...")
        base_metadata.create_all(bind=conn)
        click.secho(f"Done.")


@handle_db_connection_errors
def _delete_tables(base_metadata: MetaData, engine_: Engine):
    """Deletes all tables in the given database in reverse dependency order"""

    # Clear out any tables that may have been created
    click.secho(f"Deleting tables from database {engine_.url.database}...", color=True, fg="yellow")
    for table in reversed(base_metadata.sorted_tables):
        # Delete all rows in the table
        with engine.begin() as conn:
            # Check if table exists
            if engine.dialect.has_table(conn, table.name):
                conn.execute(table.delete())


class Base(DeclarativeBase):
    __allow_unmapped__ = True
    type_annotation_map = {
        enum.Enum: Enum(enum.Enum, native_enum=False),
        typing.Literal: Enum(enum.Enum, native_enum=False),
        datetime.datetime: DateTime(),
    }


Base.metadata.bind = engine


@handle_db_connection_errors
def _create_db_and_tables():
    if not database_exists(engine.url):
        _create_db(engine)
        _create_tables(Base.metadata, engine)


_create_db_and_tables()


@handle_db_connection_errors
def _get_session():
    return scoped_session(
        sessionmaker(
            bind=engine,
            autoflush=True,
            expire_on_commit=False,
        )
    )


session = _get_session()


# Create an inspector to inspect the database schema
@handle_db_connection_errors
def _get_inspector():
    return inspect(engine)


inspector: EngineInspector = _get_inspector()


@handle_db_connection_errors
def _reset_table_id_sequences(base_metadata: MetaData, engine_: Engine):
    click.secho(f"Resetting id sequences for {engine_.url.database} tables...")
    for table in reversed(base_metadata.sorted_tables):
        with engine.begin() as conn:
            if engine.dialect.has_table(conn, table.name):
                sequence_name = f"{table.name}_id_seq"
                conn.execute(text(f"ALTER SEQUENCE IF EXISTS {sequence_name} RESTART WITH 1"))


@handle_db_connection_errors
def clear_db(base_metadata: MetaData = Base.metadata):
    base_metadata.bind = engine

    if database_exists(engine.url):
        # Delete all tables in reverse dependency order
        _delete_tables(base_metadata, engine)
    else:
        _create_db(engine)

    _create_tables(base_metadata, engine)
    _reset_table_id_sequences(base_metadata, engine)


@handle_db_connection_errors
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


@handle_db_connection_errors
def upgrade_db():
    """Runs Alembic database migrations"""
    import os
    from alembic.command import upgrade
    from alembic.config import Config
    from inspect import getsourcefile

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


@handle_db_connection_errors
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


@handle_db_connection_errors
def get_class_for_table(table: Table):
    """Gets Python class matching the given SQLAlchemy table's name"""
    from sqlalchemy_utils import get_class_by_table

    return get_class_by_table(Base, table)


@handle_db_connection_errors
def get_class(class_name: str):
    """Gets Python class matching the given class name"""

    for c in Base.registry._class_registry.values():
        if hasattr(c, "__name__") and c.__name__ == class_name:
            return c


@handle_db_connection_errors
def _select_by_id(model, object_id: int, joins: list = None):
    """Selects a record by its id"""
    statement = _add_joins(select(model), joins)
    return statement.filter_by(id=object_id)


@handle_db_connection_errors
def _add_joins(statement: Select, joins: list = None):
    """Adds joins to a select statement"""
    joins = joins or []

    for join in joins:
        statement = statement.options(joinedload(join))

    return statement


@handle_db_connection_errors
def get_db_object_by_id(model, object_id: int, joins: list = None):
    """Gets a record from the given model by its id, closes the session, and returns the object."""
    statement = _select_by_id(model, object_id, joins)
    result = session.execute(statement).unique().scalar_one_or_none()
    # session.close()
    return result


@handle_db_connection_errors
def get_all_db_objects(model, order_by=None, joins: list = None):
    """Gets all records from the given model, closes the session, and returns the objects."""
    statement = select(model).order_by(order_by) if order_by else select(model)
    statement = _add_joins(statement, joins)
    result = session.execute(statement).unique().scalars().all()
    # session.close()
    return result
