from marshmallow import fields, pre_load
from marshmallow_sqlalchemy import ModelSchema

from app import db
from app.model.questionnaires.housemate import Housemate, HousemateSchema
from app.model.questionnaires.home_mixin import HomeMixin


class HomeDependentQuestionnaire(db.Model, HomeMixin):
    __tablename__ = "home_dependent_questionnaire"
    __label__ = "Home"

    struggle_to_afford_label = '"Do you or " + (model.preferred_name) + "\'s other caregivers ever struggle with being ' \
                               'able to afford to pay for household needs, food, or security for the family?"'

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
            "hide_expression": '!(model.dependent_living_situation && model.dependent_living_situation.includes("livingOther"))',
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

        # As housemates is a different model, it does not work to put the dependent's name into the label
        # in the same way we have done for other labels (model.preferred_name will return undefined)
        field_groups["housemates"]["template_options"]["label"] = "Who else lives with your child?"

        return field_groups


class HomeDependentQuestionnaireSchema(ModelSchema):
    @pre_load
    def set_field_session(self, data):
        self.fields['housemates'].schema.session = self.session

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
