from sqlalchemy import func, Column, Integer, String, DateTime

from app.database import Base


class ResourceChangeLog(Base):
    __tablename__ = "resource_change_log"
    id = Column(Integer, primary_key=True)
    type = Column(String)
    user_id = Column(Integer)
    user_email = Column(String)
    resource_id = Column(Integer)
    resource_title = Column(String)
    last_updated = Column(DateTime(timezone=True), default=func.now())
