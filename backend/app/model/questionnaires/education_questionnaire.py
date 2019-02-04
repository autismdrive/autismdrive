import datetime

from marshmallow_sqlalchemy import ModelSchema

from app import db


class EducationQuestionnaire(db.Model):
    __tablename__ = 'education_questionnaire'
    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime, default=datetime.datetime.now)
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
    attends_school = db.Column(
        db.Boolean,
        info={
            'display_order': 1,
            'type': 'radio',
            'default_value': True,
            'template_options': {
                'label': 'Attends school',
                'required': False,
                'options': [
                    {'value': True, 'label': 'Yes'},
                    {'value': False, 'label': 'No'}
                ]
            },
            'expression_properties': {
                'template_options.label': '(model.is_self ? "Do you attend an academic program, such as a school, '
                                          'college, or university?" : '
                                          '"Does " + (model.nickname || model.first_name || "your child") + '
                                          '" attend school?")'
            }
        }
    )
    school_name = db.Column(
        db.String,
        info={
            'display_order': 2,
            'type': 'input',
            'template_options': {
                'label': 'What is the name of the school or program?',
                'required': False
            }
        }
    )
    school_type = db.Column(
        db.String,
        info={
            'display_order': 2,
            'type': 'input',
            'template_options': {
                'label': 'What type of school?',
                'required': False
            },
            'expression_properties': {
                'template_options.label': '(model.is_self ? "Is this a public school, private school, or are you '
                                          'home schooled?" : '
                                          '"Is " + (model.nickname || model.first_name || "your child") + '
                                          '"\'s school:")'
            }
        }
    )
    self_placement = db.Column(
        db.String,
        info={
            'display_order': 1,
            'type': 'radio',
            'template_options': {
                'label': 'What type of program is it?',
                'required': False,
                'options': [
                    {'value': 'highSchool', 'label': 'High school, please specify CURRENT GRADE below'},
                    {'value': 'vocational', 'label': 'Vocational school where I am learning job or life skills'},
                    {'value': 'college', 'label': 'College/university'},
                    {'value': 'graduate', 'label': 'Graduate school'},
                    {'value': 'schoolOther', 'label': 'Other'}
                ]
            }
        }
    )
    dependent_placement = db.Column(
        db.String,
        info={
            'display_order': 1,
            'type': 'radio',
            'template_options': {
                'label': '"What is " + (model.nickname || model.first_name || "your child") + "\'s '
                         'current grade/school placement?"',
                'required': False,
                'options': [
                    {'value': 'daycare', 'label': 'Daycare center'},
                    {'value': 'preschool', 'label': 'Preschool'},
                    {'value': 'kindergarten', 'label': 'Kindergarten'},
                    {'value': '1through12', 'label': '1st through 12th grade, please specify CURRENT GRADE below'},
                    {'value': 'vocational', 'label': 'Vocational school where I am learning job or life skills'},
                    {'value': 'college', 'label': 'College/university'},
                    {'value': 'graduate', 'label': 'Graduate school'},
                    {'value': 'schoolOther', 'label': 'Other'}
                ]
            }
        }
    )
    placement_other = db.Column(
        db.String,
        info={
            'display_order': 3.2,
            'type': 'input',
            'template_options': {
                'placeholder': 'Enter school placement'
            },
            'hide_expression': '!((model.dependent_placement && (model.dependent_placement.schoolOther)) || '
                               '(model.self_placement && (model.self_placement.schoolOther)))',
        }
    )
    current_grade = db.Column(
        db.String,
        info={
            'display_order': 3.2,
            'type': 'input',
            'template_options': {
                'placeholder': 'Enter grade'
            },
            'hide_expression': '!((model.dependent_placement && (model.dependent_placement.1through12)) || '
                               '(model.self_placement && (model.self_placement.highSchool)))',
        }
    )
    school_services = db.Column(
        db.String,
        info={
            'display_order': 1,
            'type': 'radio',
            'template_options': {
                'label': 'School services',
                'required': False,
                'options': [
                    {'value': '504mod', 'label': '504 Modification Plan'},
                    {'value': 'iep', 'label': 'Individualized Education Program (IEP)'},
                    {'value': '1:1aide', 'label': '1:1 aide or paraprofessional in classroom'},
                    {'value': 'partTimeInstruction', 'label': 'Part-time specialized instruction in a resource room or special education classroom'},
                    {'value': 'fullTimeInstruction', 'label': 'Full-time specialized instruction in a resource room or special education classroom'},
                    {'value': 'specializedSchool', 'label': 'Specialized school for special learning needs'},
                    {'value': 'dayTreatment', 'label': 'Day treatment or residential center'},
                    {'value': 'disabilitySupports', 'label': 'Disability supports services (at college/vocational school)'},
                    {'value': 'servicesOther', 'label': 'Other'}
                ]
            },
            'expression_properties': {
                'template_options.label': '"Please check the following services " + (model.is_self ? "you currently '
                                          'receive through your academic program (check all that apply):" : '
                                          '(model.nickname || model.first_name || "your child") + '
                                          '" currently receives in school (check all that apply):")'
            }
        }
    )
    school_services_other = db.Column(
        db.String,
        info={
            'display_order': 3.2,
            'type': 'input',
            'template_options': {
                'placeholder': 'Enter service'
            },
            'hide_expression': '!(model.school_services && (model.schoolServices.servicesOther))',
        }
    )

    def get_meta(self):
        info = {
            'table': {
                'sensitive': False,
                'label': 'Education',
                'description': '',
            }
        }
        for c in self.metadata.tables['education_questionnaire'].columns:
            if c.info:
                info[c.name] = c.info
        return info


class EducationQuestionnaireSchema(ModelSchema):
    class Meta:
        model = EducationQuestionnaire
        fields = ('id', 'last_updated', 'participant_id', 'user_id', 'attends_school', 'school_name', 'school_type',
                  'self_placement', 'dependent_placement', 'placement_other', 'current_grade', 'school_services',
                  'school_services_other')


class EducationQuestionnaireMetaSchema(ModelSchema):
    class Meta:
        model = EducationQuestionnaire
        fields = ('get_meta',)

