import datetime

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
            'type': 'input',
            'template_options': {
                'label': 'Last name*',
                'required': True
            }
        }
    )
    is_first_name_preferred = db.Column(
        db.Boolean,
        info={
            'type': 'radio',
            'template_options': {
                'required': False
            },
            'self_template_label': 'Is this your preferred name/nick name?',
            'guardian_template_label': 'Is this your child’s preferred name/nick name?'
        }
    )
    nickname = db.Column(
        db.String,
        info={
            'type': 'input',
            'template_options': {
                'label': 'Preferred name or nickname',
                'required': False
            },
            'hide_expression': '!model.is_first_name_preferred',
            'hide_label': 'Enter nickname'
        }
    )
    birthdate = db.Column(
        db.Date,
        info={
            'type': 'datepicker',
            'template_options': {
                'required': True
            },
            'self_template_label': 'Your Date of Birth*',
            'guardian_template_label': 'model.first_name + "\'s Date of Birth*"'
        }
    )
    birth_city = db.Column(
        db.String,
        info={
            'type': 'input',
            'template_options': {
                'required': True
            },
            'self_template_label': 'Your City/municipality of birth*',
            'guardian_template_label': 'model.first_name + "\'s City/municipality of birth*"'
        }
    )
    birth_state = db.Column(
        db.String,
        info={
            'type': 'input',
            'template_options': {
                'required': True
            },
            'self_template_label': 'Your state of birth*',
            'guardian_template_label': 'model.first_name + "\'s state of birth*"'
        }
    )
    birth_sex = db.Column(
        db.String,
        info={
            'type': 'radio',
            'template_options': {
                'required': True
            },
            'self_template_label': 'Your sex at birth*',
            'guardian_template_label': 'model.first_name + "\'s sex at birth*"',
            'options': [{'value': 'male', 'label': 'Male'},
                        {'value': 'female', 'label': 'Female'},
                        {'value': 'intersex', 'label': 'Intersex'}
                        ]
        }
    )
    gender_identity = db.Column(
        db.String,
        info={
            'type': 'radio',
            'template_options': {
                'required': True
            },
            'self_template_label': 'Your current gender identity (how you describe yourself)*:',
            'guardian_template_label': 'model.first_name + "\'s current gender identity (how " + model.first_name + '
                                       '" describes themselves)*:"',
            'options': [{'value': 'male', 'label': 'Male'},
                        {'value': 'female', 'label': 'Female'},
                        {'value': 'intersex', 'label': 'Intersex'},
                        {'value': 'transgender', 'label': 'Transgender'},
                        {'value': 'other', 'label': 'Other'},
                        {'value': 'no_answer', 'label': 'Choose not to answer'}
                        ]
            }
    )

    gender_identity_other = db.Column(
        db.String,
        info={
            'display_order': 1,
            'type': 'input',
            'template_options': {
                'placeholder': 'Enter gender identity'
            },
            'hideExpression': '!(model.gender_identity && (model.gender_identity === "other"))',
        }
    )

    race_ethnicity = db.Column(
        db.String,
        info={
            'type': 'radio',
            'template_options': {
                'required': True
            },
            'self_template_label': 'What is your race/ethnicity? (select all that apply)*',
            'guardian_template_label': '"What is " + model.first_name + "\'s race/ethnicity?* (select all that apply)"',
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
    )

    race_ethnicity_other = db.Column(
        db.String,
        info={
            'display_order': 1,
            'type': 'input',
            'template_options': {
                'placeholder': 'Enter race/ethnicity'
            },
            'hideExpression': '!(model.race_ethnicity && (model.race_ethnicity === "other"))',
        }
    )

    is_english_primary = db.Column(
        db.Boolean,
        info={
            'type': 'radio',
            'default': True,
            'template_options': {
                'required': False
            },
            'self_template_label': 'Is your primary language English?',
            'guardian_template_label': '"Is " + model.first_name + "\'s primary language English?"',
            'options': [
                {'value': 'true', 'label': 'True'},
                {'value': 'false', 'label': 'False'}
            ]
        }
    )

    def get_meta(self, is_self=True):
        info = {'table': {'sensitive': False,
                          'label': 'Demographics'
                          }
                }
        if is_self:
            info['table']['description'] = 'Please answer the following questions about yourself (* indicates ' \
                                           'required response):',
        else:
            info['table']['description'] = 'Please answer the following questions about your child or the person ' \
                                           'with autism on whom you are providing information (* indicates required ' \
                                           'response):'
        for c in self.metadata.tables['demographics_questionnaire'].columns:
            info[c.name] = c.info
            if 'self_template_label' in info[c.name] and is_self:
                info[c.name]['template_options']['label'] = info[c.name]['self_template_label']
            elif 'guardian_template_label' in info[c.name] and not is_self:
                info[c.name]['template_options']['label'] = info[c.name]['guardian_template_label']
        return info
