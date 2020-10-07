from marshmallow import fields, missing
from sqlalchemy import func

from app import db
from app.schema.model_schema import ModelSchema


class Medication(db.Model):
    __tablename__ = "medication"
    __label__ = "Medication"
    __no_export__ = True  # This will be transferred as a part of a parent class
    symptom_other_hide_expression = '!(model.symptom && (model.symptom === "symptomOther"))'

    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime(timezone=True), default=func.now())
    supports_questionnaire_id = db.Column(
        "supports_questionnaire_id",
        db.Integer,
        db.ForeignKey("supports_questionnaire.id"),
    )
    symptom = db.Column(
        db.String,
        info={
            "display_order": 1,
            "type": "select",
            "template_options": {
                "label": "Select symptom",
                "placeholder": "Please select",
                "required": True,
                "options": [
                    {"value": "symptomAnxiety", "label": "Anxiety"},
                    {"value": "symptomDepression", "label": "Depression"},
                    {"value": "symptomInsomnia", "label": "Insomnia"},
                    {"value": "symptomADHD", "label": "ADHD"},
                    {"value": "symptomOther", "label": "Other"},
                ],
            },
        }
    )
    symptom_other = db.Column(
        db.String,
        info={
            "display_order": 1.2,
            "type": "textarea",
            "template_options": {
                "label": "Enter symptom",
                "required": True,
            },
            "hide_expression": symptom_other_hide_expression,
            "expression_properties": {
                "template_options.required": '!' + symptom_other_hide_expression
            }
        },
    )
    name = db.Column(
        db.String,
        info={
            "display_order": 2,
            "type": "textarea",
            "template_options": {
                "label": "Name of Medication (if known)",
            },
        },
    )
    notes = db.Column(
        db.String,
        info={
            "display_order": 3,
            "type": "textarea",
            "template_options": {
                "label": "Notes on use and/or issues with medication",
                "required": False,
            },
        },
    )

    def get_field_groups(self):
        info = {
            "symptom_group": {
                "fields": ["symptom", "symptom_other"],
                "display_order": 1,
                "wrappers": ["card"],
                "template_options": {
                    "label": ""
                },
                "expression_properties": {
                    "template_options.label": {
                        "RELATIONSHIP_SPECIFIC": {
                            "self_participant": '"Symptom for which you are taking medication"',
                            "self_guardian": '"Symptom for which you are taking medication"',
                            "self_professional": '"Symptom for which you are taking medication"',
                            "dependent": '"Symptom for which " + (formState.preferredName || "your child") + " is taking medication"'
                        }
                    }
                },
            }
        }
        return info


class MedicationSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Medication
        fields = ("id", "last_updated", "supports_questionnaire_id", "symptom", "symptom_other", "name", "notes",
                  "participant_id", "user_id")
    participant_id = fields.Method('get_participant_id', dump_only=True)
    user_id = fields.Method('get_user_id', dump_only=True)

    def get_participant_id(self, obj):
        if obj is None:
            return missing
        return obj.supports_questionnaire.participant_id

    def get_user_id(self, obj):
        if obj is None:
            return missing
        return obj.supports_questionnaire.user_id
