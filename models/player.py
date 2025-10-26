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
    ):
        """
        Initializes a Player instance.

        Args:
            last_name (str): The player's last name.
            first_name (str): The player's first name.
            date_of_birth (str): The player's date of birth (e.g., "YYYY-MM-DD").
            national_id (str): The player's unique national chess ID.
            total_points (float): The player's total points in a tournament. Defaults to 0.0.
            opponents_history (list, optional): A list of national_ids of players already faced.
                                                Defaults to an empty list.
        """
        self.last_name = last_name
        self.first_name = first_name
        self.date_of_birth = date_of_birth
        self.national_id = national_id
        self.total_points = total_points
        self.opponents_history = [] if opponents_history is None else opponents_history             

    def to_dict(self):
        """
        Serializes the Player object to a dictionary.

        Returns:
            dict: A dictionary representation of the player.
        """
        return {
            "last_name": self.last_name,
            "first_name": self.first_name,
            "date_of_birth": self.date_of_birth,
            "national_id": self.national_id,
            "total_points": self.total_points,
            "opponents_history": self.opponents_history,
        }
