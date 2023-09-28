from flask_marshmallow import Schema

from config.load import settings


class FrontendConfig:
    """Provides general information about the backend service, what mode it is running in, could also use it for
    health checks etc..."""

    development = settings.DEVELOPMENT
    testing = settings.TESTING
    mirroring = settings.MIRRORING
    production = settings.PRODUCTION
    apiUrl = settings.API_URL
    apiKey = settings.GOOGLE_MAPS_API_KEY
    googleAnalyticsKey = settings.GOOGLE_ANALYTICS_API_KEY


class FrontendConfigSchema(Schema):
    class Meta:
        ordered = True
        fields = ["development", "testing", "mirroring", "production", "apiUrl", "apiKey", "googleAnalyticsKey"]
