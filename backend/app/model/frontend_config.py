from flask_marshmallow import Schema

from app import app


class FrontendConfig:
    """ Provides general information about the backend service, what mode it is running in, could also use it for
        health checks etc... """
    development = app.config.get("DEVELOPMENT")
    testing = app.config.get("TESTING")
    mirroring = app.config.get("MIRRORING")
    production = app.config.get("PRODUCTION")
    apiUrl = app.config.get("API_URL")
    apiKey = app.config.get("GOOGLE_MAPS_API_KEY")
    googleAnalyticsKey = app.config.get("GOOGLE_ANALYTICS_API_KEY")


class FrontendConfigSchema(Schema):
    class Meta:
        ordered = True
        fields = ["development", "testing", "mirroring", "production", "apiUrl",
                  "apiKey", "googleAnalyticsKey"]
