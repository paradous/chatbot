
from os import environ


class Config:
    """Bot configuration class."""

    # Deployment
    PORT = int(environ.get("PORT", 3978))

    # Azure deployment
    APP_ID = environ.get("MS_APP_ID", "")
    APP_PASSWORD = environ.get("MS_APP_PASSWORD", "")

    # Models
    MODEL_PREPROCESS = "en_core_web_sm"  # SpaCy smallest model - For preprocess
    MODEL_INFERENCE = "bert-base-uncased"  # HuggingFace smallest BERT model - For inference
    MODEL_MATCHING = "TF-IDF"  # PolyFuzz lightest model - Optimized for matching

    # External files
    FILTERS_TOML = "./filters.toml"
