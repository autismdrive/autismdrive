import datetime

from marshmallow_sqlalchemy import ModelSchema

from app import db


class CurrentBehaviorsQuestionnaire(db.Model):
    __tablename__ = 'current_behaviors_questionnaire'
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
    verbal_ability = db.Column(
        db.String
    )
    concerning_behaviors = db.Column(
        db.String
    )
    has_academic_difficulties = db.Column(
        db.Boolean
    )
    academic_difficulty_areas = db.Column(
        db.String
    )
    academic_difficulty_other = db.Column(
        db.String
    )

    def get_meta(self):
        info = {
            'table': {
                'sensitive': False,
                'label': 'Current Behaviors',
                'description': '',
            }
        }
        for c in self.metadata.tables['current_behaviors_questionnaire'].columns:
            if c.info:
                info[c.name] = c.info
        return info


class CurrentBehaviorsQuestionnaireSchema(ModelSchema):
    class Meta:
        model = CurrentBehaviorsQuestionnaire
        fields = ('id', 'last_updated', 'participant_id', 'user_id', 'verbal_ability', 'concerning_behaviors',
                  'has_academic_difficulties', 'academic_difficulty_areas', 'academic_difficulty_other')


class CurrentBehaviorsQuestionnaireMetaSchema(ModelSchema):
    class Meta:
        model = CurrentBehaviorsQuestionnaire
        fields = ('get_meta',)

