from sqlalchemy import func, Column, Integer, DateTime, Float

from app.database import Base


class ZipCode(Base):
    __tablename__ = "zip_code"
    id = Column(Integer, primary_key=True)
    latitude = Column(Float)
    longitude = Column(Float)
    last_updated = Column(DateTime(timezone=True), default=func.now())
