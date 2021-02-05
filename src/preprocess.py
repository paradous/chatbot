
from bs4 import BeautifulSoup
import spacy
import unidecode
from word2number import w2n
import contractions

from config import Config
config = Config()


class Preprocessor:

    def __init__(self):

        # Load SpaCy model for preprocess. Default: en_core_web_sm
        self.nlp = spacy.load(config.MODEL_PREPROCESS)

    @staticmethod
    def strip_html_tags(text: str) -> str:
        """Remove html tags from the document."""

        soup = BeautifulSoup(text, "html.parser")
        return soup.get_text(separator=" ")

    @staticmethod
    def expand_contractions(text: str) -> str:
        """Expand shortened words, e.g. 'don't' to 'do not'."""

        return contractions.fix(text)

    @staticmethod
    def remove_accented_chars(text: str) -> str:
        """Remove accented characters from text, e.g. café."""

        return unidecode.unidecode(text)

    @staticmethod
    def remove_whitespace(text: str) -> str:
        """Remove extra whitespaces from text."""

        text = text.strip()
        return " ".join(text.split())

    @staticmethod
    def limit_n_words(text: str, limit: int = 256):
        """Limit a text to n-words. Default: 256."""

        text = text.split()[:limit]
        return " ".join(text)

    def preprocess(self, text: str) -> str:
        """Apply a preprocess pipeline to a given text."""

        # Apply all preformatting
        text = self.strip_html_tags(text)
        text = self.expand_contractions(text)
        text = self.remove_accented_chars(text)
        text = self.expand_contractions(text)
        text = self.limit_n_words(text)
        text = text.lower()

        # Tokenize the text
        document = self.nlp(text)
        clean_text = []

        for token in document:

            # Convert number words to numeric numbers
            if token.pos_ == 'NUM':
                clean_text.append(w2n.word_to_num(token.text))

            # Convert tokens to base form
            elif token.lemma_ != "-PRON-":
                clean_text.append(token.lemma_)

            # Append the token if no modification was applied
            else:
                clean_text.append(token)

        return " ".join(str(clean_text))
