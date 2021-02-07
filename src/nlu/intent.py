
from enum import Enum


class Intent(Enum):

    # Yes/No
    YES = "smalltalk_confirmation_yes"
    NO = "smalltalk_confirmation_no"

    # Small talks
    GREETINGS = "smalltalk_greetings_hello"

    # Hotel long talks
    BOOK_ROOM = "longtalk_make_reservation"
