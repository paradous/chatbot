
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

    # Remote files
    s3_base_url = environ.get("S3_BASE_URL", "")

    weight_file = "resa_BERT_model.pt"
    MODEL_WEIGHT_URL = f"{s3_base_url}/{weight_file}"  # Fine-tuned weights for BERT model
    MODEL_WEIGHT_LOCAL_COPY = f"./assets/model/{weight_file}"

    classes_file = "labels.pickle"
    MODEL_CLASSES_URL = f"{s3_base_url}/{classes_file}"
    MODEL_CLASSES_LOCAL_COPY = f"./assets/model/{classes_file}"

    # Filters
    FILTERS_TOML = "./filters.toml"
