from config.base import Settings


settings = Settings(
    ENV_NAME="testing",
    SQLALCHEMY_DATABASE_URI="postgresql+psycopg://ed_user:ed_pass@localhost/stardrive_test",
    TESTING=True,
    CORS_ENABLED=True,
    DEBUG=False,
    DEVELOPMENT=False,
    MASTER_URL="http://localhost:5000",
    MASTER_EMAIL="daniel.h.funk@gmail.com",
    MASTER_PASS="dfunk7",
    MIRRORING=False,
    DELETE_RECORDS=False,
    ELASTIC_SEARCH={
        "index_prefix": "stardrive_test",
        "hosts": ["http://localhost:9200"],
        "timeout": 20,
        "verify_certs": False,
        "use_ssl": False,
        "http_auth_user": "",
        "http_auth_pass": "",
    },
    GOOGLE_MAPS_API_KEY="TEST_API_KEY_GOES_HERE",
)
