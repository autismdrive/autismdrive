import datetime

import flask_restful
from flask import request, g
from marshmallow import ValidationError
from sqlalchemy import exists, desc, cast, Integer, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.attributes import InstrumentedAttribute

from app.auth import auth
from app.database import session
from app.email_service import EmailService, email_service
from app.enums import Permission, Role
from app.models import EmailLog, EventUser, Study, User, UserFavorite, StudyUser, Participant
from app.rest_exception import RestException
from app.schemas import UserSchema, UserSearchSchema, RegistrationQuestionnaireSchema
from app.wrappers import requires_permission
from config.load import settings


class UserEndpoint(flask_restful.Resource):

    schema = UserSchema()

    @auth.login_required
    def get(self, id):
        if g.user.id != eval(id) and Permission.user_detail_admin not in g.user.role.permissions():
            raise RestException(RestException.PERMISSION_DENIED)
        model = (
            session.execute(
                select(User)
                .options(
                    joinedload(User.participants).options(
                        joinedload(Participant.identification),
                        joinedload(Participant.contact),
                    ),
                    joinedload(User.events),
                    joinedload(User.user_events),
                    joinedload(User.admin_notes),
                    joinedload(User.studies),
                    joinedload(User.user_studies),
                )
                .filter_by(id=cast(id, Integer))
            )
            .unique()
            .scalar_one_or_none()
        )
        session.close()
        if model is None:
            raise RestException(RestException.NOT_FOUND)
        return self.schema.dump(model)

    @auth.login_required
    @requires_permission(Permission.delete_user)
    def delete(self, id):
        session.query(EventUser).filter_by(user_id=cast(id, Integer)).delete()
        session.query(StudyUser).filter_by(user_id=cast(id, Integer)).delete()
        session.query(UserFavorite).filter_by(user_id=cast(id, Integer)).delete()
        session.query(User).filter_by(id=cast(id, Integer)).delete()
        session.commit()
        return None

    @auth.login_required
    def put(self, id):
        if g.user.id != eval(id) and Permission.user_detail_admin not in g.user.role.permissions():
            raise RestException(RestException.PERMISSION_DENIED)
        request_data = request.get_json()
        if "role" in request_data and request_data["role"] == "admin":
            if g.user.role == Role.admin:
                request_data["role"] = "admin"
            else:
                request_data["role"] = "user"
        instance = session.query(User).filter_by(id=cast(id, Integer)).first()
        try:
            updated = self.schema.load(request_data, instance=instance)
        except Exception as errors:
            raise RestException(RestException.INVALID_OBJECT, details=errors)
        updated.last_updated = datetime.datetime.utcnow()
        session.add(updated)
        session.commit()
        return self.schema.dump(updated)


class UserListEndpoint(flask_restful.Resource):

    usersSchema = UserSchema(many=True)
    userSchema = UserSchema()
    searchSchema = UserSearchSchema()

    @auth.login_required
    @requires_permission(Permission.user_admin)
    def get(self):
        args = request.args
        pageNumber = eval(args["pageNumber"]) if ("pageNumber" in args) else 0
        per_page = eval(args["pageSize"]) if ("pageSize" in args) else 20
        query = session.query(User)
        if "filter" in args:
            if args["filter"].isdigit():
                query = query.filter(User.id == args["filter"])
            else:
                f = "%" + args["filter"] + "%"
                query = query.filter(User.email.ilike(f))

        sort_column = args["sort"] if ("sort" in args) else "email"
        col = getattr(User, sort_column)

        # FIXME: Enable sorting by function properties.
        if isinstance(col, InstrumentedAttribute):
            if args["sortOrder"] == "desc":
                query = query.order_by(desc(col))
            else:
                query = query.order_by(col)

        page = query.paginate(page=pageNumber + 1, per_page=per_page, error_out=False)
        return self.searchSchema.dump(page)

    def post(self):
        """
        Adds new user (with given attributes in request data) to the database and sends confirmation email
        to the provided email address
        """
        request_data = request.get_json()
        try:
            request_data["role"] = "user"
            try:
                new_user = self.userSchema.load(request_data)
            except Exception as errors:
                raise RestException(RestException.INVALID_OBJECT, details=errors)
            email_exists = session.query(exists().where(User.email == new_user.email)).scalar()
            if email_exists:
                raise RestException(RestException.EMAIL_EXISTS)
            session.add(new_user)
            session.commit()
            self.send_confirm_email(new_user)
            return self.userSchema.dump(new_user)
        except IntegrityError as ie:
            raise RestException(RestException.INVALID_OBJECT, details=ie)
        except ValidationError as err:
            raise RestException(RestException.INVALID_OBJECT, details=err)

    @staticmethod
    def send_confirm_email(user):
        current_studies = session.query(Study).filter_by(status="currently_enrolling").all()
        for study in current_studies:
            study.link = (
                settings.SITE_URL
                + "/#/study/"
                + str(study.id)
                + EmailService.generate_google_analytics_link_content("reset_password_study" + str(study.id), "0days")
            )
        tracking_code = email_service.confirm_email(user, current_studies)
        log = EmailLog(user_id=user.id, type="confirm_email", tracking_code=tracking_code)
        session.add(log)
        session.commit()


class UserRegistrationEndpoint(flask_restful.Resource):
    def post(self):
        request_data = request.get_json()
        if "_links" in request_data:
            request_data.pop("_links")
        schema = RegistrationQuestionnaireSchema()
        registration_quest, errors = schema.load(request_data, session=session)

        if errors:
            raise RestException(RestException.INVALID_OBJECT, details=errors)
        session.add(registration_quest)
        session.commit()
        return schema.dump(registration_quest)
