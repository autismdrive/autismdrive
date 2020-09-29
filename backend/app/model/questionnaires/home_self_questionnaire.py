from marshmallow import fields, pre_load, EXCLUDE
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app import db
from app.model.questionnaires.housemate import HousemateSchema
from app.model.questionnaires.home_mixin import HomeMixin


class HomeSelfQuestionnaire(db.Model, HomeMixin):
    __tablename__ = "home_self_questionnaire"
    __label__ = "Home"
    self_living_other_hide_expression = '!(model.self_living_situation && model.self_living_situation.includes("livingOther"))'

    struggle_to_afford_desc = '"Do you ever struggle with being able to afford to pay for household needs, food, or security?"'

    self_living_situation = db.Column(
        db.ARRAY(db.String),
        info={
            "display_order": 1.1,
            "type": "multicheckbox",
            "template_options": {
                "type": "array",
                "label": "Current Living Situation",
                "required": True,
                "description": "(select all that apply)",
                "options": [
                    {"value": "alone", "label": "On my own"},
                    {"value": "spouse", "label": "With a spouse or significant other"},
                    {"value": "family", "label": "With my family"},
                    {"value": "roommates", "label": "With roommates"},
                    {"value": "caregiver", "label": "With a paid caregiver"},
                    {"value": "livingOther", "label": "Other"},
                ],
                "validators": {"required": "multicheckbox"},
            },
        },
    )
    self_living_other = db.Column(
        db.String,
        info={
            "display_order": 1.2,
            "type": "input",
            "template_options": {
                "label": "Describe your current living situation",
                "required": True,
            },
            "hide_expression": self_living_other_hide_expression,
            "expression_properties": {
                "template_options.required": '!' + self_living_other_hide_expression
            }
        },
    )

    def get_field_groups(self):
        field_groups = super().get_field_groups()
        field_groups["housemates"]["template_options"]["label"] = "Who else lives with you?"
        field_groups["self_living"] = {
                    "fields": ["self_living_situation", "self_living_other"],
                    "display_order": 1,
                    "wrappers": ["card"],
                    "template_options": {"label": "Where do you currently live?"},
                }
        return field_groups


class HomeSelfQuestionnaireSchema(SQLAlchemyAutoSchema):
    @pre_load
    def set_field_session(self, data, **kwargs):
        self.fields['housemates'].schema.session = self.session
        return data

    class Meta:
        model = HomeSelfQuestionnaire
        include_relationships = True
        load_instance = True
        unknown = EXCLUDE
        fields = (
            "id",
            "last_updated",
            "participant_id",
            "user_id",
            "time_on_task_ms",
            "self_living_situation",
            "self_living_other",
            "housemates",
            "struggle_to_afford",
        )
        ordered = True
    housemates = fields.Nested(HousemateSchema, many=True)
