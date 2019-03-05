from marshmallow import fields, pre_load
from marshmallow_sqlalchemy import ModelSchema

from app import db
from app.model.questionnaires.housemate import Housemate, HousemateSchema
from app.model.questionnaires.home_mixin import HomeMixin


class HomeSelfQuestionnaire(db.Model, HomeMixin):
    __tablename__ = "home_self_questionnaire"
    __label__ = "Home"

    struggle_to_afford_label = "Do you ever struggle with being able to afford to pay for household needs, food, or security?"

    self_living_situation = db.Column(
        db.ARRAY(db.String),
        info={
            "display_order": 1.1,
            "type": "multicheckbox",
            "class_name": "vertical-checkbox-group",
            "template_options": {
                "type": "array",
                "required": True,
                "label": "Where do you currently live? (select all that apply)",
                "options": [
                    {"value": "alone", "label": "On my own"},
                    {"value": "spouse", "label": "With a spouse or significant other"},
                    {"value": "family", "label": "With my family"},
                    {"value": "roommates", "label": "With roommates"},
                    {"value": "caregiver", "label": "With a paid caregiver"},
                    {"value": "livingOther", "label": "Other"},
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
            "hide_expression": '!(model.self_living_situation && model.self_living_situation.includes("livingOther"))',
        },
    )

    def get_field_groups(self):
        field_groups = super().get_field_groups()
        field_groups["housemates"]["template_options"]["label"] = "Who else lives with you?"
        field_groups["self_living"] = {
                    "fields": ["self_living_situation", "self_living_other"],
                    "display_order": 1,
                    "wrappers": ["card"],
                    "template_options": {"label": "Current Living Situation"},
                }
        return field_groups


class HomeSelfQuestionnaireSchema(ModelSchema):
    @pre_load
    def set_field_session(self, data):
        self.fields['housemates'].schema.session = self.session

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
    housemates = fields.Nested(HousemateSchema, many=True)
