from typing import Literal, Optional

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class ElasticsearchSettings(BaseModel):
    hosts: list[str] = Field(default_factory=lambda: ["http://localhost:9200"])
    http_auth_pass: str = ""
    http_auth_user: str = ""
    index_prefix: str = "stardrive"
    timeout: int = 20
    use_ssl: bool = False
    verify_certs: bool = False


class GoogleMapsMapIds(BaseModel):
    resource_details_page: str = ""
    search_page: str = ""


class Settings(BaseSettings):
    NAME: str = "STAR DRIVE Database"
    VERSION: str = "0.1"

    ENV_NAME: str = "local"
    CORS_ENABLED: bool = True
    CORS_ALLOW_ORIGINS: Optional[list[str]] = Field(default_factory=lambda: ["localhost:4200"])
    DEVELOPMENT: bool = True
    TESTING: bool = True
    MIRRORING: bool = False
    PRODUCTION: bool = False
    DELETE_RECORDS: bool = True
    EXPORT_CHECK_INTERNAL_MINUTES: int = 1
    IMPORT_INTERVAL_MINUTES: int = 1

    SQLALCHEMY_DATABASE_URI: str = "postgresql+psycopg://ed_user:ed_pass@localhost/stardrive"
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    ELASTIC_SEARCH: ElasticsearchSettings = Field(default_factory=ElasticsearchSettings)

    API_URL: str = "http://localhost:5000"
    SITE_URL: str = "http://localhost:4200"

    SECRET_KEY: str = "stardrive_impossibly_bad_key_stored_in_public_repo_dont_use_this_outside_development_yuck!"

    FRONTEND_AUTH_CALLBACK: str = "#/session"
    FRONTEND_EMAIL_RESET: str = "#/reset_password/"
    FRONTEND_FORGOT_PASSWORD: str = "#/forgot-password"

    MAIL_SERVER: str = "smtp.mailtrap.io"
    MAIL_PORT: int = 2525
    MAIL_USE_TLS: bool = True
    MAIL_USERNAME: str = "__MAIL_USERNAME__"
    MAIL_PASSWORD: str = "__MAIL_PASSWORD__"
    MAIL_DEFAULT_SENDER: str = "autismdrive@virginia.edu"
    MAIL_TIMEOUT: int = 10

    GOOGLE_MAPS_API_KEY: str = "__GOOGLE_MAPS_API_KEY__"
    GOOGLE_ANALYTICS_TAG_ID: str = "__GOOGLE_ANALYTICS_TAG_ID__"
    GOOGLE_MAPS_MAP_IDS: GoogleMapsMapIds = Field(default_factory=GoogleMapsMapIds)

    ADMIN_EMAIL: str = "admin@tester.com"
    PRINCIPAL_INVESTIGATOR_EMAIL: str = "pi@tester.com"  # Receives some high level alerts per agreement with InfoSec.

    _d = r"(?=.*\d)"  # At least one digit.
    _u = r"(?=.*[A-Z])"  # At least one uppercase letter.
    _l = r"(?=.*[a-z])"  # At least one lowercase letter.
    _p = r"(?=.*[^a-zA-Z\d])"  # Punctuation. i.e., any character that isn't a letter or a number.

    ADMIN_PASSWORD_REGEX: str = f"({_d}{_l}{_u}{_p}.{{25}})"  # At least 25 characters long.
    ADMIN_PASSWORD_INSTRUCTIONS: str = (
        "Your password must be at least 25 characters long and contain at least one of each of "
        "the following: uppercase letters, lowercase letters, numbers, and punctuation "
        "characters. Don't use a password that you have used for any other purpose."
    )
    USER_PASSWORD_REGEX: str = f"({_d}{_l}{_u}{_p}.{{8}})"  # At least 8 characters long.
    USER_PASSWORD_INSTRUCTIONS: str = (
        "Your password must be at least 8 characters long, but we recommend 20 characters. It "
        "should include at least one of each of the following: uppercase letters, "
        "lowercase letters, numbers, and punctuation characters."
    )

    FLASK_DEBUG: bool = False
    MASTER_EMAIL: str = "__MASTER_EMAIL__"
    MASTER_PASS: str = "__MASTER_PASS__"
    MASTER_URL: str = "http://localhost:5000"
