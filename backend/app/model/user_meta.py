import enum


from app import db
from app.model.participant_relationship import Relationship


class UserMeta(db.Model):
    __tablename__ = 'usermeta'
    __label__ = "User Meta Info"
    user_id = db.Column(db.Integer, db.ForeignKey('stardrive_user.id'), primary_key=True)
    self_participant = db.Column(db.Boolean)
    self_has_guardian = db.Column(db.Boolean)
    guardian = db.Column(db.Boolean)
    guardian_has_dependent = db.Column(db.Boolean)
    professional = db.Column(db.Boolean)
    interested = db.Column(db.Boolean)

    def get_relationship(self):
        if self.self_participant:
            return Relationship.self_interested.name if self.self_has_guardian else Relationship.self_participant.name
        if self.guardian and self.guardian_has_dependent:
            return Relationship.self_guardian.name
        if self.professional:
            return Relationship.professional.name
        # Lower Precedence Relationships
        if self.guardian and not self.guardian_has_dependent:
            return Relationship.self_interested.name
        if self.interested:
            return Relationship.self_interested.name
        return ''

