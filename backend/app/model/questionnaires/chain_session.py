from marshmallow import fields, missing, pre_load
from sqlalchemy import func
from sqlalchemy.ext.declarative import declared_attr

from app import db, ma
from app.export_service import ExportService
from app.schema.model_schema import ModelSchema
from app.model.questionnaires.chain_session_step import ChainSessionStepSchema


class ChainSession(db.Model):
    """
    SkillStar: Chain Session
    """
    __tablename__ = "chain_session"
    __label__ = "SkillSTAR Chain Session"
    __question_type__ = ExportService.TYPE_UNRESTRICTED
    __estimated_duration_minutes__ = 5

    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime(timezone=True), default=func.now())
    time_on_task_ms = db.Column(db.BigInteger, default=0)


    @declared_attr
    def date(cls):
        return db.Column(
            db.DateTime,
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

    tasks = [
        {"id": "task_01", "label": "Put toothpaste on your toothbrush"},
        {"id": "task_02", "label": "Put toothpaste away"},
        {"id": "task_03", "label": "Rinse toothbrush"},
        {"id": "task_04", "label": "Brush top surface of bottom teeth on right side."},
        {"id": "task_05", "label": "Brush top surface of bottom teeth on left side."},
        {"id": "task_06", "label": "Brush top surface of top teeth on right side"},
        {"id": "task_07", "label": "Brush top surface of top teeth on left side"},
        {"id": "task_08", "label": "Brush outside surface (facing cheek) of bottom teeth on right side"},
        {"id": "task_09", "label": "Brush outside surface (facing lips) of bottom teeth at the front of your mouth"},
        {"id": "task_10", "label": "Brush outside surface (facing cheek) of bottom teeth on left side"},
        {"id": "task_11", "label": "Brush outside surface (facing cheek) of top teeth on right side"},
        {"id": "task_12", "label": "Brush outside surface (facing lips) of top teeth at the front of your mouth"},
        {"id": "task_13", "label": "Brush outside surface (facing cheek) of top teeth on left side"},
        {"id": "task_14", "label": "Brush the inside surface (facing tongue) of bottom teeth on right side."},
        {"id": "task_15", "label": "Brush the inside surface (facing tongue) of bottom teeth on left side"},
        {"id": "task_16", "label": "Brush the inside surface (facing tongue) of top teeth on left side."},
        {"id": "task_17", "label": "Brush the inside surface (facing tongue) of top teeth on right side."},
        {"id": "task_18", "label": "Spit in the sink"},
        {"id": "task_19", "label": "Rinse toothbrush and put it away"},
        {"id": "task_20", "label": "Get your cup and fill with water"},
        {"id": "task_21", "label": "Rinse mouth and spit in sink"},
        {"id": "task_22", "label": "Wipe your face with a towel"},
        {"id": "task_23", "label": "Clean up"},
    ]

    participant_id = db.Column(
        "participant_id", db.Integer, db.ForeignKey("stardrive_participant.id")
    )
    user_id = db.Column(
        "user_id", db.Integer, db.ForeignKey("stardrive_user.id")
    )


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
            "complete",
            "step_attempts",
        )

    step_attempts = ma.Nested(ChainSessionStepSchema, many=True)

    participant_id = fields.Method('get_participant_id')
    user_id = fields.Method('get_user_id')
    skillstar_chain_questionnaire_id = fields.Integer(required=False, allow_none=True)
    skillstar_chain_questionnaire = fields.Nested('SkillstarChainQuestionnaire', required=False, allow_none=True)

    def get_participant_id(self, obj):
        if obj is None:
            return missing
        elif obj.home_dependent_questionnaire is not None:
            return obj.home_dependent_questionnaire.participant_id
        elif obj.home_self_questionnaire is not None:
            return obj.home_self_questionnaire.participant_id

    def get_user_id(self, obj):
        if obj is None:
            return missing
        elif obj.home_dependent_questionnaire is not None:
            return obj.home_dependent_questionnaire.user_id
        elif obj.home_self_questionnaire is not None:
            return obj.home_self_questionnaire.user_id
