from marshmallow_sqlalchemy import ModelSchema
from sqlalchemy import func

from app import db, ma
from app.export_service import ExportService


class IdentificationQuestionnaire(db.Model):
    __tablename__ = "identification_questionnaire"
    __label__ = "Identification"
    __question_type__ = ExportService.TYPE_IDENTIFYING
    __estimated_duration_minutes__ = 5
    relationship_to_participant_other_hide_expression = '!(model.relationship_to_participant && (model.relationship_to_participant === "other"))'

    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime(timezone=True), default=func.now())
    time_on_task_ms = db.Column(db.BigInteger, default=0)

    participant_id = db.Column("participant_id", db.Integer, db.ForeignKey("stardrive_participant.id"))

    user_id = db.Column(
        "user_id", db.Integer, db.ForeignKey("stardrive_user.id")
    )
    relationship_to_participant = db.Column(
        db.String,
        info={
            "RELATIONSHIP_REQUIRED": ['dependent'],
            "display_order": 1.1,
            "type": "radio",
            "template_options": {
                "required": False,
                "label": "",
                "options": [
                    {"value": "bioMother", "label": "Biological mother"},
                    {"value": "bioFather", "label": "Biological father"},
                    {"value": "adoptMother", "label": "Adoptive mother"},
                    {"value": "adoptFather", "label": "Adoptive father"},
                    {"value": "other", "label": "Other"},
                ],
            },
        },
    )
    relationship_to_participant_other = db.Column(
        db.String,
        info={
            "RELATIONSHIP_REQUIRED": ['dependent'],
            "display_order": 1.2,
            "type": "input",
            "template_options": {
                "label": "Enter your relationship",
                "required": True,
            },
            "hide_expression": relationship_to_participant_other_hide_expression,
            "expression_properties": {
                "template_options.required": '!' + relationship_to_participant_other_hide_expression
            }
        },
    )
    first_name = db.Column(
        db.String,
        info={
            "display_order": 2,
            "type": "input",
            "template_options": {"label": "First name", "required": True},
        },
    )
    middle_name = db.Column(
        db.String,
        info={
            "display_order": 3,
            "type": "input",
            "template_options": {"label": "Middle name", "required": False},
        },
    )
    last_name = db.Column(
        db.String,
        info={
            "display_order": 4,
            "type": "input",
            "template_options": {"label": "Last name", "required": True},
        },
    )
    is_first_name_preferred = db.Column(
        db.Boolean,
        info={
            "display_order": 5,
            "type": "radio",
            "template_options": {
                "required": False,
                "label": {
                            "RELATIONSHIP_SPECIFIC": {
                                "self_participant": "Is this your preferred name?",
                                "self_guardian": "Is this your preferred name?",
                                "self_professional": "Is this your preferred name?",
                                "dependent": "Is this your child\'s preferred name?",
                            }
                        },
                "options": [
                    {"value": True, "label": "Yes"},
                    {"value": False, "label": "No"},
                ],
            },
        },
    )
    nickname = db.Column(
        db.String,
        info={
            "display_order": 6,
            "type": "input",
            "template_options": {
                "label": "Nickname",
                "required": False,
            },
            "hide_expression": "model.is_first_name_preferred",
        },
    )
    birthdate = db.Column(
        db.Date,
        info={
            "display_order": 7,
            "type": "datepicker",
            "template_options": {
                "required": True,
                "label": {
                            "RELATIONSHIP_SPECIFIC": {
                                "self_participant": "Your date of birth",
                                "self_guardian": "Your date of birth",
                                "self_professional": "Your date of birth",
                                "dependent": "Your child\'s date of birth",
                            }
                        },
            },
        },
    )
    birth_city = db.Column(
        db.String,
        info={
            "display_order": 8,
            "type": "input",
            "template_options": {
                "required": True,
                "label": {
                            "RELATIONSHIP_SPECIFIC": {
                                "self_participant": "Your city/municipality of birth",
                                "self_guardian": "Your city/municipality of birth",
                                "self_professional": "Your city/municipality of birth",
                                "dependent": "Your child\'s city/municipality of birth",
                            }
                        },
            },
        },
    )
    birth_state = db.Column(
        db.String,
        info={
            "display_order": 9,
            "type": "input",
            "template_options": {
                "required": True,
                "label": {
                            "RELATIONSHIP_SPECIFIC": {
                                "self_participant": "Your state of birth",
                                "self_guardian": "Your state of birth",
                                "self_professional": "Your state of birth",
                                "dependent": "Your child\'s state of birth",
                            }
                        },
            },
        },
    )
    is_english_primary = db.Column(
        db.Boolean,
        info={
            "display_order": 10,
            "type": "radio",
            "template_options": {
                "required": False,
                "label": {
                            "RELATIONSHIP_SPECIFIC": {
                                "self_participant": "Is your primary language English?",
                                "self_guardian": "Is your primary language English?",
                                "self_professional": "Is your primary language English?",
                                "dependent": "Is your child\'s primary language English?",
                            }
                        },
                "options": [
                    {"value": True, "label": "Yes"},
                    {"value": False, "label": "No"},
                ],
            },
        },
    )

    def get_name(self):
        if not self.is_first_name_preferred:
            return self.nickname
        else:
            return self.first_name

    def get_field_groups(self):
        return {
                "relationship": {
                    "RELATIONSHIP_REQUIRED": ['dependent'],
                    "fields": [
                        "relationship_to_participant",
                        "relationship_to_participant_other",
                    ],
                    "display_order": 0,
                    "wrappers": ["card"],
                    "template_options": {
                        "label": "Your relationship to your child or the person with autism on whom you are providing information:"
                    },
                },
                "intro": {
                    "fields": [],
                    "display_order": 1,
                    "wrappers": ["help"],
                    "template_options": {
                        "description": {
                            "RELATIONSHIP_SPECIFIC": {
                                "self_participant": "Please answer the following questions about yourself (* indicates required response):",
                                "self_guardian": "Please answer the following questions about yourself (* indicates required response):",
                                "self_professional": "Please answer the following questions about yourself (* indicates required response):",
                                "dependent": "Please answer the following questions about your child or the person with autism on whom you are providing information",
                            }
                        }
                    },
                },
            }


class IdentificationQuestionnaireSchema(ModelSchema):
    class Meta:
        model = IdentificationQuestionnaire
        ordered = True
        include_fk = True
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.questionnaireendpoint', name="identification_questionnaire", id='<id>')
    })
