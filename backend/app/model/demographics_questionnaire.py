import datetime

from app import db


class DemographicsQuestionnaire(db.Model):
    __tablename__ = 'demographics_questionnaire'
    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime, default=datetime.datetime.now)
    participant_id = db.Column('participant_id', db.Integer, db.ForeignKey('stardrive_user.id'))
    guardian_id = db.Column('guardian_id', db.Integer, db.ForeignKey('stardrive_user.id'))
    first_name = db.Column(db.String)
    middle_name = db.Column(db.String)
    last_name = db.Column(db.String)
    is_first_name_preferred = db.Column(db.Boolean)
    nickname = db.Column(db.String)
    birthdate = db.Column(db.Date)
    birth_city = db.Column(db.String)
    birth_state = db.Column(db.String)
    birth_sex = db.Column(db.String)
    current_gender = db.Column(db.String)
    race_ethnicity = db.Column(db.String)
    is_english_primary = db.Column(db.Boolean)
