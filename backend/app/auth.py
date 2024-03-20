from flask_bcrypt import Bcrypt
from flask_httpauth import HTTPTokenAuth

from config.load import settings

auth = HTTPTokenAuth(scheme="Bearer")
bcrypt = Bcrypt()

password_requirements = {
    "user": {
        "regex": settings.USER_PASSWORD_REGEX,
        "instructions": settings.USER_PASSWORD_INSTRUCTIONS,
    },
    "editor": {
        "regex": settings.USER_PASSWORD_REGEX,
        "instructions": settings.USER_PASSWORD_INSTRUCTIONS,
    },
    "researcher": {
        "regex": settings.USER_PASSWORD_REGEX,
        "instructions": settings.USER_PASSWORD_INSTRUCTIONS,
    },
    "test": {
        "regex": settings.ADMIN_PASSWORD_REGEX,
        "instructions": settings.ADMIN_PASSWORD_INSTRUCTIONS,
    },
    "admin": {
        "regex": settings.ADMIN_PASSWORD_REGEX,
        "instructions": settings.ADMIN_PASSWORD_INSTRUCTIONS,
    },
}
