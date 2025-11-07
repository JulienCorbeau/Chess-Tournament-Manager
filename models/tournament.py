from models.round import Round

class Tournament:
    """
    Represents a single tournament.
    This class is the "mold" for creating tournament objects.
    """

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
        tournament_id=None
    ):
        """
        This is the "builder" for the Tournament object.
        """
        self.name = name
        self.location = location
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.number_of_rounds = number_of_rounds
        self.current_round = current_round
        
        # 'rounds' is a list that will hold Round objects
        self.rounds = rounds if rounds is not None else []
        
        # 'players' is a list that will hold Player objects (or IDs)
        self.players = players if players is not None else []
        
        self.tournament_id = tournament_id  # The internal ID (e.g., 1, 2, 3)

    def to_dict(self):
        """
        Converts the Tournament object into a dictionary
        so it can be saved to the JSON file.
        """

        # --- Convert Player objects to IDs ---
        # We only want to save the player's ID, not the whole object
        player_ids = []
        for player in self.players:
            if hasattr(player, 'player_id'):
                player_ids.append(player.player_id)  # Get ID from object
            else:
                player_ids.append(player)  # It is already an ID

        # --- Convert Round objects to dicts ---
        # We must call .to_dict() on each Round object
        serialized_rounds = []
        for round_item in self.rounds:
            if isinstance(round_item, Round):
                serialized_rounds.append(round_item.to_dict())  # Convert object
            else:
                serialized_rounds.append(round_item)  # It is already a dict

        # Return the final dictionary
        return {
            "tournament_id": self.tournament_id,
            "name": self.name,
            "location": self.location,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "number_of_rounds": self.number_of_rounds,
            "current_round": self.current_round,
            "rounds": serialized_rounds,  # Save the converted list of rounds
            "players": player_ids,       # Save the list of player IDs
        }