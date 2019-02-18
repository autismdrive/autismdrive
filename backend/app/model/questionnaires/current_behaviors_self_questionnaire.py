import datetime

from marshmallow_sqlalchemy import ModelSchema

from app import db
from app.question_service import QuestionService


class CurrentBehaviorsSelfQuestionnaire(db.Model):
    __tablename__ = "current_behaviors_self_questionnaire"
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
    self_verbal_ability = db.Column(
        db.String,
        info={
            "display_order": 1,
            "type": "multicheckbox",
            "class_name": "vertical-checkbox-group",
            "template_options": {
                "label": "How do you best communicate?",
                "required": False,
                "options": [
                    {"value": "verbal", "label": "Verbally"},
                    {"value": "nonVerbal", "label": "Non-verbally"},
                    {
                        "value": "AACsystem",
                        "label": "An alternative and augmentative communication (AAC) system "
                        "(e.g., Picture exchange, sign language, ipad, etc)",
                    },
                ],
            },
        },
    )
    has_academic_difficulties = db.Column(
        db.Boolean,
        info={
            "display_order": 3,
            "type": "radio",
            "default_value": True,
            "template_options": {
                "label": "Do you have any difficulties with academics?",
                "required": False,
                "options": [
                    {"value": True, "label": "Yes"},
                    {"value": False, "label": "No"},
                ],
            },
        },
    )
    academic_difficulty_areas = db.Column(
        db.String,
        info={
            "display_order": 4,
            "type": "multicheckbox",
            "class_name": "vertical-checkbox-group",
            "template_options": {
                "label": "What areas of academics are difficult for you?",
                "required": True,
                "options": [
                    {"value": "math", "label": "Math"},
                    {"value": "reading", "label": "Reading"},
                    {"value": "writing", "label": "Writing"},
                    {"value": "other", "label": "Other"},
                ],
            },
        },
    )
    academic_difficulty_other = db.Column(
        db.String,
        info={
            "display_order": 4.2,
            "type": "input",
            "template_options": {
                "placeholder": "Enter area of academic difficulty"
            },
            "hide_expression": "!(model.academic_difficulty_areas && (model.academic_difficulty_areas.other))",
        },
    )

    def get_meta(self):
        info = {
            "table": {
                "sensitive": False,
                "label": "Current Behaviors",
                "description": "",
            }
        }
        for c in self.metadata.tables[
            "current_behaviors_self_questionnaire"
        ].columns:
            if c.info:
                info[c.name] = c.info
        return info


class CurrentBehaviorsSelfQuestionnaireSchema(ModelSchema):
    class Meta:
        model = CurrentBehaviorsSelfQuestionnaire
        fields = (
            "id",
            "last_updated",
            "participant_id",
            "user_id",
            "self_verbal_ability",
            "has_academic_difficulties",
            "academic_difficulty_areas",
            "academic_difficulty_other",
        )


class CurrentBehaviorsSelfQuestionnaireMetaSchema(ModelSchema):
    class Meta:
        model = CurrentBehaviorsSelfQuestionnaire
        fields = ("get_meta",)
