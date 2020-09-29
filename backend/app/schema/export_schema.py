from marshmallow import fields, EXCLUDE
from marshmallow_enum import EnumField
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app import ma
from app.model.participant import Participant, Relationship
from app.model.user import User, Role


"""
This package provides specialized schemas to use during export and import to
a mirrored system.  Define classes here as XXXExportSchema and they will be
picked up bo the ExportService and used automatically.   If not defined here,
the Export Service will first fall back to using a schema XXXSchema defined in
the same module as the class to be marshaled. If this does not exist, it will
check for a schema in the Schema module, a file located in the same directory as
this file.
"""


class UserExportSchema(SQLAlchemyAutoSchema):
    """ Used exclusively for data export, removes identifying information"""
    class Meta:
        model = User
        include_relationships = True
        load_instance = True
        unknown = EXCLUDE
        fields = ('id', 'last_updated', 'role', 'email_verified', 'email', '_links')
        ordered = True
        include_fk = True
    role = EnumField(Role)
    email = fields.Method("obfuscate_email")
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.userendpoint', id='<id>'),
    })

    def obfuscate_email(self, obj):
        return obj.id


class AdminExportSchema(SQLAlchemyAutoSchema):
    """Allows the full details of an admin account to be exported, so that administrators
    can continue to log into the secondary private server with their normal credentials."""
    class Meta:
        model = User
        include_relationships = True
        load_instance = True
        unknown = EXCLUDE
        fields = ('id', 'last_updated', 'email', '_password', 'role',
                  'participants', 'token', 'email_verified')
    role = EnumField(Role)


class ParticipantExportSchema(SQLAlchemyAutoSchema):
    """ Used exclusively for data export, removes identifying information"""
    class Meta:
        model = Participant
        include_relationships = True
        load_instance = True
        unknown = EXCLUDE
        fields = ('id', 'last_updated', 'user_id', 'relationship', 'avatar_icon', 'avatar_color', '_links')
        ordered = True
        include_fk = True
    relationship = EnumField(Relationship)
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.participantendpoint', id='<id>'),
    })
