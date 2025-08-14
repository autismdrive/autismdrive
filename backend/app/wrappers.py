from functools import wraps
from http import HTTPStatus
from typing import Literal

from app.enums import Role, Permission
from app.rest_exception import RestException

def _check_if_allowed(val: Permission | Role):
    from flask import g

    allowed = False

    if "user" not in g:
        raise RestException(RestException.PERMISSION_DENIED, HTTPStatus.UNAUTHORIZED)
    elif val in Permission:
        allowed = val in g.user.role.permissions()
    elif val in Role:
        allowed = g.user.role is val
    else:
        raise RestException(RestException.INVALID_OBJECT, HTTPStatus.UNPROCESSABLE_ENTITY)

    if not allowed:
        raise RestException(RestException.PERMISSION_DENIED, HTTPStatus.FORBIDDEN)


def requires_role(role: Role):
    """Decorator to require a user to have a specific role to access an endpoint."""

    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            _check_if_allowed(role)
            return f(*args, **kwargs)
        return wrapped
    return wrapper


def requires_permission(permission: Permission):
    """Decorator to require a user to have a specific permission to access an endpoint."""

    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            _check_if_allowed(permission)
            return f(*args, **kwargs)
        return wrapped
    return wrapper
