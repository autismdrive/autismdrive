from marshmallow import fields, missing, pre_load
from sqlalchemy import func
from sqlalchemy.ext.declarative import declared_attr

from app import db, ma
from app.export_service import ExportService
from app.schema.model_schema import ModelSchema
from app.model.questionnaires.chain_session_step import ChainSessionStepSchema, ChainSessionStep


class ChainSession(db.Model):
    """
    SkillStar: Chain Session
    """
    __tablename__ = "chain_session"
    __label__ = "SkillSTAR Chain Session"
    __no_export__ = True  # This will be transferred as a part of a parent class
    __question_type__ = ExportService.TYPE_UNRESTRICTED
    __estimated_duration_minutes__ = 5

    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime(timezone=True), default=func.now())
    time_on_task_ms = db.Column(db.BigInteger, default=0)

    chain_questionnaire_id = db.Column(
        "chain_questionnaire_id",
        db.Integer,
        db.ForeignKey('chain_questionnaire.id')
    )

    @declared_attr
    def date(cls):
        return db.Column(
            db.DateTime(timezone=True),
            info={
                "display_order": 1,
                "type": "datepicker",
                "template_options": {
                    "required": True,
                    "label": 'Session Date',
                },
            },
        )

    @declared_attr
    def completed(cls):
        return db.Column(
            db.Boolean,
            info={
                "display_order": 2,
                "type": "radio",
                "template_options": {
                    "required": True,
                    "label": 'Session Complete?',
                    "options": [
                        {"value": True, "label": "Yes"},
                        {"value": False, "label": "No"},
                    ],
                },
            },
        )

    @declared_attr
    def session_type(cls):
        return db.Column(
            db.String,
            info={
                "display_order": 2,
                "type": "radio",
                "template_options": {
                    "required": True,
                    "label": 'Session Type',
                    "options": [
                        {"value": 'training', "label": "Training"},
                        {"value": 'probe', "label": "Probe"},
                        {"value": 'booster', "label": "Booster"},
                    ],
                },
            },
        )

    @declared_attr
    def step_attempts(cls):
        return db.relationship(
            "ChainSessionStep",
            backref=db.backref(cls.__tablename__, lazy=True),
            cascade="all, delete-orphan",
            passive_deletes=True
        )

    def get_field_groups(self):
        field_groups = {
            "step_attempts": {
                "type": "repeat",
                "display_order": 3,
                "wrappers": ["card"],
                "repeat_class": ChainSessionStep,
                "template_options": {
                    "label": "Which tasks were attempted?",
                    "description": "Add a step",
                },
                "expression_properties": {},
            },
        }
        return field_groups

class ChainSessionSchema(ModelSchema):
    @pre_load
    def set_field_session(self, data, **kwargs):
        self.fields['step_attempts'].schema.session = self.session
        return data

    class Meta(ModelSchema.Meta):
        model = ChainSession
        fields = (
            "id",
            "last_updated",
            "participant_id",
            "user_id",
            "time_on_task_ms",
            "date",
            "completed",
            "session_type",
            "step_attempts",
            "chain_questionnaire_id"
        )

    step_attempts = ma.Nested(ChainSessionStepSchema, many=True)
    participant_id = fields.Method('get_participant_id', dump_only=True)
    user_id = fields.Method('get_user_id', dump_only=True)

    def get_participant_id(self, obj):
        print('get_participant_id', obj)
        return obj.chain_questionnaire.participant_id

    def get_user_id(self, obj):
        print('get_user_id', obj)
        return obj.chain_questionnaire.user_id
