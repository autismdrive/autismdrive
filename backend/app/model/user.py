import datetime
import re

import jwt
from sqlalchemy import func, select, case, text
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm import column_property

from app import app, db, RestException, bcrypt, password_requirements
from app.model.participant import Participant
from app.model.role import Role
from app.model.random_id_generator import random_integer
from app.model.user_meta import UserMeta


class User(db.Model):
    # The user model is used to manage interaction with the StarDrive system, including sign-in and access levels. Users
    # can be Admins, people with autism and/or their guardians wishing to manage their care and participate in studies,
    # as well professionals in the field of autism research and care. Anyone who wishes to use the system will have a
    # user account. Please note that there is a separate participant model for tracking enrollment and participation in
    # studies.
    __tablename__ = 'stardrive_user'
    #    id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, primary_key=True, default=random_integer)
    last_updated = db.Column(db.DateTime(timezone=True), default=func.now())
    registration_date = db.Column(db.DateTime(timezone=True), default=func.now())
    last_login = db.Column(db.DateTime(timezone=True))
    email = db.Column(db.String, nullable=False, unique=True)
    role = db.Column(db.Enum(Role))
    participants = db.relationship(Participant, back_populates="user")
    participant_count = column_property(select([func.count(Participant.id)]).
                                        where(Participant.user_id==id).
                                        correlate_except(Participant)
                                        )
    email_verified = db.Column(db.Boolean, nullable=False, default=False)
    _password = db.Column('password', db.Binary(60))
    token = ''
    token_url = ''

    def related_to_participant(self, participant_id):
        for p in self.participants:
            if participant_id == p.id:
                return True

    def self_participant(self):
        if len(self.participants) > 0:
            for p in self.participants:
                if 'self' in p.relationship.name:
                    return p

    def self_registration_complete(self):
        if self.self_participant() is not None:
            return self.self_participant().get_percent_complete() == 1

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext):
        role_name = self.role_name()
        if self.password_meets_requirements(role_name, plaintext):
            self._password = bcrypt.generate_password_hash(plaintext)
        else:
            message = "Please enter a valid password. " + password_requirements[role_name]['instructions']
            raise RestException(RestException.INVALID_INPUT, details=message)

    def role_name(self):
        return self.role if isinstance(self.role, str) else self.role.name

    @classmethod
    def password_meets_requirements(cls, role_name, plaintext):
        reqs = password_requirements[role_name]
        regex = re.compile(reqs['regex'])

        if plaintext and isinstance(plaintext, str):
            match = regex.match(plaintext)
            return bool(match)
        else:
            return False

    def is_correct_password(self, plaintext):
        if not self._password:
            raise RestException(RestException.LOGIN_FAILURE)
        return bcrypt.check_password_hash(self._password, plaintext)

    def encode_auth_token(self):
        try:
            payload = {
                'exp':
                    datetime.datetime.utcnow() + datetime.timedelta(
                        hours=2, minutes=0, seconds=0),
                'iat':
                    datetime.datetime.utcnow(),
                'sub':
                    self.id
            }
            return jwt.encode(
                payload, app.config.get('SECRET_KEY'), algorithm='HS256')
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(
                auth_token, app.config.get('SECRET_KEY'), algorithms='HS256')
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise RestException(RestException.TOKEN_EXPIRED)
        except jwt.InvalidTokenError:
            raise RestException(RestException.TOKEN_INVALID)

    def get_contact(self):
        for p in self.participants:
            if p.contact:
                return {'name': p.get_name(), 'relationship': p.relationship.name, 'contact': p.contact}

    def created_password(self):
        return self._password is not None

    def identity(self):
        self_participant = self.self_participant()
        return 'Not set' if self_participant is None else self_participant.relationship.name

    def percent_self_registration_complete(self):
        self_participant = self.self_participant()
        return 0 if self_participant is None else self_participant.get_percent_complete()
