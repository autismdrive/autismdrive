import datetime

from marshmallow_sqlalchemy import ModelSchema

from app import db


class Medication(db.Model):
    __tablename__ = "medication"
    __label__ = "Medication"
    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime, default=datetime.datetime.now)
    supports_questionnaire_id = db.Column(
        "supports_questionnaire_id",
        db.Integer,
        db.ForeignKey("supports_questionnaire.id"),
    )
    symptom = db.Column(
        db.String,
        info={
            "display_order": 1,
            "type": "multicheckbox",
            "template_options": {
                "type": "array",
                "required": True,
                "options": [
                    {"value": "symptomAnxiety", "label": "Anxiety"},
                    {"value": "symptomDepression", "label": "Depression"},
                    {"value": "symptomInsomnia", "label": "Insomnia"},
                    {"value": "symptomADHD", "label": "ADHD"},
                    {"value": "symptomOther", "label": "Other"},
                ],
                "description": "(select all that apply)",
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
                "appearance": "standard",
                "required": False,
            },
            "hide_expression": '!(model.symptom && (model.symptom.includes("symptomOther")))',
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
    class Meta:
        model = Medication
        ordered = True
