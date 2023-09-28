import os


ENV_NAME = os.getenv("ENV_NAME", default="local")

# Load the configuration based on the environment name set in environment variables.
match ENV_NAME:
    case "testing":
        from config.testing import settings as _settings
    case "mirroring":
        from config.mirror import settings as _settings
    case "docker":
        from config.docker import settings as _settings
    case "local":
        from instance.config import settings as _settings
    case _:
        from config.default import settings as _settings

settings = _settings
