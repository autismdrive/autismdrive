import datetime

from app import db


class ContactQuestionnaire(db.Model):
    __tablename__ = 'contact_questionnaire'
    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime, default=datetime.datetime.now)
    participant_id = db.Column('participant_id', db.Integer, db.ForeignKey('stardrive_user.id'))
    first_name = db.Column(db.String, info={'type': 'input', 'template_label': 'First name', 'required': 'true'})
    last_name = db.Column(db.String, info={'type': 'input', 'template_label': 'Last name', 'required': 'true'})
    is_first_name_preferred = db.Column(db.Boolean, info={'type': 'radio',
                                                          'template_label': 'Is this your preferred name/nick name?',
                                                          'required': 'false'})
    nickname = db.Column(db.String, info={'type': 'input', 'template_label': 'Preferred name or nickname',
                                          'required': 'false'})
    phone = db.Column(db.String, info={'type': 'input', 'template_type': 'tel', 'required': 'true',
                                       'template_label': 'Preferred phone number (including area code)',
                                       'validation': 'phone'})
    phone_type = db.Column(db.String, info={'type': 'radio', 'template_type': 'tel', 'required': 'true',
                                            'template_label': '', 'options': [{'value': 'home', 'label': 'Home'},
                                                                              {'value': 'cell', 'label': 'Cell'}]})
    can_leave_voicemail = db.Column(db.Boolean, info={'type': 'radio', 'default_value': 'true',
                                                      'template_label': 'Is it okay to leave a voicemail message at this number?',
                                                      'required': 'false'})
    contact_times = db.Column(db.String, info={'type': 'textarea',
                                               'template_label': 'Some research studies might involve a phone call. If '
                                                                 'that’s the case, when would be the best times of day '
                                                                 'to call you?', 'required': 'false'})
    email = db.Column(db.String, info={'type': 'input', 'template_label': 'Email', 'required': 'true',
                                       'validation': 'email'})
    street_address = db.Column(db.String, info={'type': 'input', 'template_label': 'Street Address', 'required': 'true'})
    city = db.Column(db.String, info={'type': 'input', 'template_label': 'Town/City', 'required': 'false'})
    state = db.Column(db.String, info={'type': 'input', 'template_label': 'State', 'required': 'false'})
    zip = db.Column(db.Integer, info={'type': 'input', 'template_type': 'number', 'template_label': 'Zip', 'max': 99999,
                                      'min': 0, 'pattern': '\\d{5}', 'required': 'true'})
    marketing_channel = db.Column(db.String, info={'type': 'radio', 'class_name': 'vertical-radio-group',
                                                   'template_type': 'number',
                                                   'required': 'true',
                                                   'options': [{'value': '1', 'label': 'Internet'},
                                                               {'value': '2', 'label': 'Health care provider (doctor, speech therapist, etc)'},
                                                               {'value': '3', 'label': 'Teacher or school'},
                                                               {'value': '4', 'label': 'Word of mouth (friend, family member, etc)'},
                                                               {'value': '5', 'label': 'Community event (autism walk, resource fair, etc.)'},
                                                               {'value': '6', 'label': 'Television or radio (CNN, NPR, local news, etc.)'},
                                                               {'value': '7', 'label': 'While participating in a research study'},
                                                               {'value': '8', 'label': 'Other'},
                                                               ]
                                                   })

    def get_meta(self):
        info = {'table': {'sensitive': 'false', 'label': 'Research Registrant Contact Information',
                'description': 'Please answer the following questions about YOURSELF (* indicates required response):'},
                'field_groups': {'phone': {'fields': ['phone', 'phone_type', 'can_leave_voicemail', 'contact_times'],
                                           'label': 'Address'},
                                 'address': {'fields': ['street_address', 'city', 'state', 'zip'],
                                             'label': 'Address'},
                                 'marketing': {'fields': ['marketing_channel'], 'label': 'How did you hear about us?'}
                                 }
                }
        for c in self.metadata.tables['contact_questionnaire'].columns:
            info[c.name] = c.info
        return info
