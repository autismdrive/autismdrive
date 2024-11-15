from config.base import Settings

settings = Settings(
    SQLALCHEMY_DATABASE_URI="postgresql+psycopg://ed_user:ed_pass@localhost/stardrive",
    TESTING=False,
    CORS_ENABLED=True,
    DEBUG=True,
    DEVELOPMENT=True,
    MASTER_URL="http://localhost:5000",
    DELETE_RECORDS=False,
)
