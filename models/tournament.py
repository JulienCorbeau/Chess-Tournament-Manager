"""
Tournament Model

Represents a chess tournament with its configuration, participants, and rounds.
Following the anemic model pattern: contains only data attributes.
Business logic is handled by TournamentManager.
"""

from models.round import Round


class Tournament:
    """
    A chess tournament with multiple rounds and players.
    
    Attributes:
        tournament_id (int): Unique identifier
        name (str): Tournament name
        location (str): Tournament location
        description (str): Tournament description
        start_date (str): Start date in YYYY-MM-DD format
        end_date (str): End date in YYYY-MM-DD format
        number_of_rounds (int): Total number of rounds (default: 4)
        current_round (int): Current round number (1-indexed)
        rounds (list): List of Round objects
        players (list): List of Player objects (hydrated by manager)
        player_scores (dict): Tournament-specific player data
                             Format: {player_id: {"total_points": float,
                                                  "opponents_history": list}}
    
    Note on player_scores:
        - total_points: Player's cumulative score in this tournament
        - opponents_history: List of opponent IDs faced (includes -1 for byes)
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
        tournament_id=None,
        player_scores=None
    ):
        """
        Initialize a new Tournament instance.
        
        Args:
            name (str): Tournament name
            location (str): Tournament location
            description (str): Tournament description
            start_date (str): Start date in YYYY-MM-DD format
            end_date (str): End date in YYYY-MM-DD format
            number_of_rounds (int, optional): Total rounds. Defaults to 4.
            current_round (int, optional): Current round number. Defaults to 1.
            rounds (list, optional): List of Round objects. Defaults to empty list.
            players (list, optional): List of Player objects. Defaults to empty list.
            tournament_id (int, optional): Unique identifier. Auto-generated if None.
            player_scores (dict, optional): Player performance data. Defaults to empty dict.
        """
        self.tournament_id = tournament_id
        self.name = name
        self.location = location
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.number_of_rounds = number_of_rounds
        self.current_round = current_round
        self.rounds = rounds if rounds is not None else []
        self.players = players if players is not None else []
        self.player_scores = player_scores if player_scores is not None else {}

    def to_dict(self):
        """
        Convert the Tournament object to a dictionary for JSON serialization.
        
        This method "dehydrates" the tournament:
        - Converts Player objects to player IDs
        - Converts Round objects to dictionaries
        - Preserves player_scores as-is (IDs are sufficient)
        
        Returns:
            dict: Tournament data ready for JSON storage
        """
        # Convert Player objects to IDs
        player_ids = []
        for player in self.players:
            player_id = (
                player.player_id
                if hasattr(player, 'player_id')
                else player
            )
            player_ids.append(player_id)

        # Convert Round objects to dictionaries
        serialized_rounds = []
        for round_item in self.rounds:
            if isinstance(round_item, Round):
                serialized_rounds.append(round_item.to_dict())
            else:
                serialized_rounds.append(round_item)

        return {
            "tournament_id": self.tournament_id,
            "name": self.name,
            "location": self.location,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "number_of_rounds": self.number_of_rounds,
            "current_round": self.current_round,
            "rounds": serialized_rounds,
            "players": player_ids,
            "player_scores": self.player_scores,
        }
