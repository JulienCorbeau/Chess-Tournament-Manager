class Player:
    """Represents a player in the chess tournament."""

    def __init__(
        self,
        last_name,
        first_name,
        date_of_birth,
        national_id,
        total_points=0.0,
        opponents_history=None,
        player_id=None,  # --- AJOUT ---
    ):
        """
        Initializes a Player instance.
        """
        self.last_name = last_name
        self.first_name = first_name
        self.date_of_birth = date_of_birth
        self.national_id = national_id
        self.total_points = total_points
        self.opponents_history = [] if opponents_history is None else opponents_history
        self.player_id = player_id  # --- AJOUT ---

    def to_dict(self):
        """
        Serializes the Player object to a dictionary.
        """
        return {
            "player_id": self.player_id,  # --- AJOUT ---
            "last_name": self.last_name,
            "first_name": self.first_name,
            "date_of_birth": self.date_of_birth,
            "national_id": self.national_id,
            "total_points": self.total_points,
            "opponents_history": self.opponents_history,
        }