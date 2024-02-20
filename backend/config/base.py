import re
from os import environ

from pydantic_settings import BaseSettings
from typing_extensions import TypedDict


class SettingsDictElasticsearch(TypedDict):
    hosts: list[str]
    http_auth_pass: str
    http_auth_user: str
    index_prefix: str
    timeout: int
    use_ssl: bool
    verify_certs: bool


class Settings(BaseSettings):
    NAME: str = "STAR DRIVE Database"
    VERSION: str = "0.1"

    ENV_NAME: str = environ.get("ENV_NAME", default="local")
    CORS_ENABLED: bool = True
    CORS_ALLOW_ORIGINS: list[str] = re.split(r",\s*", environ.get("CORS_ALLOW_ORIGINS", default="localhost:4200"))
    DEVELOPMENT: bool = True
    TESTING: bool = True
    MIRRORING: bool = False
    PRODUCTION: bool = False
    DELETE_RECORDS: bool = True
    EXPORT_CHECK_INTERNAL_MINUTES: int = 1
    IMPORT_INTERVAL_MINUTES: int = 1

    SQLALCHEMY_DATABASE_URI: str = "postgresql+psycopg://ed_user:ed_pass@localhost/stardrive"
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    ELASTIC_SEARCH: SettingsDictElasticsearch = {
        "index_prefix": "stardrive",
        "hosts": ["http://localhost:9200"],
        "timeout": 20,
        "verify_certs": False,
        "use_ssl": False,
        "http_auth_user": "",
        "http_auth_pass": "",
    }

    API_URL: str = "http://localhost:5000"
    SITE_URL: str = "http://localhost:4200"

    SECRET_KEY: str = "stardrive_impossibly_bad_key_stored_in_public_repo_dont_use_this_outside_development_yuck!"

    FRONTEND_AUTH_CALLBACK: str = "#/session"
    FRONTEND_EMAIL_RESET: str = "#/reset_password/"
    FRONTEND_FORGOT_PASSWORD: str = "#/forgot-password"

    MAIL_SERVER: str = "smtp.mailtrap.io"
    MAIL_PORT: int = 2525
    MAIL_USE_SSL: bool = False
    MAIL_USE_TLS: bool = True
    MAIL_USERNAME: str = "YOUR-MAILTRAP-NAME - Copy these lines to your instance/config! edit there."
    MAIL_PASSWORD: str = "YOUR-MAILTRAP-PASSWORD - Copy these lines to your instance/config! edit there."
    MAIL_DEFAULT_SENDER: str = "someaddress@fake.com"
    MAIL_DEFAULT_USER: str = "someaddress@fake.com"
    MAIL_TIMEOUT: int = 10

    GOOGLE_MAPS_API_KEY: str = "PRODUCTION_API_KEY_GOES_HERE"
    GOOGLE_ANALYTICS_API_KEY: str = "PRODUCTION_API_KEY_GOES_HERE"

    ADMIN_EMAIL: str = "admin@tester.com"
    PRINCIPAL_INVESTIGATOR_EMAIL: str = "pi@tester.com"  # Receives some high level alerts per agreement with InfoSec.

    ADMIN_PASSWORD_REGEX: str = r"((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{25})"
    ADMIN_PASSWORD_INSTRUCTIONS: str = (
        "Your password must be at least 25 characters long and contain at least one of each of "
        "the following: uppercase letters, lowercase letters, numbers, and punctuation "
        "characters. Don't use a password that you have used for any other purpose."
    )
    USER_PASSWORD_REGEX: str = r"((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8})"
    USER_PASSWORD_INSTRUCTIONS: str = (
        "Your password must be at least 8 characters long, but we recommend 20 characters. It "
        "should include at least one of each of the following: uppercase letters, "
        "lowercase letters, numbers, and punctuation characters."
    )

    DEBUG: bool = False
    MASTER_EMAIL: str = None
    MASTER_PASS: str = None
    MASTER_URL: str = None