
import re
from typing import Dict, List

import toml
import pandas as pd
from polyfuzz import PolyFuzz

from src.matching import Filter
from config import Config
config = Config()


class Matcher:

    def __init__(self):

        # Load PolyFuzz model for matching. Default: TF-IDF
        self.model = PolyFuzz(config.MODEL_MATCHING)

        # Load the filters
        self.filters: Dict[str, List[Filter]] = self.__load_filters()

    @staticmethod
    def __load_filters() -> dict:
        """
        Load the filters from filters.toml (by default), create Filter
        objects, and return a dictionary of these object classified by
        intent.
        """
        filters = {}

        # Load the raw filter
        toml_file = toml.load(config.FILTERS_TOML, _dict=dict)

        # Loop over each intent
        for intent, raw_filters in toml_file.items():
            filter_list = []

            # Loop over each filter in this intent
            for name, content in raw_filters.items():

                # Create and append a Filter object
                filter_list.append(
                    Filter(
                        name=name,
                        words=content['words'],
                        regex=content['regex'],
                        threshold=content['threshold']
                    )
                )

            # Save the filters to the main dictionary
            filters[intent] = filter_list

        return filters

    def get_keywords(self, text: str, intent: str) -> dict:

        keywords = {}

        if intent in self.filters:

            # Split the text into a list of words
            entries = text.split(" ")

            for filter_ in self.filters[intent]:

                # Math similarities between the filter and the given text
                self.model.match(entries, filter_.words)
                matches: pd.DataFrame = self.model.get_matches()

                try:
                    # Get the word with the maximum similarity
                    thresholds = matches[matches['Similarity'] >= filter_.threshold]
                    keyword = thresholds[thresholds['Similarity'] == thresholds['Similarity'].max()].iloc[0, 0]

                except Exception:
                    # If there's no match, set the filter as None
                    keywords[filter_.name] = None

                else:
                    # Use the keyword to retrieve and save its chained-data
                    if result := re.search(filter_.regex % keyword, text):
                        keywords[filter_.name] = result.group(filter_.name)

                    else:
                        keywords[filter_.name] = None

        return keywords
