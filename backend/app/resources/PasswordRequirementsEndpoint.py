import flask_restful
from flask import jsonify, request

from app.auth import password_requirements
from app.models import User
from app.enums import Role
from app.rest_exception import RestException


class PasswordRequirementsEndpoint(flask_restful.Resource):

    # Returns password requirements for the given role
    def get(self, role):
        if Role.has_name(role):
            return jsonify(password_requirements[role])
        else:
            raise RestException(RestException.INVALID_INPUT, details="Please enter a valid user role.")

    # Returns true if given password meets requirements for the given role
    def post(self, role):
        request_data = request.get_json()

        if Role.has_name(role):
            reqs = password_requirements[role]
            message = "Please enter a password. " + reqs["instructions"]

            if request_data and "password" in request_data:
                s = request_data["password"]
                if isinstance(s, str):
                    return jsonify(User.password_meets_requirements(role, s))
                else:
                    raise RestException(RestException.INVALID_INPUT, details=message)
            else:
                raise RestException(RestException.INVALID_INPUT, details=message)
        else:
            raise RestException(RestException.INVALID_INPUT, details="Please enter a valid user role.")
