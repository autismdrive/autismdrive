from marshmallow_sqlalchemy import ModelSchema

from app import db
from app.model.questionnaires.current_behaviors_mixin import CurrentBehaviorsMixin


class CurrentBehaviorsSelfQuestionnaire(db.Model, CurrentBehaviorsMixin):
    __tablename__ = "current_behaviors_self_questionnaire"

    has_academic_difficulties_desc = '"Do you have any difficulties with academics?"'
    academic_difficulty_areas_desc = '"What areas of academics are difficult for you?"'


    self_verbal_ability = db.Column(
        db.ARRAY(db.String),
        info={
            "display_order": 1,
            "type": "multicheckbox",
            "template_options": {
                "type": "array",
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

    def get_field_groups(self):
        return super().get_field_groups()


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
