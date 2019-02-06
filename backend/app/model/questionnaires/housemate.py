import datetime

from marshmallow_sqlalchemy import ModelSchema

from app import db


class Housemate(db.Model):
    __tablename__ = "housemate"
    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime, default=datetime.datetime.now)
    home_questionnaire_id = db.Column(
        "home_questionnaire_id", db.Integer, db.ForeignKey("home_questionnaire.id")
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
                "options": [
                    {"value": "bioParent", "label": "Biological Parent"},
                    {"value": "bioSibling", "label": "Biological Sibling"},
                    {"value": "stepParent", "label": "Step Parent"},
                    {"value": "stepSibling", "label": "Step Sibling"},
                    {"value": "adoptParent", "label": "Adoptive Parent"},
                    {"value": "adoptSibling", "label": "Adoptive Sibling"},
                    {"value": "spouse", "label": "Spouse"},
                    {"value": "significantOther", "label": "Significant Other"},
                    {"value": "child", "label": "Child"},
                    {"value": "roommate", "label": "Roommate"},
                    {"value": "paidCaregiver", "label": "Paid Caregiver"},
                    {"value": "relationOther", "label": "Other"},
                ],
            },
            "expression_properties": {
                "template_options.label": '"Relationship to " + (formState.mainModel.is_self ? "you" : (model.nickname || model.first_name || "your child"))'
            },
        },
    )
    relationship_other = db.Column(
        db.String,
        info={
            "display_order": 3.3,
            "type": "input",
            "template_options": {"placeholder": "Please enter their relationship"},
            "hide_expression": '!(model.relationship && (model.relationship === "relationOther"))',
        },
    )
    age = db.Column(
        db.Integer,
        info={
            "display_order": 3.4,
            "type": "input",
            "template_options": {"type": "number", "label": "Age", "required": True},
        },
    )
    has_autism = db.Column(
        db.Boolean,
        info={
            "display_order": 3.5,
            "type": "radio",
            "default_value": True,
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

    def get_meta(self):
        info = {"table": {"sensitive": False, "label": "Housemate"}}
        for c in self.metadata.tables["housemate"].columns:
            if c.info:
                info[c.name] = c.info
        return info


class HousemateSchema(ModelSchema):
    class Meta:
        model = Housemate
        fields = (
            "id",
            "last_updated",
            "home_questionnaire_id",
            "name",
            "relationship",
            "relationship_other",
            "age",
            "has_autism",
        )


class HousemateMetaSchema(ModelSchema):
    class Meta:
        model = Housemate
        fields = ("get_meta",)
