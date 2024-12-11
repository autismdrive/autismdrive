from config.base import Settings, ElasticsearchSettings

settings = Settings(
    CORS_ENABLED=False,
    SQLALCHEMY_DATABASE_URI="postgresql+psycopg://ed_user:ed_pass@star-drive_db_1/stardrive",
    ELASTIC_SEARCH=ElasticsearchSettings(
        index_prefix="stardrive",
        hosts=["star-drive_es_1:9200"],
    ),
)
