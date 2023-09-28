from flask_marshmallow import fields as ma_fields
from marshmallow import missing, fields

from app.model.participant import Participant, Relationship
from app.model.user import User, Role
from app.schema.model_schema import ModelSchema


"""
This package provides specialized schemas to use during export and import to
a mirrored system.  Define classes here as XXXExportSchema and they will be
picked up bo the ExportService and used automatically.   If not defined here,
the Export Service will first fall back to using a schema XXXSchema defined in
the same module as the class to be marshaled. If this does not exist, it will
check for a schema in the Schema module, a file located in the same directory as
this file.
"""


class UserExportSchema(ModelSchema):
    """Used exclusively for data export, removes identifying information"""

    class Meta(ModelSchema.Meta):
        model = User
        fields = ("id", "last_updated", "role", "email_verified", "email", "_links")

    role = fields.Enum(Role)
    email = fields.Function(lambda obj: missing if obj is None else str(obj.id))
    _links = ma_fields.Hyperlinks(
        {
            "self": ma_fields.URLFor("api.userendpoint", id="<id>"),
        }
    )


class AdminExportSchema(ModelSchema):
    """Allows the full details of an admin account to be exported, so that administrators
    can continue to log into the secondary private server with their normal credentials."""

    class Meta(ModelSchema.Meta):
        model = User
        fields = ("id", "last_updated", "email", "_password", "role", "participants", "token", "email_verified")

    role = fields.Enum(Role)


class ParticipantExportSchema(ModelSchema):
    """Used exclusively for data export, removes identifying information"""

    class Meta(ModelSchema.Meta):
        model = Participant
        fields = ("id", "last_updated", "user_id", "relationship", "avatar_icon", "avatar_color", "_links")

    relationship = fields.Enum(Relationship)
    _links = ma_fields.Hyperlinks(
        {
            "self": ma_fields.URLFor("api.participantendpoint", id="<id>"),
        }
    )
