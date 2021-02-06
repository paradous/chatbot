
from transformers import BertTokenizer

from config import Config
config = Config()


class Tokenizer:

    def __init__(self):
        self.tokenizer = BertTokenizer.from_pretrained(config.MODEL_CLASSIFIER)

    def get_dataset(self, text: str):
        """Return a torch Dataset from a given text."""

        # Tokenize the text and return it
        return self.tokenizer(text, return_tensors="pt")
