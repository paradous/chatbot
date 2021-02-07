
class RoomReservation:
    """Hotel's room reservation state."""

    def __init__(self, people: int = None, duration: int = None, breakfast: bool = None):

        self.people: int = people  # Number of people
        self.duration: int = duration  # Number of nights
        self.breakfast: bool = breakfast  # If they take breakfast
