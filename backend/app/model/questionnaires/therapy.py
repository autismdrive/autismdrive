from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from sqlalchemy import func

from app import db


class Therapy(db.Model):
    __tablename__ = "therapy"
    __label__ = "Therapy or Service"
    __no_export__ = True  # This will be transferred as a part of a parent class
    type_other_hide_expression = '!(model.type && (model.type === "other"))'

    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime(timezone=True), default=func.now())
    supports_questionnaire_id = db.Column(
        "supports_questionnaire_id",
        db.Integer,
        db.ForeignKey("supports_questionnaire.id"),
    )
    type = db.Column(
        db.String,
        info={
            "display_order": 1,
            "type": "radio",
            "className": "vertical-radio-group",
            "template_options": {
                "label": "Select type",
                "placeholder": "Please select",
                "required": True,
                "options": [
                    {
                        "value": "speechLanguage",
                        "label": "Speech/Language Therapy",
                    },
                    {"value": "occupational", "label": "Occupational Therapy"},
                    {"value": "physical", "label": "Physical Therapy"},
                    {
                        "value": "behavioral",
                        "label": "Behavior Therapy (ABA, Lovaas, Discrete Trial Training)",
                    },
                    {
                        "value": "natDevBehavioral",
                        "label": "Naturalistic Developmental Behavioral (Pivotal Response Training, Early Start Denver Model, JASPER, etc)",
                    },
                    {
                        "value": "developmental",
                        "label": "Developmental or relationship-based Therapy (DIR/Floortime)",
                    },
                    {
                        "value": "family",
                        "label": "Family Therapy and/or counseling",
                    },
                    {
                        "value": "behavioralParent",
                        "label": "Behavioral parent training (non ASD specific)",
                    },
                    {
                        "value": "individual",
                        "label": "Individual counseling or therapy",
                    },
                    {
                        "value": "medication",
                        "label": "Medication management/Psychiatry",
                    },
                    {
                        "value": "socialSkills",
                        "label": "Social skills training",
                    },
                    {
                        "value": "parentEducation",
                        "label": "Parent education workshops",
                    },
                    {
                        "value": "alternativeTreatments",
                        "label": "Complementary or alternative treatments (e.g., vitamin/nutrient supplements, special diet, food restrictions)",
                    },
                    {"value": "other", "label": "Others (please specify)"},
                ],
            },
        },
    )
    type_other = db.Column(
        db.String,
        info={
            "display_order": 1.2,
            "type": "textarea",
            "template_options": {
                "label": "Enter therapy or service",
                "required": True,
            },
            "hide_expression": type_other_hide_expression,
            "expression_properties": {
                "template_options.required": '!' + type_other_hide_expression
            }
        },
    )
    timeframe = db.Column(
        db.String,
        info={
            "display_order": 3,
            "type": "radio",
            "template_options": {
                "label": "",
                "required": False,
                "options": [
                    {"value": "current", "label": "Currently receiving"},
                    {"value": "past", "label": "Received in the past"},
                    {"value": "futureInterest", "label": "Interested in receiving"},
                ],
            },
        },
    )
    notes = db.Column(
        db.String,
        info={
            "display_order": 4,
            "type": "textarea",
            "template_options": {
                "label": "Notes on use and/or issues with therapy or service",
                "required": False,
            },
        },
    )

    def get_field_groups(self):
        info = {
            "type_group": {
                "fields": ["type", "type_other"],
                "display_order": 1,
                "wrappers": ["card"],
                "template_options": {
                    "label": "Type of therapy or service"
                },
            }
        }
        return info


class TherapySchema(ModelSchema):
    class Meta:
        model = Therapy
        ordered = True
        fields = ("id", "last_updated", "supports_questionnaire_id", "type", "type_other",
                  "timeframe", "notes", "participant_id", "user_id")
    participant_id = fields.Method('get_participant_id', dump_only=True)
    user_id = fields.Method('get_user_id', dump_only=True)

    def get_participant_id(self, obj):
        return obj.supports_questionnaire.participant_id

    def get_user_id(self, obj):
        return obj.supports_questionnaire.user_id
