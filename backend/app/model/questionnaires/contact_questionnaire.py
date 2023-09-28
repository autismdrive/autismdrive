from flask_marshmallow.fields import Hyperlinks, URLFor
from sqlalchemy import func, Column, Integer, String, ForeignKey, DateTime, Boolean, BigInteger

from app.database import Base
from app.export_service import ExportService
from app.schema.model_schema import ModelSchema


class ContactQuestionnaire(Base):
    __tablename__ = "contact_questionnaire"
    __label__ = "Contact Information"
    __question_type__ = ExportService.TYPE_IDENTIFYING
    __estimated_duration_minutes__ = 5
    marketing_other_hide_expression = '!(model.marketing_channel && (model.marketing_channel === "other"))'

    id = Column(Integer, primary_key=True)
    last_updated = Column(DateTime(timezone=True), default=func.now())
    time_on_task_ms = Column(BigInteger, default=0)

    participant_id = Column("participant_id", Integer, ForeignKey("stardrive_participant.id"))
    user_id = Column("user_id", Integer, ForeignKey("stardrive_user.id"))
    phone = Column(
        String,
        info={
            "display_order": 1.1,
            "type": "input",
            "template_options": {
                "required": True,
                "type": "tel",
                "label": "Preferred number",
                "description": "(including area code)",
                "placeholder": "555-555-5555",
            },
            "validators": {"validation": ["phone"]},
        },
    )
    phone_type = Column(
        String,
        info={
            "display_order": 1.2,
            "type": "radio",
            "template_options": {
                "label": "Type",
                "placeholder": "",
                "description": "",
                "required": True,
                "options": [
                    {"value": "home", "label": "Home"},
                    {"value": "cell", "label": "Cell"},
                ],
            },
        },
    )
    can_leave_voicemail = Column(
        Boolean,
        info={
            "display_order": 1.3,
            "type": "radio",
            "template_options": {
                "label": "Leave voicemail?",
                "description": "Is it okay to leave a voicemail message at this number?",
                "required": False,
                "options": [
                    {"value": True, "label": "Yes"},
                    {"value": False, "label": "No"},
                ],
            },
        },
    )
    contact_times = Column(
        String,
        info={
            "display_order": 1.4,
            "type": "textarea",
            "template_options": {
                "label": "Best times to call",
                "description": "Some research studies might involve a phone call. "
                "If that’s the case, when would be the best times "
                "of day to call you?",
                "required": False,
            },
        },
    )
    email = Column(
        String,
        info={
            "display_order": 2,
            "type": "input",
            "template_options": {
                "label": "Email",
                "type": "email",
                "required": True,
            },
            "validators": {"validation": ["email"]},
        },
    )
    street_address = Column(
        String,
        info={
            "display_order": 3.1,
            "type": "input",
            "template_options": {"label": "Street Address", "required": True},
        },
    )
    city = Column(
        String,
        info={
            "display_order": 3.2,
            "type": "input",
            "template_options": {"label": "Town/City", "required": False},
        },
    )
    state = Column(
        String,
        info={
            "display_order": 3.3,
            "type": "input",
            "template_options": {"label": "State", "required": False},
        },
    )
    zip = Column(
        Integer,
        info={
            "display_order": 3.4,
            "type": "input",
            "template_options": {
                "type": "number",
                "label": "Zip",
                "max": 99999,
                "min": 0,
                "pattern": "\\d{5}",
                "required": True,
            },
        },
    )
    marketing_channel = Column(
        String,
        info={
            "display_order": 4.1,
            "type": "select",
            "template_options": {
                "label": "",
                "placeholder": "Please select how you heard about us",
                "description": "",
                "required": True,
                "options": [
                    {"value": "internet", "label": "Internet"},
                    {"value": "health_care_provider", "label": "Health care provider (doctor, speech therapist, etc)"},
                    {"value": "school", "label": "Teacher or school"},
                    {"value": "word_of_mouth", "label": "Word of mouth (friend, family member, etc)"},
                    {"value": "community_event", "label": "Community event (autism walk, resource fair, etc.)"},
                    {"value": "media", "label": "Television or radio (CNN, NPR, local news, etc.)"},
                    {"value": "research_study", "label": "While participating in a research study"},
                    {"value": "other", "label": "Other"},
                ],
            },
        },
    )
    marketing_other = Column(
        String,
        info={
            "display_order": 4.2,
            "type": "input",
            "template_options": {
                "label": "Please specify how you heard about us",
                "required": True,
            },
            "hide_expression": marketing_other_hide_expression,
            "expression_properties": {"template_options.required": "!" + marketing_other_hide_expression},
        },
    )

    def get_field_groups(self):
        return {
            "phone_group": {
                "fields": [
                    "phone",
                    "phone_type",
                    "can_leave_voicemail",
                    "contact_times",
                ],
                "display_order": 1,
                "wrappers": ["card"],
                "template_options": {"label": "Phone"},
            },
            "address": {
                "fields": ["street_address", "city", "state", "zip"],
                "display_order": 3,
                "wrappers": ["card"],
                "template_options": {"label": "Address"},
            },
            "email": {
                "fields": ["email"],
                "display_order": 4,
                "wrappers": ["card"],
                "template_options": {"label": "Email"},
            },
            "marketing": {
                "fields": ["marketing_channel", "marketing_other"],
                "display_order": 5,
                "wrappers": ["card"],
                "template_options": {"label": "How did you hear about us?"},
            },
        }


class ContactQuestionnaireSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = ContactQuestionnaire

    _links = Hyperlinks({"self": URLFor("api.questionnaireendpoint", name="contact_questionnaire", id="<id>")})
