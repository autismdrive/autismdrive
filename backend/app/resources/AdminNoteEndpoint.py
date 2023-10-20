import datetime

import flask_restful
from flask import request
from marshmallow import ValidationError

from app.auth import auth
from app.database import session
from app.models import AdminNote
from app.enums import Permission
from app.rest_exception import RestException
from app.schemas import AdminNoteSchema
from app.wrappers import requires_permission


class AdminNoteEndpoint(flask_restful.Resource):

    schema = AdminNoteSchema()

    @auth.login_required
    @requires_permission(Permission.edit_resource)
    def get(self, id):
        model = session.query(AdminNote).filter(AdminNote.id == id).first()
        if model is None:
            raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(model)

    @auth.login_required
    @requires_permission(Permission.edit_resource)
    def delete(self, id):
        session.query(AdminNote).filter(AdminNote.id == id).delete()
        session.commit()
        return None

    @auth.login_required
    @requires_permission(Permission.edit_resource)
    def put(self, id):
        request_data = request.get_json()
        instance = session.query(AdminNote).filter(AdminNote.id == id).first()
        try:
            updated = self.schema.load(data=request_data, instance=instance, session=session)
        except ValidationError as e:
            raise RestException(RestException.INVALID_OBJECT, details=e.messages)
        updated.last_updated = datetime.datetime.utcnow()
        session.add(updated)
        session.commit()
        return self.schema.dump(updated)


class AdminNoteListEndpoint(flask_restful.Resource):

    adminNotesSchema = AdminNoteSchema(many=True)
    adminNoteSchema = AdminNoteSchema()

    @auth.login_required
    @requires_permission(Permission.edit_resource)
    def get(self):
        admin_notes = session.query(AdminNote).all()
        return self.adminNotesSchema.dump(admin_notes)

    @auth.login_required
    @requires_permission(Permission.edit_resource)
    def post(self):
        request_data = request.get_json()
        try:
            new_note = self.adminNoteSchema.load(data=request_data, session=session)
            session.add(new_note)
            session.commit()
            return self.adminNoteSchema.dump(new_note)
        except ValidationError as err:
            raise RestException(RestException.INVALID_OBJECT, details=err)


class AdminNoteListByUserEndpoint(flask_restful.Resource):
    @auth.login_required
    @requires_permission(Permission.user_detail_admin)
    def get(self, user_id):
        schema = AdminNoteSchema(many=True)
        logs = session.query(AdminNote).filter(AdminNote.user_id == user_id).all()
        return schema.dump(logs)


class AdminNoteListByResourceEndpoint(flask_restful.Resource):
    @auth.login_required
    @requires_permission(Permission.edit_resource)
    def get(self, resource_id):
        schema = AdminNoteSchema(many=True)
        logs = session.query(AdminNote).filter(AdminNote.resource_id == resource_id).all()
        return schema.dump(logs)
