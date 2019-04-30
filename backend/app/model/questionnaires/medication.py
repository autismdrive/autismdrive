import datetime

from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

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
    name = db.Column(
        db.String,
        info={
            "display_order": 1,
            "type": "textarea",
            "template_options": {
                "label": "Name of Medication or Vitamin",
                "required": True,
            },
        },
    )
    dosage = db.Column(
        db.String,
        info={
            "display_order": 2,
            "type": "textarea",
            "template_options": {"label": "Dosage", "required": False},
        },
    )
    time_frame = db.Column(
        db.String,
        info={
            "display_order": 3,
            "type": "radio",
            "template_options": {
                "label": "",
                "required": False,
                "options": [
                    {"value": "current", "label": "Currently taking"},
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
                "label": "Notes on use and/or issues with medication",
                "required": False,
            },
        },
    )

    def get_field_groups(self):
        return {}


class MedicationSchema(ModelSchema):
    class Meta:
        model = Medication
        ordered = True
        fields = ("id", "last_updated", "supports_questionnaire_id", "name", "dosage", "time_frame", "notes",
                  "participant_id", "user_id")
    participant_id = fields.Method('get_participant_id')
    user_id = fields.Method('get_user_id')

    def get_participant_id(self, obj):
        return obj.supports_questionnaire.participant_id

    def get_user_id(self, obj):
        return obj.supports_questionnaire.user_id
