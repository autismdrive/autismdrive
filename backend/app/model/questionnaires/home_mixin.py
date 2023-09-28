from sqlalchemy import func, Column, Integer, ForeignKey, DateTime, Boolean, BigInteger
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship, backref

from app.export_service import ExportService
from app.model.questionnaires.housemate import Housemate


class HomeMixin(object):
    __question_type__ = ExportService.TYPE_UNRESTRICTED
    __estimated_duration_minutes__ = 5

    id = Column(Integer, primary_key=True)
    last_updated = Column(DateTime(timezone=True), default=func.now())
    time_on_task_ms = Column(BigInteger, default=0)

    @declared_attr
    def participant_id(cls):
        return Column("participant_id", Integer, ForeignKey("stardrive_participant.id"))

    @declared_attr
    def user_id(cls):
        return Column("user_id", Integer, ForeignKey("stardrive_user.id"))

    @declared_attr
    def housemates(cls):
        return relationship(
            "Housemate",
            backref=backref(cls.__tablename__, lazy=True),
            cascade="all, delete-orphan",
            passive_deletes=True,
        )

    @declared_attr
    def struggle_to_afford(cls):
        return Column(
            Boolean,
            info={
                "display_order": 4,
                "type": "radio",
                "template_options": {
                    "required": False,
                    "label": "Financial Struggles",
                    "options": [
                        {"value": True, "label": "Yes"},
                        {"value": False, "label": "No"},
                    ],
                },
                "expression_properties": {"template_options.description": cls.struggle_to_afford_desc},
            },
        )

    def get_field_groups(self):
        field_groups = {
            "housemates": {
                "type": "repeat",
                "display_order": 3,
                "wrappers": ["card"],
                "repeat_class": Housemate,
                "template_options": {
                    "label": "Who else lives there?",
                    "description": "Add a housemate",
                },
                "expression_properties": {},
            },
        }
        return field_groups
