
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
    MODEL_MATCHING = "TF-IDF"  # PolyFuzz lightest model - Optimized for matching
    MODEL_CLASSIFIER = "bert-base-uncased"  # HuggingFace smallest BERT model - For tokenization and classifying

    # Weights to fine-tune the classifier
    MODEL_WEIGHT_URL = "https://static.paradous.be/file/paradous/chatbot/resa_BERT_model.pt"
    MODEL_WEIGHT_LOCAL_COPY = "./assets/model/resa_BERT_model.pt"

    # External files
    FILTERS_TOML = "./filters.toml"
