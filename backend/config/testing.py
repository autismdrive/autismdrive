from config.base import Settings, ElasticsearchSettings

settings = Settings(
    ENV_NAME="testing",
    SQLALCHEMY_DATABASE_URI="postgresql+psycopg://ed_user:ed_pass@localhost/stardrive_test",
    TESTING=True,
    CORS_ENABLED=True,
    FLASK_DEBUG=False,
    DEVELOPMENT=False,
    MASTER_URL="http://localhost:5000",
    MASTER_EMAIL="daniel.h.funk@gmail.com",
    MASTER_PASS="dfunk7",
    MIRRORING=False,
    DELETE_RECORDS=False,
    ELASTIC_SEARCH=ElasticsearchSettings(
        index_prefix="stardrive_test",
    ),
    GOOGLE_MAPS_API_KEY="TEST_API_KEY_GOES_HERE",
)
