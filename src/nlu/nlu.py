
from . import Intent
from .matching import Matcher
from .preprocessing import Preprocessor, Tokenizer
from .classifying import Classifier


class NLU:

    def __init__(self):

        # Preprocessing
        self.preprocessor = Preprocessor()
        self.tokenizer = Tokenizer()

        # Classifier
        self.classifier = Classifier()
        self.matcher = Matcher()

    def get_intent(self, message: str) -> (Intent, dict):
        """
        Return the intention and the keywords of a given message.
        """

        # Clean the message and create a dataset of tokens
        preprocessed_text = self.preprocessor.preprocess(message)
        dataset = self.tokenizer.get_dataset(preprocessed_text)

        # Get the intention
        intent = self.classifier.predict(dataset)
        keywords = self.matcher.get_keywords(preprocessed_text, intent.value)

        return intent, keywords
