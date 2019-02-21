import datetime

from marshmallow_sqlalchemy import ModelSchema

from app import db
from app.question_service import QuestionService
from app.model.questionnaires.housemate import Housemate


class HomeSelfQuestionnaire(db.Model):
    __tablename__ = "home_self_questionnaire"
    __question_type__ = QuestionService.TYPE_IDENTIFYING
    __estimated_duration_minutes__ = 5

    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime, default=datetime.datetime.now)
    time_on_task_ms = db.Column(db.BigInteger, default=0)

    participant_id = db.Column(
        "participant_id", db.Integer, db.ForeignKey("stardrive_participant.id")
    )
    user_id = db.Column("user_id", db.Integer, db.ForeignKey("stardrive_user.id"))
    self_living_situation = db.Column(
        db.String,
        info={
            "display_order": 1.1,
            "type": "multicheckbox",
            "class_name": "vertical-checkbox-group",
            "template_options": {
                "required": True,
                "label": "Where do you currently live? (select all that apply)",
                "options": [
                    {"value": "alone", "label": "On my own"},
                    {"value": "spouse", "label": "With a spouse or significant other"},
                    {"value": "family", "label": "With my family"},
                    {"value": "roommates", "label": "With roommates"},
                    {"value": "caregiver", "label": "With a paid caregiver"},
                    {"value": "livingOther", "label": "self_living_situation"},
                ],
            },
        },
    )
    self_living_other = db.Column(
        db.String,
        info={
            "display_order": 1.2,
            "type": "input",
            "template_options": {
                "placeholder": "Describe your current living situation"
            },
            "hide_expression": '!(model.self_living_situation && (model.self_living_situation === "livingOther"))',
        },
    )
    housemates = db.relationship(
        "Housemate",
        backref=db.backref("home_self_questionnaire", lazy=True),
        info={
            "display_order": 3,
            "type": "repeat",
            "template_options": {"required": False, "label": "Who else lives with you?"},
        },
    )
    struggle_to_afford = db.Column(
        db.Boolean,
        info={
            "display_order": 4,
            "type": "radio",
            "default_value": False,
            "template_options": {
                "required": False,
                "label": "Do you ever struggle with being able to afford to pay for household needs, food, or security?",
                "options": [
                    {"value": True, "label": "Yes"},
                    {"value": False, "label": "No"},
                ],
            },
        },
    )

    def get_meta(self):
        info = {
            "table": {"sensitive": False, "label": "Home"},
            "first_name": {
                "type": "input",
                "default_value": "FIRST_NAME",
                "hide_expression": True,
            },
            "nickname": {
                "type": "input",
                "default_value": "NICKNAME",
                "hide_expression": True,
            },
            "last_name": {
                "type": "input",
                "default_value": "LAST_NAME",
                "hide_expression": True,
            },
            "is_self": {
                "type": "input",
                "default_value": True,
                "hide_expression": True,
            },
            "field_groups": {
                "self_living": {
                    "fields": ["self_living_situation", "self_living_other"],
                    "display_order": 1,
                    "wrappers": ["card"],
                    "template_options": {"label": "Current Living Situation"},
                    "hide_expression": "!formState.mainModel.is_self",
                },
                "housemates": {
                    "type": "repeat",
                    "display_order": 3,
                    "wrappers": ["card"],
                    "template_options": {
                        "label": "Who else lives there?",
                        "description": "Add a housemate",
                    },
                    "expression_properties": {
                        "template_options.label": "Who else lives with you?"
                    },
                },
            },
        }
        for c in self.metadata.tables["home_self_questionnaire"].columns:
            if c.info:
                info[c.name] = c.info

        info["housemates"] = Housemate().get_meta()

        return info


class HomeSelfQuestionnaireSchema(ModelSchema):
    class Meta:
        model = HomeSelfQuestionnaire
        fields = (
            "id",
            "last_updated",
            "participant_id",
            "user_id",
            "self_living_situation",
            "self_living_other",
            "housemates",
            "struggle_to_afford",
        )


class HomeSelfQuestionnaireMetaSchema(ModelSchema):
    class Meta:
        model = HomeSelfQuestionnaire
        fields = ("get_meta",)