import datetime

from marshmallow_sqlalchemy import ModelSchema

from app import db
from app.question_service import QuestionService


class DevelopmentalQuestionnaire(db.Model):
    __tablename__ = "developmental_questionnaire"
    __label__ = "Birth and Developmental History"
    __question_type__ = QuestionService.TYPE_UNRESTRICTED
    __estimated_duration_minutes__ = 5

    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime, default=datetime.datetime.now)
    time_on_task_ms = db.Column(db.BigInteger, default=0)

    participant_id = db.Column(
        "participant_id", db.Integer, db.ForeignKey("stardrive_participant.id")
    )
    user_id = db.Column(
        "user_id", db.Integer, db.ForeignKey("stardrive_user.id")
    )
    had_birth_complications = db.Column(
        db.Boolean,
        info={
            "display_order": 1,
            "type": "radio",
            "template_options": {
                "label": "Were there any complications during the pregnancy or delivery?",
                "required": False,
                "options": [
                    {"value": True, "label": "Yes"},
                    {"value": False, "label": "No"},
                ],
            },
        },
    )
    birth_complications_description = db.Column(
        db.String,
        info={
            "display_order": 1.2,
            "type": "textarea",
            "template_options": {
                "label": "Please describe:",
                "appearance": "standard",
                "required": False,
            },
            'hide_expression': '!model.had_birth_complications',
        }
    )
    when_motor_milestones = db.Column(
        db.String,
        info={
            "display_order": 2,
            "type": "radio",
            "template_options": {
                "label": "",
                "required": False,
                "options": [
                    {"value": "early", "label": "Early"},
                    {"value": "onTime", "label": "On-time"},
                    {"value": "delayed", "label": "Delayed"},
                    {"value": "notYet", "label": "Not yet acquired"},
                ],
            },
            "expression_properties": {
                "template_options.label": '"When did " + '
                '(formState.preferredName || "Your child") + '
                '" reach their motor developmental milestones '
                '(e.g., walking, crawling, etc.)?"'
            },
        },
    )
    when_language_milestones = db.Column(
        db.String,
        info={
            "display_order": 3,
            "type": "radio",
            "template_options": {
                "label": "",
                "required": False,
                "options": [
                    {"value": "early", "label": "Early"},
                    {"value": "onTime", "label": "On-time"},
                    {"value": "delayed", "label": "Delayed"},
                    {"value": "notYet", "label": "Not yet acquired"},
                ],
            },
            "expression_properties": {
                "template_options.label": '"When did " + '
                '(formState.preferredName || "Your child") + '
                '" reach their speech/language developmental milestones '
                '(e.g., babbling, using first words and phrases)?"'
            },
        },
    )
    when_toileting_milestones = db.Column(
        db.String,
        info={
            "display_order": 4,
            "type": "radio",
            "template_options": {
                "label": "",
                "required": False,
                "options": [
                    {"value": "early", "label": "Early"},
                    {"value": "onTime", "label": "On-time"},
                    {"value": "delayed", "label": "Delayed"},
                    {"value": "notYet", "label": "Not yet acquired"},
                ],
            },
            "expression_properties": {
                "template_options.label": '"When did " + '
                '(formState.preferredName || "Your child") + '
                '" reach their toileting milestones (e.g., potty training)?"'
            },
        },
    )

    def get_field_groups(self):
        return {}


class DevelopmentalQuestionnaireSchema(ModelSchema):
    class Meta:
        model = DevelopmentalQuestionnaire
        ordered = True
        include_fk = True
