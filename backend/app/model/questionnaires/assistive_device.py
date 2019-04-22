import datetime

from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

from app import db


class AssistiveDevice(db.Model):
    __tablename__ = "assistive_device"
    __label__ = "Assistive Device"
    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime, default=datetime.datetime.now)
    supports_questionnaire_id = db.Column(
        "supports_questionnaire_id",
        db.Integer,
        db.ForeignKey("supports_questionnaire.id"),
    )
    type_group = db.Column(
        db.String,
        info={
            "display_order": 1.1,
            "type": "select",
            "template_options": {
                "required": False,
                "label": "Select category of device",
                "options": [
                    {
                        "value": "mobility",
                        "label": "Mobility aids",
                    },
                    {
                        "value": "hearing",
                        "label": "Hearing assistance",
                    },
                    {
                        "value": "computer",
                        "label": "Computer software and hardware",
                    },
                    {
                        "value": "building",
                        "label": "ADA Building Modifications",
                    },
                    {
                        "value": "other",
                        "label": "Others",
                    }
                ]
            },
        }
    )
    type = db.Column(
        db.String,
        info={
            "display_order": 1.2,
            "type": "select",
            "template_options": {
                "required": False,
                "label": "Select device",
                "all_options": [
                    {
                        "value": "cane",
                        "label": "Canes",
                        "groupValue": "mobility",
                    },
                    {
                        "value": "crutches",
                        "label": "Crutches",
                        "groupValue": "mobility",
                    },
                    {
                        "value": "orthotic",
                        "label": "Orthotic devices",
                        "groupValue": "mobility",
                    },
                    {
                        "value": "prosthetic",
                        "label": "Prosthetic devices",
                        "groupValue": "mobility",
                    },
                    {
                        "value": "scooter",
                        "label": "Scooters",
                        "groupValue": "mobility",
                    },
                    {
                        "value": "walker",
                        "label": "Walkers",
                        "groupValue": "mobility",
                    },
                    {
                        "value": "wheelchair",
                        "label": "Wheelchairs",
                        "groupValue": "mobility",
                    },
                    {
                        "value": "captioning",
                        "label": "Closed captioning",
                        "groupValue": "hearing",
                    },
                    {
                        "value": "hearingAid",
                        "label": "Hearing aids",
                        "groupValue": "hearing",
                    },
                    {
                        "value": "alarmLight",
                        "label": "Indicator/alarm lights",
                        "groupValue": "hearing",
                    },
                    {
                        "value": "cognitiveAids",
                        "label": "Cognitive aids",
                        "groupValue": "computer",
                    },
                    {
                        "value": "screenEnlarge",
                        "label": "Screen enlargement applications",
                        "groupValue": "computer",
                    },
                    {
                        "value": "screenReader",
                        "label": "Screen readers",
                        "groupValue": "computer",
                    },
                    {
                        "value": "voiceRecognition",
                        "label": "Voice recognition programs",
                        "groupValue": "computer",
                    },
                    {
                        "value": "adaptSwitch",
                        "label": "Adaptive switches",
                        "groupValue": "building",
                    },
                    {
                        "value": "grabBar",
                        "label": "Grab bars",
                        "groupValue": "building",
                    },
                    {
                        "value": "ramp",
                        "label": "Ramps",
                        "groupValue": "building",
                    },
                    {
                        "value": "wideDoor",
                        "label": "Wider doorways",
                        "groupValue": "building",
                    },
                    {
                        "value": "other",
                        "label": "Other assistive device",
                        "groupValue": "other",
                    }
                ]
            },
            "expression_properties": {
                'template_options.options': 'this.field.templateOptions.allOptions.filter(t => t.groupValue === "other" || t.groupValue === model.type_group)',
                'model.type': 'model.type_group === "other" ? "other" : (this.field.templateOptions.options.find(o => o.id === model.type) ? model.type : null)',
            },
        }
    )
    type_other = db.Column(
        db.String,
        info={
            "display_order": 1.2,
            "type": "textarea",
            "template_options": {
                "label": "Enter assistive device",
                "appearance": "standard",
                "required": False,
            },
            "hide_expression": '!((model.type_group && (model.type_group === "other")) || (model.type && (model.type === "other")))',
        },
    )
    timeframe = db.Column(
        db.String,
        info={
            "display_order": 3,
            "type": "radio",
            "default_value": True,
            "template_options": {
                "label": "",
                "required": False,
                "options": [
                    {"value": "current", "label": "Currently using"},
                    {"value": "past", "label": "Used in the past"},
                    {"value": "futureInterest", "label": "Interested in using"},
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
                "label": "Notes on use and/or issues with assistive device",
                "required": False,
            },
        },
    )

    def get_field_groups(self):
        return {
            "type": {
                "fields": ["type_group", "type", "type_other"],
                "display_order": 1,
                "wrappers": ["card"],
                "template_options": {"label": "Type of assistive device"},
            }
        }


class AssistiveDeviceSchema(ModelSchema):
    class Meta:
        model = AssistiveDevice
        ordered = True
        fields = ("id", "last_updated", "supports_questionnaire_id", "type_group", "type", "type_other", "timeframe", "notes",
                  "participant_id", "user_id")
    participant_id = fields.Method('get_participant_id')
    user_id = fields.Method('get_user_id')

    def get_participant_id(self, obj):
        return obj.supports_questionnaire.participant_id

    def get_user_id(self, obj):
        return obj.supports_questionnaire.user_id
