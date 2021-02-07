
import pickle

import requests
import torch
from transformers import BertTokenizer, BertForSequenceClassification

from src.nlu import Intent
from config import Config
config = Config()

# Set the device to cpu
device = torch.device("cpu")


class Classifier:

    def __init__(self):

        # Load the classes and the model
        self.labels = self._load_labels()
        self.model = self._load_model()

    @staticmethod
    def __load_remote_file(url: str, local: str):

        # Open the URL and a local file
        with requests.get(url, stream=True) as response:
            with open(local, 'wb') as handle:

                # Stream the model to the local file
                for chunk in response.iter_content(chunk_size=8192):
                    handle.write(chunk)

    def _load_labels(self) -> dict:
        """
        Load the dictionary labels from a remote pickle file and return it.
        """

        # Download and save the pickle locally
        self.__load_remote_file(config.MODEL_CLASSES_URL, config.MODEL_CLASSES_LOCAL_COPY)

        # Load and return a dictionary
        with open(config.MODEL_CLASSES_LOCAL_COPY, 'rb') as handle:
            return pickle.load(handle)

    def _load_model(self) -> BertForSequenceClassification:
        """
        Load the weight of the model from a remote file (around 500 Mo),
        instantiate and return the model.
        """

        # Download and save the weights locally
        # self.__load_remote_file(config.MODEL_WEIGHT_URL, config.MODEL_WEIGHT_LOCAL_COPY)

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

    def predict(self, dataset: BertTokenizer) -> Intent:
        """Make a prediction and return the class."""

        # Make the prediction, get an array of probabilities
        probabilities = self.model(
            input_ids=dataset.input_ids,
            token_type_ids=None,
            attention_mask=dataset.attention_mask
        )

        # Get the predicted class index
        _, predicted_index = torch.max(probabilities[0], dim=1)

        # Return the intent
        return Intent(self.labels[predicted_index[0].item()])
