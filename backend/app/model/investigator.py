from sqlalchemy import Column, Integer, DateTime, func, String

from app.database import Base


class Investigator(Base):
    __tablename__ = "investigator"
    id = Column(Integer, primary_key=True)
    last_updated = Column(DateTime(timezone=True), default=func.now())
    name = Column(String)
    title = Column(String)
    organization_name = Column(String)
    bio_link = Column(String)
