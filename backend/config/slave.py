SLAVE = True
SERVER_NAME = "localhost:5001"
MASTER_URL = "http://localhost:5000"
MASTER_EMAIL = "daniel.h.funk@gmail.com"
MASTER_PASS = "dfunk7"

SQLALCHEMY_DATABASE_URI = "postgresql://ed_user:ed_pass@localhost/stardrive_slave"

# Elastic Search
ELASTIC_SEARCH = {
    "index_prefix": "stardrive_slave",
    "hosts": ["localhost"],
    "port": 9200,
    "timeout": 20,
    "verify_certs": False,
    "use_ssl": False,
    "http_auth_user": "",
    "http_auth_pass": ""
}



