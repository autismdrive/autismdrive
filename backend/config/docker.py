from config.base import Settings

settings = Settings(
    CORS_ENABLED = False,
    SQLALCHEMY_DATABASE_URI = "postgresql://ed_user:ed_pass@star-drive_db_1/stardrive",
    ELASTIC_SEARCH = {
        "index_prefix": "stardrive",
        "hosts": ["star-drive_es_1"],
        "port": 9200,
        "timeout": 20,
        "verify_certs": False,
        "use_ssl": False,
        "http_auth_user": "",
        "http_auth_pass": ""
    },
)


