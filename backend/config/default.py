NAME = "STAR DRIVE Database"
VERSION = "0.1"

CORS_ENABLED = False
DEVELOPMENT = True
TESTING = True

SQLALCHEMY_DATABASE_URI = "postgresql://ed_user:ed_pass@localhost/stardrive"


# Elastic Search
ELASTIC_SEARCH = {
    "index_prefix": "stardrive",
    "hosts": ["localhost"],
    "port": 9200,
    "timeout": 20,
    "verify_certs": False,
    "use_ssl": False,
    "http_auth_user": "",
    "http_auth_pass": ""
}

API_URL = "http://localhost:5000"
SITE_URL = "http://localhost:4200"

SECRET_KEY = 'stardrive_impossibly_bad_key_stored_in_public_repo_dont_use_this_outside_development_yuck!'

FRONTEND_AUTH_CALLBACK = SITE_URL + "/#/session"
FRONTEND_EMAIL_RESET = SITE_URL + "/#/reset_password/"

MAIL_SERVER = 'smtp.mailtrap.io'
MAIL_PORT = 25
MAIL_USE_SSL = False
MAIL_USE_TLS = False
MAIL_USERNAME = "YOUR-MAILTRAP-NAME - Copy these lines to your instance/config! edit there."
MAIL_PASSWORD = "YOUR-MAILTRAP-PASSWORD - Copy these lines to your instance/config! edit there."
MAIL_DEFAULT_SENDER='someaddress@fake.com'
MAIL_DEFAULT_USER='someaddress@fake.com'
MAIL_TIMEOUT = 10
