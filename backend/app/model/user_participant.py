import enum

from sqlalchemy import Enum

from app import db
from sqlalchemy.ext.declarative import declarative_base

from app.model.participant import Participant
from app.model.user import User
Base = declarative_base()


# Describes the relationship between the User model and the participant
class Relationship(enum.Enum):
    self_participant = 1
    self_guardian = 2
    dependent = 3

    @classmethod
    def has_name(cls, name):
        return any(name == item.name for item in cls)

    @classmethod
    def options(cls):
        return [item.name for item in cls]

class UserParticipant(db.Model):
    __tablename__ = 'user_participant'

    id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(db.Integer, db.ForeignKey(Participant.id), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    participant = db.relationship(Participant, backref='participant_users')
    user = db.relationship(User, backref='user_participants')
    relationship = db.Column(Enum(Relationship))
