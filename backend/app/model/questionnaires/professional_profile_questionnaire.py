import datetime

from dateutil.tz import tzutc
from marshmallow_sqlalchemy import ModelSchema
from sqlalchemy import func

from app import db, ma
from app.export_service import ExportService


class ProfessionalProfileQuestionnaire(db.Model):
    __tablename__ = 'professional_profile_questionnaire'
    __label__ = "Professional Profile"
    __question_type__ = ExportService.TYPE_UNRESTRICTED
    __estimated_duration_minutes__ = 2
    professional_identity_other_hide_expression = '!(model.professional_identity && model.professional_identity.includes("profOther"))'
    learning_interests_other_hide_expression = '!(model.learning_interests && model.learning_interests.includes("learnOther"))'

    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime(timezone=True), default=func.now())
    time_on_task_ms = db.Column(db.BigInteger, default=0)

    participant_id = db.Column(
        'participant_id',
        db.Integer,
        db.ForeignKey('stardrive_participant.id')
    )
    user_id = db.Column(
        'user_id',
        db.Integer,
        db.ForeignKey('stardrive_user.id')
    )
    purpose = db.Column(
        db.String,
        info={
            "display_order": 1,
            "type": "select",
            "template_options": {
                "label": 'For what purposes are you interested in accessing the Autism DRIVE?',
                "placeholder": "Please select",
                "options": [
                    {"value": "profResources", "label": "To learn more about Autism and Autism Resources available"},
                    {"value": "profResearch", "label": "To learn about and engage in research projects"},
                    {"value": "profResourcesAndResearch", "label": "Both"},
                ],
            },
        },
    )
    professional_identity = db.Column(
        db.ARRAY(db.String),
        info={
            "display_order": 2.1,
            "type": "multicheckbox",
            "template_options": {
                "type": "array",
                "required": False,
                "options": [
                    {"value": "admin", "label": "Administrator"},
                    {"value": "adaptive", "label": "Adaptive Physical Education Specialist or Teacher"},
                    {"value": "artTher", "label": "Art Therapist"},
                    {"value": "behaviorAnalyst", "label": "Behavior Analyst"},
                    {"value": "audio", "label": "Audiologist"},
                    {"value": "behaviorTher", "label": "Behavior Therapist (e.g., Behavior Support Specialist, RBT)"},
                    {"value": "caseManag", "label": "Case Manager"},
                    {"value": "counselor", "label": "Counselor"},
                    {"value": "diet", "label": "Dietician"},
                    {"value": "directSupp", "label": "Direct Support Professional"},
                    {"value": "dramaTher", "label": "Drama Therapist"},
                    {"value": "earlyInter", "label": "Early Intervention Specialist/Early Intervention Special Educator"},
                    {"value": "inHomeCare", "label": "In-home caregiver"},
                    {"value": "interp", "label": "Interpreter"},
                    {"value": "jobCoach", "label": "Job coach"},
                    {"value": "musicTher", "label": "Music Therapist"},
                    {"value": "nursing", "label": "Nursing professional"},
                    {"value": "OccupatTher", "label": "Occupational Therapist"},
                    {"value": "paraprof", "label": "Paraprofessional"},
                    {"value": "physician", "label": "Physician"},
                    {"value": "physicalTher", "label": "Physical Therapist"},
                    {"value": "psychologist", "label": "Psychologist"},
                    {"value": "psychiatrist", "label": "Psychiatrist"},
                    {"value": "recInstruct", "label": "Recreational instructor"},
                    {"value": "rehabTher", "label": "Rehabilitation Therapist"},
                    {"value": "researcher", "label": "Researcher or Research Assistant"},
                    {"value": "socialWork", "label": "Social Worker"},
                    {"value": "speechLangPath", "label": "Speech Language Pathologist"},
                    {"value": "supportCoord", "label": "Support Coordinator or Specialist"},
                    {"value": "teacherGenEd", "label": "Teacher or teaching assistant, General Education"},
                    {"value": "teacherSpecEd", "label": "Teacher or teaching assistant, Special Education"},
                    {"value": "techSpec", "label": "Technology Specialist"},
                    {"value": "transitCoor", "label": "Transition coordinator"},
                    {"value": "vocationRehab", "label": "Vocational Rehabilitation Specialist"},
                    {"value": "profNoAnswer", "label": "Prefer not to answer"},
                    {"value": "profOther", "label": "Other"},
                ],
            },
        },
    )
    professional_identity_other = db.Column(
        db.String,
        info={
            "display_order": 2.2,
            "type": "input",
            "template_options": {
                "label": "Describe professional identity",
                "appearance": "standard",
                "required": True,
            },
            "hide_expression": professional_identity_other_hide_expression,
            "expression_properties": {
                "template_options.required": '!' + professional_identity_other_hide_expression
            }
        },
    )
    learning_interests = db.Column(
        db.ARRAY(db.String),
        info={
            "display_order": 3.1,
            "type": "multicheckbox",
            "template_options": {
                "type": "array",
                "required": False,
                "options": [
                    {"value": "afterSchoolProg", "label": "After-school programs"},
                    {"value": "appliedBehav", "label": "Applied Behavior Analysis (ABA) services"},
                    {"value": "assistiveTech", "label": "Assistive technology and devices"},
                    {"value": "behavManag", "label": "Behavior management"},
                    {"value": "caseManag", "label": "Case management"},
                    {"value": "collegeTransi", "label": "College/University transitions"},
                    {"value": "commAides", "label": "Communication aides"},
                    {"value": "diagServ", "label": "Diagnostic services"},
                    {"value": "eduPract", "label": "Educational practices"},
                    {"value": "effectTher", "label": "Effective therapies"},
                    {"value": "fundingOpt", "label": "Funding options"},
                    {"value": "genCond", "label": "Genetic conditions related to autism"},
                    {"value": "indivEdPlan", "label": "Individualized education plans"},
                    {"value": "indivFamSupp", "label": "Individualized Family Support Plans"},
                    {"value": "indivServPlan", "label": "Individualized Service Plans"},
                    {"value": "insuranceCov", "label": "Insurance coverage"},
                    {"value": "medCondit", "label": "Medical conditions related to autism"},
                    {"value": "mentalHealth", "label": "Mental health"},
                    {"value": "news", "label": "News and current advances in the field"},
                    {"value": "parentAdvoc", "label": "Parent advocacy"},
                    {"value": "pharmTreat", "label": "Pharmacological treatments"},
                    {"value": "resOpAdult", "label": "Residential options for adults with autism"},
                    {"value": "resOpChild", "label": "Residential options for children with autism"},
                    {"value": "therapies", "label": "Therapies"},
                    {"value": "transitionSupp", "label": "Transition-based supports"},
                    {"value": "learnNoAnswer", "label": "Prefer not to answer"},
                    {"value": "learnOther", "label": "Other"},
                ],
            },
        },
    )
    learning_interests_other = db.Column(
        db.String,
        info={
            "display_order": 3.2,
            "type": "input",
            "template_options": {
                "label": "Enter other interests",
                "appearance": "standard",
                "required": True,
            },
            "hide_expression": learning_interests_other_hide_expression,
            "expression_properties": {
                "template_options.required": '!' + learning_interests_other_hide_expression
            }
        },
    )
    currently_work_with_autistic = db.Column(
        db.Boolean,
        info={
            "display_order": 4,
            "type": "radio",
            "template_options": {
                "label": "Do you currently work with a person or people who have autism?",
                "required": False,
                "options": [
                    {"value": True, "label": "Yes"},
                    {"value": False, "label": "No"},
                ],
            },
        },
    )
    previous_work_with_autistic = db.Column(
        db.Boolean,
        info={
            "display_order": 4,
            "type": "radio",
            "template_options": {
                "label": "Did you previously work with someone/people who had autism? ",
                "required": False,
                "options": [
                    {"value": True, "label": "Yes"},
                    {"value": False, "label": "No"},
                ],
            },
        },
    )
    length_work_with_autistic = db.Column(
        db.String,
        info={
            "display_order": 5,
            "type": "input",
            "template_options": {
                "label": "In total, how long have you worked with someone/people who have autism? ",
                "required": False
            },
        },
    )

    def get_field_groups(self):
        return {
                "professional_identity": {
                    "fields": ["professional_identity", "professional_identity_other"],
                    "display_order": 2,
                    "wrappers": ["card"],
                    "template_options": {
                        "label": 'I am a(n):'
                    },
                },
                "learning_interests": {
                    "fields": ["learning_interests", "learning_interests_other"],
                    "display_order": 3,
                    "wrappers": ["card"],
                    "template_options": {
                        "label": 'What topics or areas are you interested in learning about? '
                    },
                },
        }


class ProfessionalProfileQuestionnaireSchema(ModelSchema):
    class Meta:
        model = ProfessionalProfileQuestionnaire
        ordered = True
        include_fk = True
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.questionnaireendpoint', name='professional_profile_questionnaire', id='<id>'),
    })