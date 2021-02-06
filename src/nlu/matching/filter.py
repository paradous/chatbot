
from typing import List


class Filter:
    """
    Filter object, storing values of a filter. Used in the Matcher
    class in a RegEx to extract keywords from a given text.
    """

    def __init__(self, name: str, words: List[str], regex: str, threshold: float = 0.95):

        self.name = name
        self.words = words
        self.regex = self.set_regex(regex)
        self.threshold = threshold

    @staticmethod
    def set_regex(regex: str) -> str:
        """
        Setter for _regex. Clean the regex string and remove double
        backslash due to TOML file formatting.
        """

        regex.replace('\\\\', '\\')
        return regex
