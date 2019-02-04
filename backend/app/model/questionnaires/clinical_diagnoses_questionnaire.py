import datetime

from marshmallow_sqlalchemy import ModelSchema

from app import db


class ClinicalDiagnosesQuestionnaire(db.Model):
    __tablename__ = 'clinical_diagnoses_questionnaire'
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
    developmental = db.Column(
        db.String
    )
    mental_health = db.Column(
        db.String
    )
    medical = db.Column(
        db.String
    )
    genetic_conditions = db.Column(
        db.String
    )

    def get_meta(self):
        info = {
            'table': {
                'sensitive': False,
                'label': 'Clinical Diagnoses',
                'description': '',
            }
        }
        for c in self.metadata.tables['clinical_diagnoses_questionnaire'].columns:
            if c.info:
                info[c.name] = c.info
        return info


class ClinicalDiagnosesQuestionnaireSchema(ModelSchema):
    class Meta:
        model = ClinicalDiagnosesQuestionnaire
        fields = ('id', 'last_updated', 'participant_id', 'user_id', 'developmental', 'mental_health', 'medical',
                  'genetic_conditions')


class ClinicalDiagnosesQuestionnaireMetaSchema(ModelSchema):
    class Meta:
        model = ClinicalDiagnosesQuestionnaire
        fields = ('get_meta',)

