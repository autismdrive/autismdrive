import datetime

from marshmallow_sqlalchemy import ModelSchema

from app import db
from app.question_service import QuestionService
from app.model.questionnaires.housemate import Housemate


class HomeDependentQuestionnaire(db.Model):
    __tablename__ = "home_dependent_questionnaire"
    __question_type__ = QuestionService.TYPE_IDENTIFYING
    __estimated_duration_minutes__ = 5

    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime, default=datetime.datetime.now)
    time_on_task_ms = db.Column(db.BigInteger, default=0)

    participant_id = db.Column(
        "participant_id", db.Integer, db.ForeignKey("stardrive_participant.id")
    )
    user_id = db.Column("user_id", db.Integer, db.ForeignKey("stardrive_user.id"))
    dependent_living_situation = db.Column(
        db.String,
        info={
            "display_order": 2.1,
            "type": "multicheckbox",
            "class_name": "vertical-checkbox-group",
            "template_options": {
                "required": True,
                "label": "",
                "options": [
                    {"value": "fullTimeGuardian", "label": "With me full-time"},
                    {"value": "partTimeGuardian", "label": "With me part time"},
                    {
                        "value": "otherFamily",
                        "label": "With other parent/guardian/family member ",
                    },
                    {"value": "residentialFacility", "label": "Residential facility"},
                    {"value": "groupHome", "label": "Group home"},
                    {"value": "livingOther", "label": "Other (please explain)"},
                ],
            },
        },
    )
    dependent_living_other = db.Column(
        db.String,
        info={
            "display_order": 2.2,
            "type": "input",
            "template_options": {"placeholder": ""},
            "hide_expression": "!(model.dependent_living_situation && model.dependent_living_situation.livingOther)",
            "expression_properties": {
                "template_options.placeholder": '"Please describe "+ (formState.mainModel.preferred_name) + "\'s current living situation"'
            },
        },
    )
    housemates = db.relationship(
        "Housemate",
        backref=db.backref("home_dependent_questionnaire", lazy=True),
        info={
            "display_order": 3,
            "type": "repeat",
            "template_options": {
                "required": False,
                "label": '"Who else lives with " + (formState.mainModel.preferred_name) + "?"'
            },
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
                "label": '"Do you or " + formState.mainModel.preferred_name + "\'s other caregivers ever struggle with'
                         ' being able to afford to pay for household needs, food, or security for the family?"',
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
                "dependent_living": {
                    "fields": ["dependent_living_situation", "dependent_living_other"],
                    "display_order": 2,
                    "wrappers": ["card"],
                    "template_options": {"label": "Current Living Situation"},
                    "hide_expression": "formState.mainModel.is_self",
                    "expression_properties": {
                        "template_options.label": '"Where does " + formState.mainModel.preferred_name + " currently live (select all that apply)?"'
                    },
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
                        "template_options.label": '"Who else lives with " + formState.mainModel.preferred_name + "?"'
                    },
                },
            },
        }
        for c in self.metadata.tables["home_dependent_questionnaire"].columns:
            if c.info:
                info[c.name] = c.info

        info["housemates"] = Housemate().get_meta()

        return info


class HomeDependentQuestionnaireSchema(ModelSchema):
    class Meta:
        model = HomeDependentQuestionnaire
        fields = (
            "id",
            "last_updated",
            "participant_id",
            "user_id",
            "dependent_living_situation",
            "dependent_living_other",
            "housemates",
            "struggle_to_afford",
        )


class HomeDependentQuestionnaireMetaSchema(ModelSchema):
    class Meta:
        model = HomeDependentQuestionnaire
        fields = ("get_meta",)
