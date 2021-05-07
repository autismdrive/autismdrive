import enum


from app import db
from app.model.participant_relationship import Relationship


class UserMeta(db.Model):
    __tablename__ = 'usermeta'
    __label__ = "User Meta Info"
    user_id = db.Column(db.Integer, db.ForeignKey('stardrive_user.id'), primary_key=True)
    self_has_guardian = db.Column(db.Boolean)
    self_own_guardian = db.Column(db.Boolean)
    guardian_legal = db.Column(db.Boolean)
    guardian_not_legal = db.Column(db.Boolean)
    professional = db.Column(db.Boolean)
    interested = db.Column(db.Boolean)

    def get_flow(self):
        if self.self_own_guardian: return Relationship.self_participant
        if self.guardian_legal: return Relationship.self_guardian
        if self.professional: return Relationship.self_professional
        elif self.guardian_not_legal or self.interested or self.self_has_guardian:
            return Relationship.self_interested

