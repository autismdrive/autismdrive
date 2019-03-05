import datetime

from marshmallow import fields, pre_load
from marshmallow_sqlalchemy import ModelSchema

from app import db
from app.question_service import QuestionService
from app.model.questionnaires.therapy import Therapy, TherapySchema
from app.model.questionnaires.medication import Medication, MedicationSchema
from app.model.questionnaires.assistive_device import AssistiveDevice, AssistiveDeviceSchema


class SupportsQuestionnaire(db.Model):
    __tablename__ = "supports_questionnaire"
    __label__ = "Supports"
    __question_type__ = QuestionService.TYPE_UNRESTRICTED
    __estimated_duration_minutes__ = 5

    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime, default=datetime.datetime.now)
    time_on_task_ms = db.Column(db.BigInteger, default=0)

    participant_id = db.Column(
        "participant_id", db.Integer, db.ForeignKey("stardrive_participant.id")
    )
    user_id = db.Column(
        "user_id", db.Integer, db.ForeignKey("stardrive_user.id")
    )
    medications = db.relationship(
        "Medication",
        backref=db.backref("supports_questionnaire", lazy=True),
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    therapies = db.relationship(
        "Therapy",
        backref=db.backref("supports_questionnaire", lazy=True),
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    assistive_devices = db.relationship(
        "AssistiveDevice",
        backref=db.backref("supports_questionnaire", lazy=True),
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    def get_field_groups(self):
        return {
            "medications": {
                "type": "repeat",
                "display_order": 1,
                "wrappers": ["card"],
                "repeat_class": Medication,
                "template_options": {
                    "label": {
                        "RELATIONSHIP_SPECIFIC": {
                            "self_participant": "Do you take any medications and/or vitamins?",
                            "self_guardian": "Do you take any medications and/or vitamins?",
                            "dependent": "Does your child take any medications and/or vitamins?",
                        }
                    },
                    "description": "Add a medication",
                },
            },
            "therapies": {
                "type": "repeat",
                "display_order": 2,
                "wrappers": ["card"],
                "repeat_class": Therapy,
                "template_options": {
                    "label": {
                        "RELATIONSHIP_SPECIFIC": {
                            "self_participant": "What kinds of therapies and services do you currently receive?",
                            "self_guardian": "What kinds of therapies and services do you currently receive?",
                            "dependent": "What kinds of therapies and services does your child currently receive?",
                        }
                    },
                    "description": "Add a therapy or service",
                },
            },
            "assistive_devices": {
                "type": "repeat",
                "display_order": 3,
                "wrappers": ["card"],
                "repeat_class": AssistiveDevice,
                "template_options": {
                    "label": {
                        "RELATIONSHIP_SPECIFIC": {
                            "self_participant": "Do you use an AAC (alternative & augmentative communication) "
                                                "system or other assistive device?",
                            "self_guardian": "Do you use an AAC (alternative & augmentative communication) "
                                             "system or other assistive device?",
                            "dependent": "Does your child use an AAC (alternative & augmentative communication) "
                                         "system or other assistive device?",
                        }
                    },
                    "description": "Add an assistive device",
                },
            }
        }


class SupportsQuestionnaireSchema(ModelSchema):
    @pre_load
    def set_field_session(self, data):
        self.fields['medications'].schema.session = self.session
        self.fields['therapies'].schema.session = self.session
        self.fields['assistive_devices'].schema.session = self.session

    class Meta:
        model = SupportsQuestionnaire
        fields = (
            "id",
            "last_updated",
            "participant_id",
            "user_id",
            "medications",
            "therapies",
            "assistive_devices",
        )
    medications = fields.Nested(MedicationSchema, many=True)
    therapies = fields.Nested(TherapySchema, many=True)
    assistive_devices = fields.Nested(AssistiveDeviceSchema, many=True)
