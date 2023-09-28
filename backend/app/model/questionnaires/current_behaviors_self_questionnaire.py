from flask_marshmallow.fields import Hyperlinks, URLFor
from sqlalchemy import Column, String, ARRAY

from app.model.questionnaires.current_behaviors_mixin import CurrentBehaviorsMixin
from app.schema.model_schema import ModelSchema


class CurrentBehaviorsSelfQuestionnaire(CurrentBehaviorsMixin):
    __tablename__ = "current_behaviors_self_questionnaire"

    has_academic_difficulties_desc = '"Do you have any difficulties with academics?"'
    academic_difficulty_areas_desc = '"What areas of academics are difficult for you?"'

    self_verbal_ability = Column(
        ARRAY(String),
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_field_groups(self):
        return super().get_field_groups()


class CurrentBehaviorsSelfQuestionnaireSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = CurrentBehaviorsSelfQuestionnaire
        fields = (
            "id",
            "last_updated",
            "participant_id",
            "user_id",
            "time_on_task_ms",
            "self_verbal_ability",
            "has_academic_difficulties",
            "academic_difficulty_areas",
            "academic_difficulty_other",
            "_links",
        )

    _links = Hyperlinks(
        {
            "self": URLFor("api.questionnaireendpoint", name="current_behaviors_dependent_questionnaire", id="<id>"),
        }
    )
