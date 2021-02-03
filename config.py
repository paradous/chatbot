
from os import environ


class Config:
    """Bot configuration class."""

    # Deployment
    PORT = int(environ.get("PORT", 3978))

    # Azure deployment
    APP_ID = environ.get("MS_APP_ID", "")
    APP_PASSWORD = environ.get("MS_APP_PASSWORD", "")
