from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema

from app import db
from app.model.questionnaires.housemate import Housemate, HousemateSchema
from app.model.questionnaires.home_mixin import HomeMixin


class HomeDependentQuestionnaire(db.Model, HomeMixin):
    __tablename__ = "home_dependent_questionnaire"
    __label__ = "Home"

    dependent_living_situation = db.Column(
        db.ARRAY(db.String),
        info={
            "display_order": 2.1,
            "type": "multicheckbox",
            "class_name": "vertical-checkbox-group",
            "template_options": {
                "type": "array",
                "required": True,
                "label": "",
                "options": [
                    {"value": "fullTimeGuardian", "label": "With me full-time"},
                    {"value": "partTimeGuardian", "label": "With me part time"},
                    {"value": "otherFamily", "label": "With other parent/guardian/family member "},
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
                "template_options.placeholder": '"Please describe "+ (model.preferred_name) + "\'s current living situation"'
            },
        },
    )

    def get_field_groups(self):
        field_groups = super().get_field_groups()
        field_groups["dependent_living"] = {
                    "fields": ["dependent_living_situation", "dependent_living_other"],
                    "display_order": 2,
                    "wrappers": ["card"],
                    "template_options": {"label": "Current Living Situation"},
                    "expression_properties": {
                        "template_options.label": '"Where does " + model.preferred_name + " currently '
                                                  'live (select all that apply)?"'
                    },
                }

        field_groups["housemates"]["expression_properties"]["template_options.label"] = \
            '"Who else lives with " + model.preferred_name + "?"'
        field_groups["housemates"]["template_options"]["label"] = ''
        return field_groups

    def update_meta(self, meta):
        meta["struggle_to_afford"]["expression_properties"]["template_options.label"] = \
            '"Do you or " + (model.preferred_name) + "\'s other caregivers ever struggle with being ' \
            'able to afford to pay for household needs, food, or security for the family?"'
        return meta


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
    housemates = fields.Nested(HousemateSchema, many=True)
