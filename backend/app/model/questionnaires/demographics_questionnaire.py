import datetime

from app import db


class DemographicsQuestionnaire(db.Model):
    __tablename__ = 'demographics_questionnaire'
    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime, default=datetime.datetime.now)
    participant_id = db.Column('participant_id', db.Integer, db.ForeignKey('stardrive_user.id'))
    guardian_id = db.Column('guardian_id', db.Integer, db.ForeignKey('stardrive_user.id'))
    first_name = db.Column(db.String, info={'type': 'input', 'template_label': 'First name*', 'required': 'true'})
    middle_name = db.Column(db.String, info={'type': 'input', 'template_label': 'Middle name', 'required': 'false'})
    last_name = db.Column(db.String, info={'type': 'input', 'template_label': 'Last name*', 'required': 'true'})
    is_first_name_preferred = db.Column(db.Boolean, info={'type': 'radio',
                                                          'self_template_label': 'Is this your preferred name/nick name?',
                                                          'guardian_template_label': 'Is this your child’s preferred name/nick name?',
                                                          'required': 'false'})
    nickname = db.Column(db.String, info={'type': 'input', 'template_label': 'Preferred name or nickname',
                                          'required': 'false', 'hide_expression': '!model.is_first_name_preferred',
                                          'hide_label': 'Enter race/ethnicity'})
    birthdate = db.Column(db.Date, info={'type': 'datepicker', 'self_template_label': 'Your Date of Birth*',
                                         'guardian_template_label': 'model.first_name + "\'s Date of Birth*"',
                                         'required': 'true'})
    birth_city = db.Column(db.String, info={'type': 'input', 'self_template_label': 'Your City/municipality of birth*',
                                            'guardian_template_label': 'model.first_name + "\'s City/municipality of birth*"',
                                            'required': 'true'})
    birth_state = db.Column(db.String, info={'type': 'input', 'self_template_label': 'Your state of birth*',
                                             'guardian_template_label': 'model.first_name + "\'s state of birth*"',
                                             'required': 'true'})
    birth_sex = db.Column(db.String, info={'type': 'radio', 'self_template_label': 'Your sex at birth*',
                                           'guardian_template_label': 'model.first_name + "\'s sex at birth*"',
                                           'required': 'true', 'options': [{'value': 'male', 'label': 'Male'},
                                                                           {'value': 'female', 'label': 'Female'},
                                                                           {'value': 'intersex', 'label': 'Intersex'}]
                                           })
    current_gender = db.Column(db.String, info={'type': 'radio', 'self_template_label': 'Your current gender identity '
                                                                                        '(how you  describe yourself)*:',
                                                'guardian_template_label': 'model.first_name + "\'s current gender '
                                                                           'identity (how " + model.first_name + '
                                                                           '" describes themselves)*:"',
                                                'required': 'true', 'options': [{'value': 'male', 'label': 'Male'},
                                                                                {'value': 'female', 'label': 'Female'},
                                                                                {'value': 'intersex', 'label': 'Intersex'},
                                                                                {'value': 'transgender', 'label': 'Transgender'},
                                                                                {'value': 'other', 'label': 'Other'},
                                                                                {'value': 'no_answer', 'label': 'Choose not to answer'}],
                                                'hide_expression': '!model.genderOther', 'hide_type': 'input',
                                                'hide_label': 'Enter gender identity'
                                                })
    race_ethnicity = db.Column(db.String, info={'type': 'radio', 'self_template_label': 'What is your race/ethnicity? '
                                                                                        '(select all that apply)*',
                                                'guardian_template_label': '"What is " + model.first_name + "\'s '
                                                                           'race/ethnicity?* (select all that apply)"',
                                                'required': 'true', 'options': [{'value': 'raceBlack', 'label': 'Black / African / African American'},
                                                                                {'value': 'raceAsian', 'label': 'Asian / Asian American'},
                                                                                {'value': 'raceWhite', 'label': 'White / Caucasian'},
                                                                                {'value': 'raceHispanic', 'label': 'Hispanic / Latin(o / a)'},
                                                                                {'value': 'raceNative', 'label': 'Native American / Alaskan Native'},
                                                                                {'value': 'racePacific', 'label': 'Pacific Islander'},
                                                                                {'value': 'raceNoAnswer', 'label': 'Prefer not to answer'},
                                                                                {'value': 'raceOther', 'label': 'Other'}
                                                                                ],
                                                'hide_expression': '!model.raceOther', 'hide_type': 'input',
                                                'hide_label': 'Enter race/ethnicity'
                                                })
    is_english_primary = db.Column(db.Boolean, info={'type': 'radio', 'default': 'true',
                                                     'self_template_label': 'Is your primary language English?',
                                                     'guardian_template_label': '"Is " + model.first_name + "\'s '
                                                                                'primary language English?"',
                                                     'required': 'false', 'options': [{'value': 'true', 'label': 'True'},
                                                                                      {'value': 'false', 'label': 'False'}
                                                                                      ]
                                                     })

    def get_meta(self):
        info = {'table': {'sensitive': 'false', 'label': 'Demographics',
                          'self_description': 'Please answer the following questions about yourself (* indicates '
                                              'required response):',
                          'guardian_description': 'Please answer the following questions about your child or the person'
                                                  ' with autism on whom you are providing information:'
                          }
                }
        for c in self.metadata.tables['demographics_questionnaire'].columns:
            info[c.name] = c.info
        return info
