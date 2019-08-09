import datetime
import enum

from dateutil.tz import tzutc
from marshmallow_enum import EnumField
from marshmallow_sqlalchemy import ModelSchema
from sqlalchemy import func

from app import db


# Describes the relationship between the User model and the participant
from app.model.questionnaires.identification_questionnaire import IdentificationQuestionnaire


class Relationship(enum.Enum):
    self_participant = 1
    self_guardian = 2
    dependent = 3
    self_professional = 4

    @classmethod
    def has_name(cls, name):
        return any(name == item.name for item in cls)

    @classmethod
    def options(cls):
        return [item.name for item in cls]


class Participant(db.Model):
    # The participant model is used to track enrollment and participation in studies. Participants are associated
    # with a user account; sometimes that of themselves and sometimes that of their guardian.
    __tablename__ = 'stardrive_participant'
    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('stardrive_user.id'))
    user = db.relationship("User", back_populates="participants")
    identification = db.relationship(IdentificationQuestionnaire, uselist=False)
    relationship = db.Column(db.Enum(Relationship))
    avatar_icon = db.Column(db.String)
    avatar_color = db.Column(db.String)
    has_consented = db.Column(db.Boolean)

    def get_name(self):
        if self.identification:
            return self.identification.get_name()
        else:
            return ""