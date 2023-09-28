from marshmallow import fields, missing
from sqlalchemy import func, Column, Integer, String, ForeignKey, DateTime, Boolean

from app.database import Base
from app.model.questionnaires.home_dependent_questionnaire import HomeDependentQuestionnaireSchema
from app.model.questionnaires.home_self_questionnaire import HomeSelfQuestionnaireSchema
from app.schema.model_schema import ModelSchema


class Housemate(Base):
    __tablename__ = "housemate"
    __label__ = "Housemate"
    __no_export__ = True  # This will be transferred as a part of a parent class
    relationship_other_hide_expression = '!(model.relationship && (model.relationship === "relationOther"))'

    id = Column(Integer, primary_key=True)
    last_updated = Column(DateTime(timezone=True), default=func.now())
    home_dependent_questionnaire_id = Column(
        "home_dependent_questionnaire_id",
        Integer,
        ForeignKey("home_dependent_questionnaire.id"),
    )
    home_self_questionnaire_id = Column(
        "home_self_questionnaire_id",
        Integer,
        ForeignKey("home_self_questionnaire.id"),
    )
    name = Column(
        String,
        info={
            "display_order": 3.1,
            "type": "input",
            "template_options": {"label": "Name", "required": True},
        },
    )
    relationship = Column(
        String,
        info={
            "display_order": 3.2,
            "type": "select",
            "template_options": {
                "required": False,
                "label": "Relationship",
                "placeholder": "Please select",
                "options": [
                    {"value": "bioParent", "label": "Biological Parent"},
                    {"value": "bioSibling", "label": "Biological Sibling"},
                    {"value": "stepParent", "label": "Step Parent"},
                    {"value": "stepSibling", "label": "Step Sibling"},
                    {"value": "adoptParent", "label": "Adoptive Parent"},
                    {"value": "adoptSibling", "label": "Adoptive Sibling"},
                    {"value": "spouse", "label": "Spouse"},
                    {
                        "value": "significantOther",
                        "label": "Significant Other",
                    },
                    {"value": "child", "label": "Child"},
                    {"value": "roommate", "label": "Roommate"},
                    {"value": "paidCaregiver", "label": "Paid Caregiver"},
                    {"value": "relationOther", "label": "Other"},
                ],
            },
            "expression_properties": {
                "template_options.label": {
                    "RELATIONSHIP_SPECIFIC": {
                        "self_participant": '"Relationship to you"',
                        "self_guardian": '"Relationship to you"',
                        "self_professional": '"Relationship to you"',
                        "dependent": '"Relationship to " + (formState.preferredName || "your child")',
                    }
                }
            },
        },
    )
    relationship_other = Column(
        String,
        info={
            "display_order": 3.3,
            "type": "input",
            "template_options": {
                "label": "Please enter their relationship",
                "required": True,
            },
            "hide_expression": relationship_other_hide_expression,
            "expression_properties": {"template_options.required": "!" + relationship_other_hide_expression},
        },
    )
    age = Column(
        Integer,
        info={
            "display_order": 3.4,
            "type": "input",
            "template_options": {
                "label": "Age",
                "type": "number",
                "max": 130,
                "required": True,
            },
            "validation": {
                "messages": {
                    "max": "Please enter age in years",
                }
            },
        },
    )
    has_autism = Column(
        Boolean,
        info={
            "display_order": 3.5,
            "type": "radio",
            "template_options": {
                "label": "Does this relation have autism?",
                "required": False,
                "options": [
                    {"value": True, "label": "Yes"},
                    {"value": False, "label": "No"},
                ],
            },
        },
    )

    def get_field_groups(self):
        return {}


class HousemateSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Housemate
        fields = (
            "id",
            "last_updated",
            "home_dependent_questionnaire_id",
            "home_self_questionnaire_id",
            "name",
            "relationship",
            "relationship_other",
            "age",
            "has_autism",
            "participant_id",
            "user_id",
        )

    participant_id = fields.Method("get_participant_id")
    user_id = fields.Method("get_user_id")
    home_dependent_questionnaire_id = fields.Integer(required=False, allow_none=True)
    home_self_questionnaire_id = fields.Integer(required=False, allow_none=True)
    home_dependent_questionnaire = fields.Nested(HomeDependentQuestionnaireSchema, required=False, allow_none=True)
    home_self_questionnaire = fields.Nested(HomeSelfQuestionnaireSchema, required=False, allow_none=True)

    def get_participant_id(self, obj):
        if obj is None:
            return missing
        elif obj.home_dependent_questionnaire is not None:
            return obj.home_dependent_questionnaire.participant_id
        elif obj.home_self_questionnaire is not None:
            return obj.home_self_questionnaire.participant_id

    def get_user_id(self, obj):
        if obj is None:
            return missing
        elif obj.home_dependent_questionnaire is not None:
            return obj.home_dependent_questionnaire.user_id
        elif obj.home_self_questionnaire is not None:
            return obj.home_self_questionnaire.user_id
