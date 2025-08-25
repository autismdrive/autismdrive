logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "loggers": {
        "": {  # root logger
            "handlers": ["console", "file"],
            "level": "WARN",
            "propagate": True,
        },
        "alembic.runtime.migration": {"handlers": ["console", "file"], "level": "WARN", "propagate": False},
        "urllib3.connectionpool": {"handlers": ["console", "file"], "level": "WARN", "propagate": False},
        "elasticsearch": {"handlers": ["console", "file"], "level": "WARN", "propagate": False},
        "ElasticIndex": {"handlers": ["console", "file"], "level": "WARN", "propagate": False},
    },
    "formatters": {"simple": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"}},
    "root": {
        "level": "WARN",
        "handlers": [
            "console",
            "file",
        ],
    },
    "handlers": {
        "console": {
            "formatter": "simple",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "level": "WARN",
        },
        "file": {"level": "WARN", "formatter": "simple", "class": "logging.FileHandler", "filename": "star_drive.log"},
    },
}
