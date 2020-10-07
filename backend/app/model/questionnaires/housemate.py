from marshmallow import fields, missing
from sqlalchemy import func

from app import db
from app.schema.model_schema import ModelSchema


class Housemate(db.Model):
    __tablename__ = "housemate"
    __label__ = "Housemate"
    __no_export__ = True  # This will be transferred as a part of a parent class
    relationship_other_hide_expression = '!(model.relationship && (model.relationship === "relationOther"))'

    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime(timezone=True), default=func.now())
    home_dependent_questionnaire_id = db.Column(
        "home_dependent_questionnaire_id",
        db.Integer,
        db.ForeignKey("home_dependent_questionnaire.id"),
    )
    home_self_questionnaire_id = db.Column(
        "home_self_questionnaire_id",
        db.Integer,
        db.ForeignKey("home_self_questionnaire.id"),
    )
    name = db.Column(
        db.String,
        info={
            "display_order": 3.1,
            "type": "input",
            "template_options": {"label": "Name", "required": True},
        },
    )
    relationship = db.Column(
        db.String,
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
                        "dependent": '"Relationship to " + (formState.preferredName || "your child")'
                    }
                }
            },
        },
    )
    relationship_other = db.Column(
        db.String,
        info={
            "display_order": 3.3,
            "type": "input",
            "template_options": {
                "label": "Please enter their relationship",
                "required": True,
            },
            "hide_expression": relationship_other_hide_expression,
            "expression_properties": {
                "template_options.required": '!' + relationship_other_hide_expression
            }
        },
    )
    age = db.Column(
        db.Integer,
        info={
            "display_order": 3.4,
            "type": "input",
            "template_options": {
                "label": "Age",
                "type": 'number',
                "max": 130,
                "required": True,
            },
            "validation": {
                "messages": {
                    "max": 'Please enter age in years',
                }
            }
        },
    )
    has_autism = db.Column(
        db.Boolean,
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
            }
        },
    )

    def get_field_groups(self):
        return {}


class HousemateSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Housemate
        fields = ("id", "last_updated", "home_dependent_questionnaire_id", "home_self_questionnaire_id", "name",
                  "relationship", "relationship_other", "age", "has_autism", "participant_id", "user_id")
    participant_id = fields.Method('get_participant_id')
    user_id = fields.Method('get_user_id')
    home_dependent_questionnaire_id = fields.Integer(required=False, allow_none=True)
    home_self_questionnaire_id = fields.Integer(required=False, allow_none=True)
    home_dependent_questionnaire = fields.Nested('HomeDependentQuestionnaire', required=False, allow_none=True)
    home_self_questionnaire = fields.Nested('HomeSelfQuestionnaire', required=False, allow_none=True)

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
