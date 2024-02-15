import datetime

import flask_restful
from flask import request
from marshmallow import ValidationError
from sqlalchemy import cast, Integer, select
from sqlalchemy.orm import joinedload

from app.auth import auth
from app.database import session
from app.models import AdminNote, Resource, User
from app.enums import Permission
from app.rest_exception import RestException
from app.schemas import AdminNoteSchema
from app.wrappers import requires_permission

select_admin_notes_with_joins = select(AdminNote).options(
    joinedload(AdminNote.resource).options(joinedload(Resource.resource_categories)),
    joinedload(AdminNote.user).options(joinedload(User.participants)),
)


class AdminNoteEndpoint(flask_restful.Resource):

    schema = AdminNoteSchema()

    @auth.login_required
    @requires_permission(Permission.edit_resource)
    def get(self, admin_note_id: int):
        model = session.query(AdminNote).filter(AdminNote.id == admin_note_id).first()
        if model is None:
            raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(model)

    @auth.login_required
    @requires_permission(Permission.edit_resource)
    def delete(self, admin_note_id: int):
        session.query(AdminNote).filter(AdminNote.id == admin_note_id).delete()
        session.commit()
        return None

    @auth.login_required
    @requires_permission(Permission.edit_resource)
    def put(self, admin_note_id: int):
        request_data = request.get_json()
        instance = session.query(AdminNote).filter(AdminNote.id == admin_note_id).first()
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
        admin_notes = session.execute(select_admin_notes_with_joins).unique().scalars().all()
        return self.adminNotesSchema.dump(admin_notes)

    @auth.login_required
    @requires_permission(Permission.edit_resource)
    def post(self):
        request_data = request.get_json()
        try:
            new_note = self.adminNoteSchema.load(data=request_data, session=session)
        except ValidationError as err:
            raise RestException(RestException.INVALID_OBJECT, details=err)

        session.add(new_note)
        session.commit()
        note_id = new_note.id
        session.close()

        db_note = session.execute(select_admin_notes_with_joins.filter_by(id=note_id)).unique().scalar_one()
        return self.adminNoteSchema.dump(db_note)


class AdminNoteListByUserEndpoint(flask_restful.Resource):
    @auth.login_required
    @requires_permission(Permission.user_detail_admin)
    def get(self, user_id):
        schema = AdminNoteSchema(many=True)
        logs = (
            session.execute(select_admin_notes_with_joins.filter(AdminNote.user_id == cast(user_id, Integer)))
            .unique()
            .scalars()
            .all()
        )
        return schema.dump(logs)


class AdminNoteListByResourceEndpoint(flask_restful.Resource):
    @auth.login_required
    @requires_permission(Permission.edit_resource)
    def get(self, resource_id):
        schema = AdminNoteSchema(many=True)
        logs = (
            session.execute(select_admin_notes_with_joins.filter(AdminNote.resource_id == cast(resource_id, Integer)))
            .unique()
            .scalars()
            .all()
        )
        return schema.dump(logs)
