from sqlalchemy import func, Column, Integer, ForeignKey, DateTime, Boolean

from app.database import Base
from app.model.participant_relationship import Relationship


class UserMeta(Base):
    __tablename__ = "usermeta"
    __label__ = "User Meta Info"
    id = Column(Integer, ForeignKey("stardrive_user.id"), primary_key=True)
    last_updated = Column(DateTime(timezone=True), default=func.now())
    self_participant = Column(Boolean)
    self_has_guardian = Column(Boolean)
    guardian = Column(Boolean)
    guardian_has_dependent = Column(Boolean)
    professional = Column(Boolean)
    interested = Column(Boolean)

    def get_relationship(self):
        if self.self_participant:
            return None if self.self_has_guardian else Relationship.self_participant.name
        if self.guardian and self.guardian_has_dependent:
            return Relationship.self_guardian.name
        if self.professional:
            return Relationship.self_professional.name
        # Lower Precedence Relationships
        if self.guardian and not self.guardian_has_dependent:
            return Relationship.self_interested.name
        if self.interested:
            return Relationship.self_interested.name
        return ""
