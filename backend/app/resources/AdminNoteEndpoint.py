import flask_restful
from flask import request
from marshmallow import ValidationError
from app import db, auth, RestException
from app.model.admin_note import AdminNote
from app.schema.schema import AdminNoteSchema
from app.model.role import Permission
from app.wrappers import requires_permission
import datetime


class AdminNoteEndpoint(flask_restful.Resource):

    schema = AdminNoteSchema()

    @auth.login_required
    @requires_permission(Permission.edit_resource)
    def get(self, id):
        model = db.session.query(AdminNote).filter_by(id=id).first()
        if model is None: raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(model)

    @auth.login_required
    @requires_permission(Permission.edit_resource)
    def delete(self, id):
        db.session.query(AdminNote).filter_by(id=id).delete()
        db.session.commit()
        return None

    @auth.login_required
    @requires_permission(Permission.edit_resource)
    def put(self, id):
        request_data = request.get_json()
        instance = db.session.query(AdminNote).filter_by(id=id).first()
        updated, errors = self.schema.load(request_data, instance=instance)
        if errors: raise RestException(RestException.INVALID_OBJECT, details=errors)
        updated.last_updated = datetime.datetime.utcnow()
        db.session.add(updated)
        db.session.commit()
        return self.schema.dump(updated)


class AdminNoteListEndpoint(flask_restful.Resource):

    adminNotesSchema = AdminNoteSchema(many=True)
    adminNoteSchema = AdminNoteSchema()

    @auth.login_required
    @requires_permission(Permission.edit_resource)
    def get(self):
        admin_notes = db.session.query(AdminNote).all()
        return self.adminNotesSchema.dump(admin_notes)

    @auth.login_required
    @requires_permission(Permission.edit_resource)
    def post(self):
        request_data = request.get_json()
        try:
            new_note, errors = self.adminNoteSchema.load(request_data)
            if errors: raise RestException(RestException.INVALID_OBJECT, details=errors)
            db.session.add(new_note)
            db.session.commit()
            return self.adminNoteSchema.dump(new_note)
        except ValidationError as err:
            raise RestException(RestException.INVALID_OBJECT,
                                details=new_note.errors)


class AdminNoteListByUserEndpoint(flask_restful.Resource):

    @auth.login_required
    @requires_permission(Permission.user_detail_admin)
    def get(self, user_id):
        schema = AdminNoteSchema(many=True)
        logs = db.session.query(AdminNote)\
            .filter(AdminNote.user_id == user_id)\
            .all()
        return schema.dump(logs)


class AdminNoteListByResourceEndpoint(flask_restful.Resource):

    @auth.login_required
    @requires_permission(Permission.edit_resource)
    def get(self, resource_id):
        schema = AdminNoteSchema(many=True)
        logs = db.session.query(AdminNote)\
            .filter(AdminNote.resource_id == resource_id)\
            .all()
        return schema.dump(logs)
