from sqlalchemy import func
from sqlalchemy.ext.declarative import declared_attr

from app import db
from app.export_service import ExportService
from app.model.questionnaires.chain_session_step import ChainSessionStep


class ChainSessionStepMixin(object):
    """
    SkillStar: Chain Session Step
    """
    info = {}
    __question_type__ = ExportService.TYPE_UNRESTRICTED
    __label__ = "Chain Session Step"
    __estimated_duration_minutes__ = 1

    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime(timezone=True), default=func.now())
    time_on_task_ms = db.Column(db.BigInteger, default=0)

    is_task_complete = db.Column(
        db.Boolean,
        info={
            "display_order": 1.1,
            "type": "radio",
            "template_options": {
                "type": "array",
                "label": "Task Complete?",
                "required": True,
                "options": [
                    {"value": True, "label": "Yes"},
                    {"value": False, "label": "No"},
                ],
            },
        },
    )

    has_challenging_behavior = db.Column(
        db.Boolean,
        info={
            "display_order": 1.2,
            "type": "radio",
            "template_options": {
                "type": "array",
                "label": "Challenging Behavior?",
                "required": True,
                "options": [
                    {"value": True, "label": "Yes"},
                    {"value": False, "label": "No"},
                ],
            },
        },
    )

    @declared_attr
    def participant_id(cls):
        return db.Column("participant_id", db.Integer, db.ForeignKey("stardrive_participant.id"))

    @declared_attr
    def user_id(cls):
        return db.Column("user_id", db.Integer, db.ForeignKey("stardrive_user.id"))

    @declared_attr
    def focus_steps(cls):
        return db.relationship(
            "ChainSessionStep",
            backref=db.backref(cls.__tablename__, lazy=True),
            cascade="all, delete-orphan",
            passive_deletes=True
        )

    def get_field_groups(self):
        field_groups = {
            "focus_steps": {
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
