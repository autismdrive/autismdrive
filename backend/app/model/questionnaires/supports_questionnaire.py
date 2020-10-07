from marshmallow import fields, pre_load
from sqlalchemy import func

from app import db, ma
from app.export_service import ExportService
from app.model.questionnaires.therapy import Therapy, TherapySchema
from app.model.questionnaires.medication import Medication, MedicationSchema
from app.model.questionnaires.assistive_device import AssistiveDevice, AssistiveDeviceSchema
from app.model.questionnaires.alternative_augmentative import AlternativeAugmentative, AlternativeAugmentativeSchema
from app.schema.model_schema import ModelSchema


class SupportsQuestionnaire(db.Model):
    __tablename__ = "supports_questionnaire"
    __label__ = "Supports"
    __question_type__ = ExportService.TYPE_UNRESTRICTED
    __estimated_duration_minutes__ = 5
    alternative_med_other_hide_expression = '!(model.alternative_med && model.alternative_med.includes("altMedVitaminOther") || model.alternative_med && model.alternative_med.includes("altMedOther"))'

    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime(timezone=True), default=func.now())
    time_on_task_ms = db.Column(db.BigInteger, default=0)

    participant_id = db.Column(
        "participant_id", db.Integer, db.ForeignKey("stardrive_participant.id")
    )
    user_id = db.Column(
        "user_id", db.Integer, db.ForeignKey("stardrive_user.id")
    )
    medications = db.relationship(
        "Medication",
        backref=db.backref("supports_questionnaire", lazy=True),
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    alternative_med = db.Column(
        db.String,
        info={
            "display_order": 1,
            "type": "multicheckbox",
            "template_options": {
                "type": "array",
                "options": [
                    {"value": "altMedChiropractics", "label": "Chiropractics"},
                    {"value": "altMedB6Mag", "label": "High dosing Vitamin B6 and magnesium"},
                    {"value": "altMedVitaminOther", "label": "Other vitamin supplements"},
                    {"value": "altMedAminoAcids", "label": "Amino Acids"},
                    {"value": "altMedEssFattyAcids", "label": "Essential fatty acids"},
                    {"value": "altMedGlutenFree", "label": "Gluten-free diet"},
                    {"value": "altMedOther", "label": "Other"},
                ],
                "description": "(select all that apply)",
            },
        }
    )
    alternative_med_other = db.Column(
        db.String,
        info={
            "display_order": 1.2,
            "type": "textarea",
            "template_options": {
                "label": "Enter other alternative treatment",
                "required": True,
            },
            "hide_expression": alternative_med_other_hide_expression,
            "expression_properties": {
                "template_options.required": '!' + alternative_med_other_hide_expression
            }
        },
    )
    therapies = db.relationship(
        "Therapy",
        backref=db.backref("supports_questionnaire", lazy=True),
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    assistive_devices = db.relationship(
        "AssistiveDevice",
        backref=db.backref("supports_questionnaire", lazy=True),
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    alternative_augmentative = db.relationship(
        "AlternativeAugmentative",
        backref=db.backref("supports_questionnaire", lazy=True),
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    def get_field_groups(self):
        return {
            "medications": {
                "type": "repeat",
                "display_order": 1,
                "wrappers": ["card"],
                "repeat_class": Medication,
                "template_options": {
                    "label": "",
                    "description": "Add a medication",
                },
                "expression_properties": {
                    "template_options.label": {
                        "RELATIONSHIP_SPECIFIC": {
                            "self_participant": '"Do you take any medications and/or vitamins?"',
                            "self_guardian": '"Do you take any medications and/or vitamins?"',
                            "dependent": '"Does " + (formState.preferredName || "your child")  + " take any medications and/or vitamins?"',
                        }
                    }
                }
            },
            "alternative_med_group": {
                "fields": ["alternative_med", "alternative_med_other"],
                "display_order": 2,
                "wrappers": ["card"],
                "template_options": {
                    "label": ""
                },
                "expression_properties": {
                    "template_options.label": {
                        "RELATIONSHIP_SPECIFIC": {
                            "self_participant": '"Are you receiving any complementary or alternative treatments?"',
                            "self_guardian": '"Are you receiving any complementary or alternative treatments?"',
                            "self_professional": '"Are you receiving any complementary or alternative treatments?"',
                            "dependent": '"Is " + (formState.preferredName || "your child") + " receiving any complementary or alternative treatments?"'
                        }
                    }
                },
            },
            "therapies": {
                "type": "repeat",
                "display_order": 3,
                "wrappers": ["card"],
                "repeat_class": Therapy,
                "template_options": {
                    "label": "",
                    "description": "Add a therapy or service",
                },
                "expression_properties": {
                    "template_options.label": {
                        "RELATIONSHIP_SPECIFIC": {
                            "self_participant": '"What kinds of therapies and services do you currently receive?"',
                            "self_guardian": '"What kinds of therapies and services do you currently receive?"',
                            "dependent": '"What kinds of therapies and services does " + (formState.preferredName || "your child")  + " currently receive?"',
                        }
                    }
                }
            },
            "assistive_devices": {
                "type": "repeat",
                "display_order": 4,
                "wrappers": ["card"],
                "repeat_class": AssistiveDevice,
                "template_options": {
                    "label": '',
                    "description": "Add an assistive device",
                },
                "expression_properties": {
                    "template_options.label": {
                            "RELATIONSHIP_SPECIFIC": {
                                "self_participant": '"Do you use an assistive device?"',
                                "self_guardian": '"Do you use an assistive device?"',
                                "dependent": '"Does " + (formState.preferredName || "your child")  + " use an assistive device?"',
                            }
                        }
                }
            },
            "alternative_augmentative": {
                "type": "repeat",
                "display_order": 5,
                "wrappers": ["card"],
                "repeat_class": AlternativeAugmentative,
                "template_options": {
                    "label": '',
                    "description": "Add AAC",
                },
                "expression_properties": {
                    "template_options.label": {
                            "RELATIONSHIP_SPECIFIC": {
                                "self_participant": '"Do you use an AAC (alternative & augmentative communication) system?"',
                                "self_guardian": '"Do you use an AAC (alternative & augmentative communication) system?"',
                                "dependent": '"Does " + (formState.preferredName || "your child")  + " use an AAC (alternative & augmentative communication) system?"',
                            }
                        }
                }
            }
        }


class SupportsQuestionnaireSchema(ModelSchema):
    @pre_load
    def set_field_session(self, data, **kwargs):
        self.fields['medications'].schema.session = self.session
        self.fields['therapies'].schema.session = self.session
        self.fields['alternative_augmentative'].schema.session = self.session
        self.fields['assistive_devices'].schema.session = self.session
        return data

    class Meta(ModelSchema.Meta):
        model = SupportsQuestionnaire
        fields = ("id", "last_updated", "time_on_task_ms", "participant_id", "user_id", "medications", "therapies",
                  "assistive_devices", "alternative_augmentative", "_links")
    medications = ma.Nested(MedicationSchema, many=True)
    therapies = ma.Nested(TherapySchema, many=True)
    assistive_devices = ma.Nested(AssistiveDeviceSchema, many=True)
    alternative_augmentative = ma.Nested(AlternativeAugmentativeSchema, many=True)
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.questionnaireendpoint', name='supports_questionnaire', id='<id>'),
    })
