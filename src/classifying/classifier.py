
import pickle

import requests
import torch
from transformers import BertTokenizer, BertForSequenceClassification

from config import Config
config = Config()

# Set the device to cpu
device = torch.device("cpu")


class Classifier:

    def __init__(self):

        # Load the classes
        self.labels = self._load_labels()

        # Download the model and instantiate it
        # self._download_model()
        self.model = self._load_model()

    @staticmethod
    def _load_labels() -> dict:
        """Load the dictionary labels from a pickle file and return it."""

        with open('./assets/data/labels.pickle', 'rb') as handle:
            return pickle.load(handle)

    @staticmethod
    def _download_model():
        """
        Stream and download the model from a given url to the given path.
        """

        # Open the URL and a local file
        with requests.get(config.MODEL_WEIGHT_URL, stream=True) as response:
            with open(config.MODEL_WEIGHT_LOCAL_COPY, 'wb') as handle:

                # Stream the model to the local file
                for chunk in response.iter_content(chunk_size=8192):
                    handle.write(chunk)

    def _load_model(self) -> BertForSequenceClassification:

        # Instantiate the model
        model = BertForSequenceClassification.from_pretrained(
            config.MODEL_CLASSIFIER,
            num_labels=len(self.labels),
            output_attentions=False,
            output_hidden_states=False
        )
        model.to(device)

        # Load and append the weights
        model.load_state_dict(
            torch.load(config.MODEL_WEIGHT_LOCAL_COPY, map_location=device)
        )

        return model

    def predict(self, dataset: BertTokenizer):
        """Make a prediction and return the class."""

        # Make the prediction, get an array of probabilities
        probabilities = self.model(
            input_ids=dataset.input_ids,
            token_type_ids=None,
            attention_mask=dataset.attention_mask
        )

        # Get the predicted class index
        _, predicted_index = torch.max(probabilities[0], dim=1)

        # Return the class name
        return self.labels[predicted_index.data[0].item()]
