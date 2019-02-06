import datetime

from marshmallow_sqlalchemy import ModelSchema

from app import db
from app.question_service import QuestionService
from app.model.questionnaires.therapy import Therapy
from app.model.questionnaires.medication import Medication
from app.model.questionnaires.assistive_device import AssistiveDevice


class SupportsQuestionnaire(db.Model):
    __tablename__ = "supports_questionnaire"
    __question_type__ = QuestionService.TYPE_UNRESTRICTED
    __estimated_duration_minutes__ = 5

    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime, default=datetime.datetime.now)
    participant_id = db.Column(
        "participant_id", db.Integer, db.ForeignKey("stardrive_participant.id")
    )
    user_id = db.Column(
        "user_id", db.Integer, db.ForeignKey("stardrive_user.id")
    )
    medications = db.relationship(
        "Medication", backref=db.backref("supports_questionnaire", lazy=True)
    )
    therapies = db.relationship(
        "Therapy", backref=db.backref("supports_questionnaire", lazy=True)
    )
    assistive_devices = db.relationship(
        "AssistiveDevice",
        backref=db.backref("supports_questionnaire", lazy=True),
    )

    def get_meta(self):
        info = {
            "table": {"sensitive": False, "label": "Supports"},
            "field_groups": {
                "medications": {
                    "type": "repeat",
                    "display_order": 1,
                    "wrappers": ["card"],
                    "template_options": {
                        "label": "Medications and/or vitamins",
                        "description": "Add a medication",
                    },
                    "expression_properties": {
                        "template_options.label": '(formState.mainModel.is_self ? "Do you" : "Does your child") + " take any medications and/or vitamins?"'
                    },
                },
                "therapies": {
                    "type": "repeat",
                    "display_order": 2,
                    "wrappers": ["card"],
                    "template_options": {
                        "label": "Therapies and services",
                        "description": "Add a therapy or service",
                    },
                    "expression_properties": {
                        "template_options.label": '"What kinds of therapies and services " + (formState.mainModel.is_self ? "do you" : "does your child") + " currently receive?"'
                    },
                },
                "assistive_devices": {
                    "type": "repeat",
                    "display_order": 3,
                    "wrappers": ["card"],
                    "template_options": {
                        "label": "Assistive devices",
                        "description": "Add an assistive device",
                    },
                    "expression_properties": {
                        "template_options.label": '(formState.mainModel.is_self ? "Do you" : "Does your child") + " use an AAC (alternative & augmentative communication) system or other assistive device?"'
                    },
                },
            },
        }

        info["medications"] = Medication().get_meta()
        info["therapies"] = Therapy().get_meta()
        info["assistive_devices"] = AssistiveDevice().get_meta()

        return info


class SupportsQuestionnaireSchema(ModelSchema):
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


class SupportsQuestionnaireMetaSchema(ModelSchema):
    class Meta:
        model = SupportsQuestionnaire
        fields = ("get_meta",)
