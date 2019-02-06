import datetime

from marshmallow_sqlalchemy import ModelSchema

from app import db
from app.question_service import QuestionService


class EvaluationHistoryQuestionnaire(db.Model):
    __tablename__ = 'evaluation_history_questionnaire'
    __question_type__ = QuestionService.TYPE_SENSITIVE
    __estimated_duration_minutes__ = 5

    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime, default=datetime.datetime.now)
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
    self_identifies_autistic = db.Column(
        db.Boolean,
        info={
            'display_order': 1,
            'type': 'radio',
            'default_value': True,
            'template_options': {
                'label': 'Self-identify as having Autism?',
                'required': False,
                'options': [
                    {'value': True, 'label': 'Yes'},
                    {'value': False, 'label': 'No'}
                ]
            },
            'expression_properties': {
                'template_options.label': '(formState.mainModel.is_self ? "Do you" : "Does " + formState.mainModel.preferred_name) + '
                                          '" self-identify as having Autism?"'
            }
        }
    )
    has_autism_diagnosis = db.Column(
        db.Boolean,
        info={
            'display_order': 2,
            'type': 'radio',
            'default_value': True,
            'template_options': {
                'label': 'Formal diagnosis of Autism?',
                'required': True,
                'options': [
                    {'value': True, 'label': 'Yes'},
                    {'value': False, 'label': 'No'}
                ]
            },
            'expression_properties': {
                'template_options.label': '(formState.mainModel.is_self ? "Have you" : "Has " + formState.mainModel.preferred_name) + '
                                          '" been formally diagnosed with Autism Spectrum Disorder?"'
            }
        }
    )
    years_old_at_first_diagnosis = db.Column(
        db.Integer,
        info={
            'display_order': 3,
            'type': 'input',
            'template_options': {
                'label': 'Years old at first diagnosis?',
                'required': True
            },
            'expression_properties': {
                'template_options.label': '"How old " + (formState.mainModel.is_self ? "were you " : "was " + formState.mainModel.preferred_name) + '
                                          '" when " + (formState.mainModel.is_self ? "you " : "they ") + " were first diagnosed'
                                          ' with ASD?"'
            }
        }
    )
    who_diagnosed = db.Column(
        db.String,
        info={
            'display_order': 4,
            'type': 'select',
            'template_options': {
                'label': 'Who diagnosed?',
                'required': True,
                'options': [
                    {'value': 'pediatrician', 'label': 'Pediatrician/Developmental pediatrician/Primary care physician'},
                    {'value': 'psychiatrist', 'label': 'Psychiatrist'},
                    {'value': 'neurologist', 'label': 'Neurologist'},
                    {'value': 'psychologist', 'label': 'Psychologist'},
                    {'value': 'healthTeam', 'label': 'Team of healthcare professionals'},
                    {'value': 'diagnosisOther', 'label': 'Other'}
                ]
            },
            'expression_properties': {
                'template_options.label': '"Who first diagnosed " + (formState.mainModel.is_self ? "you" : formState.mainModel.preferred_name) + '
                                          '" with ASD?"'
            }
        }
    )
    who_diagnosed_other = db.Column(
        db.String,
        info={
            'display_order': 5,
            'type': 'input',
            'template_options': {
                'placeholder': 'First diagnosed by'
            },
            'hide_expression': '!(formState.mainModel.who_diagnosed && (formState.mainModel.who_diagnosed === "diagnosisOther"))',
        }
    )
    where_diagnosed = db.Column(
        db.String,
        info={
            'display_order': 6,
            'type': 'select',
            'template_options': {
                'label': 'Where diagnosed?',
                'required': True,
                'options': [
                    {'value': '1uvaDp', 'label': 'UVA Developmental Pediatrics or UVA Child Development and Rehabilitation Center (formerly Kluge Children\'s Rehabilitation Center, KCRC)'},
                    {'value': '2sjcCse', 'label': 'Sheila Johnson Center or Curry School of Education'},
                    {'value': '3via', 'label': 'Virginia Institute of Autism (VIA)'},
                    {'value': '4school', 'label': 'School system'},
                    {'value': '5evms', 'label': 'Eastern Virginia Medical School (EVMS)'},
                    {'value': '6chkd', 'label': 'Children’s Hospital of the Kings Daughters (CHKD)'},
                    {'value': '7cas', 'label': 'Commonwealth Autism Services (Virginia Commonwealth University)'},
                    {'value': '8vtAc', 'label': 'Virginia Tech Autism Clinic'},
                    {'value': '9gmu', 'label': 'George Mason University'},
                    {'value': '10brAac', 'label': 'Blue Ridge Autism and Achievement Center'},
                    {'value': '11cnh', 'label': 'Children’s National Hospital'},
                    {'value': '12kki', 'label': 'Center for Autism and Related Disorders (Kennedy Krieger Institute)'},
                    {'value': '13vcu', 'label': 'Children’s Hospital of Richmond (VCU)'},
                    {'value': '14vtc', 'label': 'Virginia Tech Carilion'},
                    {'value': '15centra', 'label': 'CENTRA Lynchburg'},
                    {'value': '16apg', 'label': 'Alexandria Pediatrician Group'},
                    {'value': '17cc', 'label': 'Carilion Clinic'},
                    {'value': '18mwh', 'label': 'Mary Washington Hospital'},
                    {'value': '19rna', 'label': 'Roanoke Neurological Associates'},
                    {'value': '20ruac', 'label': 'Radford University Autism Center'},
                    {'value': '21rcim', 'label': 'Rimland Center for Integrative Medicine'},
                    {'value': '22occa', 'label': 'One Child Center for Autism (Williamsburg)'},
                    {'value': '23inova', 'label': 'INOVA Health System'},
                    {'value': '24sentara', 'label': 'Sentara Health System'},
                    {'value': '25psv', 'label': 'Pediatric Specialists of Virginia'},
                    {'value': 'diagnosisOther', 'label': 'Other'}
                ]
            },
            'expression_properties': {
                'template_options.label': '"Where did " + (formState.mainModel.is_self ? "you" : formState.mainModel.preferred_name) + '
                                          '" receive this diagnosis?"'
            }
        }
    )
    where_diagnosed_other = db.Column(
        db.String,
        info={
            'display_order': 7,
            'type': 'input',
            'template_options': {
                'placeholder': 'Where diagnosed?'
            },
            'hide_expression': '!(formState.mainModel.where_diagnosed && (formState.mainModel.where_diagnosed === "diagnosisOther"))',
        }
    )
    partner_centers_evaluation = db.Column(
        db.String,
        info={
            'display_order': 8.1,
            'type': 'multicheckbox',
            'class_name': 'vertical-checkbox-group',
            'template_options': {
                'required': True,
                'options': [
                    {'value': 'uva', 'label': 'UVA Developmental Pediatrics or UVA Child Development and Rehabilitation Center (formerly Kluge Children\'s Rehabilitation Center, KCRC)'},
                    {'value': 'sjc', 'label': 'Sheila Johnson Center or Curry School of Education'},
                    {'value': 'via', 'label': 'Virginia Institute of Autism (VIA)'},
                    {'value': 'fc', 'label': 'Faison Center'},
                    {'value': 'inova', 'label': 'INOVA Health System'}
                ]
            }
        }
    )
    gives_permission_to_link_evaluation_data = db.Column(
        db.Boolean,
        info={
            'display_order': 9,
            'type': 'radio',
            'default_value': True,
            'template_options': {
                'label': 'Permission to link?',
                'required': True,
                'options': [
                    {'value': True, 'label': 'Yes'},
                    {'value': False, 'label': 'No'}
                ]
            },
            'expression_properties': {
                'template_options.label': '"Do we have your permission to link " + (!formState.mainModel.is_self ? "your" : formState.mainModel.preferred_name + "\'s") + '
                                          '" evaluation data to the UVa Autism Database?"'
                                         },
            'hide_expression': '!(formState.mainModel.partner_centers_evaluation)',
        }
    )
    has_iq_test = db.Column(
        db.Boolean,
        info={
            'display_order': 10,
            'type': 'radio',
            'default_value': True,
            'template_options': {
                'label': 'IQ or intelligence test?',
                'required': False,
                'options': [
                    {'value': True, 'label': 'Yes'},
                    {'value': False, 'label': 'No'}
                ]
            },
            'expression_properties': {
                'template_options.label': '(formState.mainModel.is_self ? "Have you" : "Has " + formState.mainModel.preferred_name) + '
                                          '" been given an IQ or intelligence test?"'
            }
        }
    )
    recent_iq_score = db.Column(
        db.Integer,
        info={
            'display_order': 11,
            'type': 'input',
            'template_options': {
                'placeholder': 'IQ score'
            },
            'expression_properties': {
                'template_options.label': '"What was " + (formState.mainModel.is_self ? "your" : formState.mainModel.preferred_name + "\'s") + '
                                          '" most recent IQ score?"'
            },
            'hide_expression': '!(formState.mainModel.has_iq_test)'
        }
    )

    def get_meta(self):
        info = {
            'table': {
                'sensitive': True,
                'label': 'Evaluation History',
                'description': '',
            },
            'field_groups': {
                'partner_centers': {
                    'fields': [
                        'partner_centers_evaluation'
                    ],
                    'display_order': 8,
                    'wrappers': ['card'],
                    'template_options': {
                        'label': 'Evaluation at partner institution?'
                    },
                    'expression_properties': {
                        'template_options.label': '(formState.mainModel.is_self ? "Have you" : "Has " + formState.mainModel.preferred_name) + '
                        '" ever been evaluated at any of the following centers?"'
                    }
                }
            }
        }
        for c in self.metadata.tables['evaluation_history_questionnaire'].columns:
            if c.info:
                info[c.name] = c.info
        return info


class EvaluationHistoryQuestionnaireSchema(ModelSchema):
    class Meta:
        model = EvaluationHistoryQuestionnaire
        fields = ('id', 'last_updated', 'participant_id', 'user_id', 'self_identifies_autistic',
                  'has_autism_diagnosis', 'years_old_at_first_diagnosis', 'who_diagnosed', 'who_diagnosed_other',
                  'where_diagnosed', 'where_diagnosed_other', 'partner_centers_evaluation',
                  'gives_permission_to_link_evaluation_data', 'has_iq_test', 'recent_iq_score')


class EvaluationHistoryQuestionnaireMetaSchema(ModelSchema):
    class Meta:
        model = EvaluationHistoryQuestionnaire
        fields = ('get_meta',)
