
from os import environ


class Config:
    """Bot configuration class."""

    # Deployment
    PORT = 3978

    # Azure deployment
    APP_ID = environ.get("MicrosoftAppId", "")
    APP_PASSWORD = environ.get("MicrosoftAppPassword", "")
