class Tournament:
    """Represents a chess tournament."""

    def __init__(
        self,
        name,
        location,
        description,
        start_date,
        end_date,
        number_of_rounds=4,
        current_round=1,
        rounds=None,
        players=None,
    ):
        """
        Initializes a Tournament instance.

        Args:
            name (str): Tournament's name.
            location (str): Tournament's location.
            description (str): General description.
            start_date (str): Start date (e.g., "YYYY-MM-DD").
            end_date (str): End date (e.g., "YYYY-MM-DD").
            number_of_rounds (int): Total number of rounds. Defaults to 4.
            current_round (int): The current round number. Defaults to 1.
            rounds (list, optional): List of Round objects or dicts (from JSON). Defaults to None.
            players (list, optional): List of Player objects or player IDs (from JSON). Defaults to None.
        """
        self.name = name
        self.location = location
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.number_of_rounds = number_of_rounds
        self.current_round = current_round
        # This is empty for the moment:
        self.rounds = rounds if rounds is not None else []
        self.players = players if players is not None else []

    def to_dict(self):
        """
        Serializes the Tournament object to a dictionary
        suitable for JSON storage.

        Returns:
            dict: A dictionary representation of the tournament.
        """
        return {
            "name": self.name,
            "location": self.location,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "number_of_rounds": self.number_of_rounds,
            "current_round": self.current_round,
            # Need to be update with round & match module :
            "rounds": self.rounds,
            "players": self.players,
        }