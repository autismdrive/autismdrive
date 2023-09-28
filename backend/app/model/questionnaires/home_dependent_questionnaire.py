from flask_sqlalchemy.model import Model
from marshmallow import pre_load
from marshmallow.fields import Nested
from sqlalchemy import Column, String, ARRAY

from app.model.questionnaires.home_mixin import HomeMixin
from app.model.questionnaires.housemate import HousemateSchema
from app.schema.model_schema import ModelSchema


class HomeDependentQuestionnaire(Model, HomeMixin):
    __tablename__ = "home_dependent_questionnaire"
    __label__ = "Home"
    dependent_living_other_hide_expression = (
        '!(model.dependent_living_situation && model.dependent_living_situation.includes("livingOther"))'
    )

    struggle_to_afford_desc = (
        '"Do you or " + (formState.preferredName || "your child") + "\'s other caregivers ever struggle with being '
        'able to afford to pay for household needs, food, or security for the family?"'
    )

    dependent_living_situation = Column(
        ARRAY(String),
        info={
            "display_order": 2.1,
            "type": "multicheckbox",
            "template_options": {
                "type": "array",
                "required": True,
                "label": "Current Living Situation",
                "options": [
                    {"value": "fullTimeGuardian", "label": "With me full-time"},
                    {"value": "partTimeGuardian", "label": "With me part time"},
                    {"value": "otherFamily", "label": "With other parent/guardian/family member "},
                    {"value": "residentialFacility", "label": "Residential facility"},
                    {"value": "groupHome", "label": "Group home"},
                    {"value": "livingOther", "label": "Other (please explain)"},
                ],
            },
            "validators": {"required": "multicheckbox"},
        },
    )
    dependent_living_other = Column(
        String,
        info={
            "display_order": 2.2,
            "type": "input",
            "template_options": {
                "label": "",
                "required": True,
            },
            "hide_expression": dependent_living_other_hide_expression,
            "expression_properties": {
                "template_options.label": '"Please describe "+ (formState.preferredName || "your child") + "\'s current living situation"',
                "template_options.required": "!" + dependent_living_other_hide_expression,
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
                "template_options.label": '"Where does " + (formState.preferredName || "your child") + " currently '
                'live (select all that apply)?"'
            },
        }
        field_groups["housemates"][
            "hide_expression"
        ] = '((formState.mainModel.dependent_living_situation && formState.mainModel.dependent_living_situation.includes("residentialFacility"))||(formState.mainModel.dependent_living_situation && formState.mainModel.dependent_living_situation.includes("groupHome")))'

        field_groups["housemates"]["expression_properties"] = {
            "template_options.label": '"Who else lives with " + (formState.preferredName || "your child") + "?"'
        }

        return field_groups


class HomeDependentQuestionnaireSchema(ModelSchema):
    @pre_load
    def set_field_session(self, data, **kwargs):
        self.fields["housemates"].schema.session = self.session
        return data

    class Meta(ModelSchema.Meta):
        model = HomeDependentQuestionnaire
        fields = (
            "id",
            "last_updated",
            "participant_id",
            "user_id",
            "time_on_task_ms",
            "dependent_living_situation",
            "dependent_living_other",
            "housemates",
            "struggle_to_afford",
        )

    housemates = Nested(HousemateSchema, many=True)
