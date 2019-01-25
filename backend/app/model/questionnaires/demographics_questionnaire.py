import datetime

from marshmallow_sqlalchemy import ModelSchema

from app import db


class DemographicsQuestionnaire(db.Model):
    __tablename__ = 'demographics_questionnaire'
    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime, default=datetime.datetime.now)
    participant_id = db.Column(
        'participant_id',
        db.Integer,
        db.ForeignKey('stardrive_user.id')
    )
    guardian_id = db.Column(
        'guardian_id',
        db.Integer,
        db.ForeignKey('stardrive_user.id')
    )
    first_name = db.Column(
        db.String,
        info={
            'display_order': 1,
            'type': 'input',
            'template_options': {
                'label': 'First name',
                'required': True
            }
        }
    )
    middle_name = db.Column(
        db.String,
        info={
            'display_order': 2,
            'type': 'input',
            'template_options': {
                'label': 'Middle name',
                'required': False
            }
        }
    )
    last_name = db.Column(
        db.String,
        info={
            'display_order': 3,
            'type': 'input',
            'template_options': {
                'label': 'Last name',
                'required': True
            }
        }
    )
    is_first_name_preferred = db.Column(
        db.Boolean,
        info={
            'display_order': 4,
            'type': 'radio',
            'default_value': True,
            'template_options': {
                'required': False,
                'label': 'Is this the preferred name?',
                'options': [
                    {'value': True, 'label': 'Yes'},
                    {'value': False, 'label': 'No'}
                ]
            },
            'expression_properties': {
                'template_options.label': '"Is this your " + (!model.is_self ? "child\'s " : "") + "preferred name?"'
            }
        }
    )
    nickname = db.Column(
        db.String,
        info={
            'display_order': 5,
            'type': 'input',
            'template_options': {
                'label': 'Nickname',
                'required': False
            },
            'hide_expression': 'model.is_first_name_preferred'
        }
    )
    birthdate = db.Column(
        db.Date,
        info={
            'display_order': 6,
            'type': 'datepicker',
            'template_options': {
                'required': True,
                'label': 'Date of birth'
            },
            'expression_properties': {
                'template_options.label': '(model.is_self ? "Your" : (model.nickname || model.first_name || "Your child") + "\'s") + " date of birth"'
            }
        }
    )
    birth_city = db.Column(
        db.String,
        info={
            'display_order': 7,
            'type': 'input',
            'template_options': {
                'required': True,
                'label': 'City/municipality of birth'
            },
            'expression_properties': {
                'template_options.label': '(model.is_self ? "Your" : (model.nickname || model.first_name || "Your child") + "\'s") + " city/municipality of birth"'
            }
        }
    )
    birth_state = db.Column(
        db.String,
        info={
            'display_order': 8,
            'type': 'input',
            'template_options': {
                'required': True
            },
            'expression_properties': {
                'template_options.label': '(model.is_self ? "Your" : (model.nickname || model.first_name || "Your child") + "\'s") + " state of birth"'
            }
        }
    )
    birth_sex = db.Column(
        db.String,
        info={
            'display_order': 9,
            'type': 'radio',
            'template_options': {
                'required': True,
                'options': [
                    {'value': 'male', 'label': 'Male'},
                    {'value': 'female', 'label': 'Female'},
                    {'value': 'intersex', 'label': 'Intersex'}
                ]
            },
            'expression_properties': {
                'template_options.label': '(model.is_self ? "Your" : (model.nickname || model.first_name || "Your child") + "\'s") + " sex at birth"'
            }
        }
    )
    gender_identity = db.Column(
        db.String,
        info={
            'display_order': 10.1,
            'type': 'radio',
            'class_name': 'vertical-radio-group',
            'template_options': {
                'required': True,
                'options': [
                    {'value': 'male', 'label': 'Male'},
                    {'value': 'female', 'label': 'Female'},
                    {'value': 'intersex', 'label': 'Intersex'},
                    {'value': 'transgender', 'label': 'Transgender'},
                    {'value': 'other', 'label': 'Other'},
                    {'value': 'no_answer', 'label': 'Choose not to answer'}
                ]
            }
        }
    )

    gender_identity_other = db.Column(
        db.String,
        info={
            'display_order': 10.2,
            'type': 'input',
            'template_options': {
                'placeholder': 'Enter gender identity'
            },
            'hide_expression': '!(model.gender_identity && (model.gender_identity === "other"))',
        }
    )

    race_ethnicity = db.Column(
        db.String,
        info={
            'display_order': 11.1,
            'type': 'radio',
            'class_name': 'vertical-radio-group',
            'template_options': {
                'required': True,
                'options': [
                    {'value': 'raceBlack', 'label': 'Black / African / African American'},
                    {'value': 'raceAsian', 'label': 'Asian / Asian American'},
                    {'value': 'raceWhite', 'label': 'White / Caucasian'},
                    {'value': 'raceHispanic', 'label': 'Hispanic / Latin(o / a)'},
                    {'value': 'raceNative', 'label': 'Native American / Alaskan Native'},
                    {'value': 'racePacific', 'label': 'Pacific Islander'},
                    {'value': 'raceNoAnswer', 'label': 'Prefer not to answer'},
                    {'value': 'raceOther', 'label': 'Other'}
                ]
            }
        }
    )

    race_ethnicity_other = db.Column(
        db.String,
        info={
            'display_order': 11.2,
            'type': 'input',
            'template_options': {
                'placeholder': 'Enter race/ethnicity'
            },
            'hide_expression': '!(model.race_ethnicity && (model.race_ethnicity === "other"))',
        }
    )

    is_english_primary = db.Column(
        db.Boolean,
        info={
            'display_order': 12,
            'type': 'radio',
            'default': True,
            'template_options': {
                'required': False,
                'label': 'Is the primary language English?',
                'options': [
                    {'value': 'true', 'label': 'True'},
                    {'value': 'false', 'label': 'False'}
                ]
            },
            'expression_properties': {
                'template_options.label': '"Is " + (model.is_self ? "your" : (model.nickname || model.first_name || "your child") + "\'s") + " primary language English?"'
            }

        }
    )

    def get_meta(self):
        info = {
            'table': {
                'sensitive': False,
                'label': 'Demographics',
                'description': '',
            },
            'field_groups': {
                'intro': {
                    'fields': [],
                    'display_order': 0,
                    'wrappers': ['help'],
                    'template_options': {
                        'description': ''
                    },
                    'expression_properties': {
                        'template_options.description': '"Please answer the following questions about " + '
                        '(model.is_self ? "yourself" : "your child or the person with autism on whom '
                        'you are providing information") + " (* indicates required response):"'
                    }
                },
                'gender': {
                    'fields': [
                        'gender_identity',
                        'gender_identity_other'
                    ],
                    'display_order': 10,
                    'wrappers': ['card'],
                    'template_options': {
                        'label': 'Gender identity'
                    },
                    'expression_properties': {
                        'template_options.label': '(model.is_self ? "Your" : (model.nickname || model.first_name || "Your child") + "\'s") + " current gender identity '
                        '(how " + (model.is_self ? "you describe yourself)*:" : (model.nickname || model.first_name || "your child")) + '
                        '" describes themselves)*:"'
                    }
                },
                'race': {
                    'fields': [
                        'race_ethnicity',
                        'race_ethnicity_other'
                    ],
                    'display_order': 11,
                    'wrappers': ['card'],
                    'template_options': {
                        'label': 'Race/ethnicity'
                    },
                    'expression_properties': {
                        'template_options.label': '"What is " + (model.is_self ? "your" : (model.nickname || model.first_name || "your child") + "\'s") + " race/ethnicity? (select all that apply)"',
                    }
                }
            }
        }
        for c in self.metadata.tables['demographics_questionnaire'].columns:
            if c.info:
                info[c.name] = c.info
        return info


class DemographicsQuestionnaireSchema(ModelSchema):
    class Meta:
        model = DemographicsQuestionnaire
        fields = ('id', 'last_updated', 'participant_id', 'guardian_id','first_name', 'middle_name', 'last_name',
                  'nickname', 'is_first_name_preferred', 'birthdate', 'birth_city', 'birth_state', 'birth_sex',
                  'gender_identity', 'race_ethnicity', 'is_english_primary')


class DemographicsQuestionnaireMetaSchema(ModelSchema):
    class Meta:
        model = DemographicsQuestionnaire
        fields = ('get_meta',)

