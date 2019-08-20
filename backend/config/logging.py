logging_config = {
  'version': 1,
  "loggers": {
    "console": {
      "level": "DEBUG",
      "propagate": False,
      "handlers": [
        "console"
      ]
    },
    "file": {
      "level": "DEBUG",
      "propagate": False,
      "handlers": [
        "file"
      ]
    }
  },
  "formatters": {
    "simple": {
      "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    }
  },
  "root": {
    "level": "DEBUG",
    "handlers": [
      "console",
      "file",
    ]
  },
  "handlers": {
    "console": {
      "formatter": "simple",
      "class": "logging.StreamHandler",
      "stream": "ext://sys.stdout",
      "level": "DEBUG"
    },
    "file": {
      "level": "DEBUG",
      "formatter": "simple",
      "class": "logging.FileHandler",
      "filename": "star_drive.log"
    }
  }
}

