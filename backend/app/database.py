from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

from config.load import settings

engine: Engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, echo=settings.SQLALCHEMY_TRACK_MODIFICATIONS)
db: SQLAlchemy = SQLAlchemy(session_options={"bind": engine})
session: scoped_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
