from app import db
from sqlalchemy.ext.declarative import declarative_base

from app.model.participant import Participant
from app.model.user import User
Base = declarative_base()


class UserParticipant(db.Model):
    __tablename__ = 'user_participant'
    id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(db.Integer, db.ForeignKey(Participant.id), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    participant = db.relationship(Participant, backref='participant_users')
    user = db.relationship(User, backref='user_participants')
    relationship = db.Column(db.String)
