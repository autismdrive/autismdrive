from sqlalchemy import func, Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship

from app.database import Base
from app.model.resource import Resource
from app.model.user import User


class AdminNote(Base):
    __tablename__ = "admin_note"
    id = Column(Integer, primary_key=True)
    resource_id = Column("resource_id", Integer, ForeignKey("resource.id"))
    user_id = Column("user_id", Integer, ForeignKey("stardrive_user.id"))
    user = relationship(User, backref="admin_notes")
    resource = relationship(Resource, backref="admin_notes")
    last_updated = Column(DateTime(timezone=True), default=func.now())
    note = Column(String)
