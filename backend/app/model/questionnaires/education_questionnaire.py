import datetime

from marshmallow_sqlalchemy import ModelSchema

from app import db


class EducationQuestionnaire(db.Model):
    __tablename__ = 'education_questionnaire'
    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime, default=datetime.datetime.now)
    participant_id = db.Column(
        'participant_id',
        db.Integer,
        db.ForeignKey('stardrive_participant.id')
    )
    user_id = db.Column(
        'user_id',
        db.Integer,
        db.ForeignKey('stardrive_user.id')
    )
    attends_school = db.Column(
        db.Boolean
    )
    school_name = db.Column(
        db.String
    )
    current_grade = db.Column(
        db.String
    )
    school_services = db.Column(
        db.String
    )
    school_services_other = db.Column(
        db.String
    )

    def get_meta(self):
        info = {
            'table': {
                'sensitive': False,
                'label': 'Education',
                'description': '',
            }
        }
        for c in self.metadata.tables['education_questionnaire'].columns:
            if c.info:
                info[c.name] = c.info
        return info


class EducationQuestionnaireSchema(ModelSchema):
    class Meta:
        model = EducationQuestionnaire
        fields = ('id', 'last_updated', 'participant_id', 'user_id', 'attends_school', 'school_name', 'current_grade',
                  'school_services', 'school_services_other')


class EducationQuestionnaireMetaSchema(ModelSchema):
    class Meta:
        model = EducationQuestionnaire
        fields = ('get_meta',)

