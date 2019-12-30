from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from sqlalchemy import func

from app import db


class AlternativeAugmentative(db.Model):
    __tablename__ = "alternative_augmentative"
    __label__ = "Alternative and Augmentative Communication"
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
            "display_order": 1.1,
            "type": "radio",
            "default": "self",
            "class_name": "vertical-radio-group",
            "template_options": {
                "required": True,
                "label": "Select device",
                "placeholder": "Please select",
                "options": [
                    {
                        "value": "noTechAAC",
                        "label": "No-Tech AAC: facial expressions, body posture, head nods, reaching/pointing, gestures, or signs",
                    },
                    {
                        "value": "lowTechAAC",
                        "label": "Low-Tech AAC: pen and paper, pictures/symbols, communication boards/books",
                    },
                    {
                        "value": "midTechAAC",
                        "label": "Mid -Tech AAC: battery operated or simple electronic devices",
                    },
                    {
                        "value": "highTechAAC",
                        "label": "High-Tech AAC: computerized devices (e.g., tablets, ipads) displaying letters, words, pictures, or symbols",
                    },
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
                "label": "Enter alternative and augmentative communication system",
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
                "label": "Notes on use and/or issues with alternative and augmentative communication system",
                "required": False,
            },
        },
    )

    def get_field_groups(self):
        return {
            "type": {
                "fields": ["type", "type_other"],
                "display_order": 1,
                "wrappers": ["card"],
                "template_options": {"label": "Type of alternative and augmentative communication system"},
            }
        }


class AlternativeAugmentativeSchema(ModelSchema):
    class Meta:
        model = AlternativeAugmentative
        ordered = True
        fields = ("id", "last_updated", "supports_questionnaire_id", "type", "type_other", "timeframe", "notes",
                  "participant_id", "user_id")
    participant_id = fields.Method('get_participant_id', dump_only=True)
    user_id = fields.Method('get_user_id', dump_only=True)

    def get_participant_id(self, obj):
        return obj.supports_questionnaire.participant_id

    def get_user_id(self, obj):
        return obj.supports_questionnaire.user_id
