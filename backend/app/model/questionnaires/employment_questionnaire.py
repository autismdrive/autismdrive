from flask_marshmallow.fields import Hyperlinks, URLFor
from sqlalchemy import func, Column, Integer, String, ForeignKey, DateTime, Boolean, BigInteger

from app.database import Base
from app.export_service import ExportService
from app.schema.model_schema import ModelSchema


class EmploymentQuestionnaire(Base):
    __tablename__ = "employment_questionnaire"
    __label__ = "Employment"
    __question_type__ = ExportService.TYPE_UNRESTRICTED
    __estimated_duration_minutes__ = 2

    id = Column(Integer, primary_key=True)
    last_updated = Column(DateTime(timezone=True), default=func.now())
    time_on_task_ms = Column(BigInteger, default=0)

    participant_id = Column("participant_id", Integer, ForeignKey("stardrive_participant.id"))
    user_id = Column("user_id", Integer, ForeignKey("stardrive_user.id"))
    is_currently_employed = Column(
        Boolean,
        info={
            "display_order": 1.1,
            "type": "radio",
            "template_options": {
                "label": "Are you currently employed?",
                "required": False,
                "options": [{"value": True, "label": "Yes"}, {"value": False, "label": "No"}],
            },
        },
    )
    employment_capacity = Column(
        String,
        info={
            "display_order": 1.2,
            "type": "radio",
            "default_value": "n/a",
            "template_options": {
                "label": "In what capacity?",
                "required": False,
                "options": [
                    {"value": "fullTime", "label": "Full time (> 35 hours per week)"},
                    {"value": "partTime", "label": "Part time"},
                ],
            },
            "hide_expression": "!(model.is_currently_employed)",
        },
    )
    has_employment_support = Column(
        String,
        info={
            "display_order": 2,
            "type": "radio",
            "template_options": {
                "label": "Receiving Support?",
                "description": "Do you currently receive supports to help you work successfully, such as job coaching "
                "or vocational training?",
                "required": False,
                "options": [
                    {"value": "yes", "label": "Yes"},
                    {"value": "interested", "label": "No, but I am interested"},
                    {"value": "no", "label": "No"},
                ],
            },
        },
    )

    def get_field_groups(self):
        return {}


class EmploymentQuestionnaireSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = EmploymentQuestionnaire

    _links = Hyperlinks(
        {
            "self": URLFor("api.questionnaireendpoint", name="employment_questionnaire", id="<id>"),
        }
    )
