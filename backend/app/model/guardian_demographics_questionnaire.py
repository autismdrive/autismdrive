import datetime

from app import db


class GuardianDemographicsQuestionnaire(db.Model):
    __tablename__ = 'guardian_demographics_questionnaire'
    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime, default=datetime.datetime.now)
    guardian_id = db.Column('guardian_id', db.Integer, db.ForeignKey('stardrive_user.id'))
    birthdate = db.Column(db.Date)
    sex = db.Column(db.String)
    race_ethnicity = db.Column(db.String)
    is_english_primary = db.Column(db.Boolean)
    relationship_to_child = db.Column(db.String)
