from config.base import ElasticsearchSettings, Settings

settings = Settings(
    MIRRORING=True,
    MASTER_URL="http://localhost:5000",
    MASTER_EMAIL="daniel.h.funk@gmail.com",
    MASTER_PASS="dfunk7",
    SQLALCHEMY_DATABASE_URI="postgresql+psycopg://ed_user:ed_pass@localhost/stardrive_mirror",
    ELASTIC_SEARCH=ElasticsearchSettings(
        index_prefix="stardrive_mirror",
    ),
)
