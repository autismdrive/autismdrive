import datetime

from marshmallow_sqlalchemy import ModelSchema

from app import db


class DevelopmentalQuestionnaire(db.Model):
    __tablename__ = 'developmental_questionnaire'
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
    had_birth_complications = db.Column(
        db.Boolean
    )
    when_motor_milestones = db.Column(
        db.String
    )
    when_language_milestones = db.Column(
        db.String
    )
    when_toileting_milestones = db.Column(
        db.String
    )

    def get_meta(self):
        info = {
            'table': {
                'sensitive': False,
                'label': 'Birth and Developmental History',
                'description': '',
            }
        }
        for c in self.metadata.tables['developmental_questionnaire'].columns:
            if c.info:
                info[c.name] = c.info
        return info


class DevelopmentalQuestionnaireSchema(ModelSchema):
    class Meta:
        model = DevelopmentalQuestionnaire
        fields = ('id', 'last_updated', 'participant_id', 'user_id', 'had_birth_complications', 'when_motor_milestones',
                  'when_language_milestones', 'when_toileting_milestones')


class DevelopmentalQuestionnaireMetaSchema(ModelSchema):
    class Meta:
        model = DevelopmentalQuestionnaire
        fields = ('get_meta',)

