from config.base import Settings

settings = Settings(
    MIRRORING=True,
    SERVER_NAME="localhost:5001",
    MASTER_URL="http://localhost:5000",
    MASTER_EMAIL="daniel.h.funk@gmail.com",
    MASTER_PASS="dfunk7",
    SQLALCHEMY_DATABASE_URI="postgresql+psycopg://ed_user:ed_pass@localhost/stardrive_mirror",
    ELASTIC_SEARCH={
        "index_prefix": "stardrive_mirror",
        "hosts": ["http://localhost:9200"],
        "timeout": 20,
        "verify_certs": False,
        "use_ssl": False,
        "http_auth_user": "",
        "http_auth_pass": "",
    },
)
