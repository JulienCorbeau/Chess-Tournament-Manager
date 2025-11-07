class Player:
    """
    Represents a single player.
    This class is a "mold" for creating player objects.
    """

    def __init__(
        self,
        last_name,
        first_name,
        date_of_birth,
        national_id,
        total_points=0.0,
        opponents_history=None,
        player_id=None,
    ):
        """
        This is the "builder" for the Player object.
        It runs when you create a new Player.
        """
        self.last_name = last_name
        self.first_name = first_name
        self.date_of_birth = date_of_birth
        self.national_id = national_id  # The ID from the client (e.g., "AB12345")
        self.total_points = total_points
        
        # Use an empty list by default
        self.opponents_history = [] if opponents_history is None else opponents_history
        
        self.player_id = player_id  # The internal ID (e.g., 1, 2, 3)

    def to_dict(self):
        """
        Converts the Player object into a dictionary.
        This is needed to save the data to a JSON file.
        """
        return {
            "player_id": self.player_id,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "date_of_birth": self.date_of_birth,
            "national_id": self.national_id,
            "total_points": self.total_points,
            "opponents_history": self.opponents_history,
        }