from sqlalchemy import func
from sqlalchemy.ext.declarative import declared_attr

from app import db
from app.export_service import ExportService


class TaskAssessmentMixin(object):
    """
    SkillStar: Task Assessment
    """
    info = {}
    __question_type__ = ExportService.TYPE_UNRESTRICTED
    __label__ = "Task Assessment"
    __estimated_duration_minutes__ = 1

    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime(timezone=True), default=func.now())
    time_on_task_ms = db.Column(db.BigInteger, default=0)

    @declared_attr
    def participant_id(cls):
        return db.Column("participant_id", db.Integer, db.ForeignKey("stardrive_participant.id"))

    @declared_attr
    def user_id(cls):
        return db.Column("user_id", db.Integer, db.ForeignKey("stardrive_user.id"))

    @declared_attr
    def is_task_complete(cls):
        return db.Column(
            db.ARRAY(db.String),
            info={
                "display_order": 1.1,
                "type": "multicheckbox",
                "template_options": {
                    "type": "array",
                    "label": "Task Complete?",
                    "required": True,
                    "description": "(select all that apply)",
                    "options": [
                        {"value": "task_00_complete", "label": ""},
                        {"value": "task_01_complete", "label": ""},
                        {"value": "task_02_complete", "label": ""},
                        {"value": "task_03_complete", "label": ""},
                        {"value": "task_04_complete", "label": ""},
                        {"value": "task_05_complete", "label": ""},
                        {"value": "task_06_complete", "label": ""},
                        {"value": "task_07_complete", "label": ""},
                        {"value": "task_08_complete", "label": ""},
                        {"value": "task_09_complete", "label": ""},
                        {"value": "task_10_complete", "label": ""},
                        {"value": "task_11_complete", "label": ""},
                        {"value": "task_12_complete", "label": ""},
                        {"value": "task_13_complete", "label": ""},
                        {"value": "task_14_complete", "label": ""},
                        {"value": "task_15_complete", "label": ""},
                        {"value": "task_16_complete", "label": ""},
                        {"value": "task_17_complete", "label": ""},
                        {"value": "task_18_complete", "label": ""},
                        {"value": "task_19_complete", "label": ""},
                        {"value": "task_20_complete", "label": ""},
                        {"value": "task_21_complete", "label": ""},
                        {"value": "task_22_complete", "label": ""},
                        {"value": "task_23_complete", "label": ""},
                        {"value": "task_24_complete", "label": ""},
                        {"value": "task_25_complete", "label": ""},
                    ],
                    "validators": {"required": "multicheckbox"},
                },
            },
        )

    @declared_attr
    def has_challenging_behavior(cls):
        return db.Column(
            db.ARRAY(db.String),
            info={
                "display_order": 1.1,
                "type": "multicheckbox",
                "template_options": {
                    "type": "array",
                    "label": "Challenging Behavior?",
                    "required": True,
                    "description": "(select all that apply)",
                    "options": [
                        {"value": "task_00_challenge", "label": ""},
                        {"value": "task_01_challenge", "label": ""},
                        {"value": "task_02_challenge", "label": ""},
                        {"value": "task_03_challenge", "label": ""},
                        {"value": "task_04_challenge", "label": ""},
                        {"value": "task_05_challenge", "label": ""},
                        {"value": "task_06_challenge", "label": ""},
                        {"value": "task_07_challenge", "label": ""},
                        {"value": "task_08_challenge", "label": ""},
                        {"value": "task_09_challenge", "label": ""},
                        {"value": "task_10_challenge", "label": ""},
                        {"value": "task_11_challenge", "label": ""},
                        {"value": "task_12_challenge", "label": ""},
                        {"value": "task_13_challenge", "label": ""},
                        {"value": "task_14_challenge", "label": ""},
                        {"value": "task_15_challenge", "label": ""},
                        {"value": "task_16_challenge", "label": ""},
                        {"value": "task_17_challenge", "label": ""},
                        {"value": "task_18_challenge", "label": ""},
                        {"value": "task_19_challenge", "label": ""},
                        {"value": "task_20_challenge", "label": ""},
                        {"value": "task_21_challenge", "label": ""},
                        {"value": "task_22_challenge", "label": ""},
                        {"value": "task_23_challenge", "label": ""},
                        {"value": "task_24_challenge", "label": ""},
                        {"value": "task_25_challenge", "label": ""},
                    ],
                    "validators": {"required": "multicheckbox"},
                },
            },
        )

    def get_field_groups(self):
        return {}
