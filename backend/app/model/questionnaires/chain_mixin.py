import datetime

from sqlalchemy import func
from sqlalchemy.ext.declarative import declared_attr

from app import db
from app.model.questionnaires.chain_session import ChainSession
from app.export_service import ExportService


class ChainMixin(object):
    __question_type__ = ExportService.TYPE_UNRESTRICTED
    __estimated_duration_minutes__ = 5

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
    def sessions(cls):
        return db.relationship(
            "ChainSession",
            backref=db.backref(cls.__tablename__, lazy=True),
            cascade="all, delete-orphan",
            passive_deletes=True
        )

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
    def complete(cls):
        return db.Column(
            db.Boolean,
            info={
                "display_order": 2,
                "type": "radio",
                "template_options": {
                    "required": False,
                    "label": 'Session Complete?',
                    "options": [
                        {"value": True, "label": "Yes"},
                        {"value": False, "label": "No"},
                    ],
                },
            },
        )

    def get_field_groups(self):
        field_groups = {
                "sessions": {
                    "type": "repeat",
                    "display_order": 3,
                    "wrappers": ["card"],
                    "repeat_class": ChainSession,
                    "template_options": {
                        "label": "Chain Session",
                        "description": "Add a session",
                    },
                    "expression_properties": {},
                },
            }
        return field_groups
