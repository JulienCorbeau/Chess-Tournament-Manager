"""
Tournament Manager

Specialized manager for Tournament model with automatic hydration.
Handles both data persistence AND business logic for tournament scores.

Hydration Process:
    1. Load tournaments from JSON (contains player IDs, round dicts)
    2. Convert player IDs -> Player objects
    3. Convert round dicts -> Round objects
    4. Convert player IDs in matches -> Player objects
    Result: Fully hydrated Tournament objects ready for use
"""

from models.tournament import Tournament
from models.round import Round
from managers.base_manager import BaseManager
from managers.player_manager import PlayerManager


class TournamentManager(BaseManager):
    """
    Manager for Tournament data operations and business logic.
    
    Extends BaseManager with:
    - Automatic hydration of players and rounds
    - Score management methods
    - Opponent history tracking
    """

    def __init__(self, file_path='data/tournaments/tournaments.json'):
        """
        Initialize the TournamentManager.
        
        Args:
            file_path (str, optional): Path to tournaments JSON file.
                                      Defaults to 'data/tournaments/tournaments.json'.
        """
        super().__init__(
            file_path=file_path,
            model_class=Tournament,
            id_attribute_name='tournament_id'
        )
        self.player_manager = PlayerManager()

    # ========================================
    # DATA LOADING WITH HYDRATION
    # ========================================

    def load_items(self):
        """
        Load all tournaments with automatic hydration.
        
        Hydration steps:
        1. Load basic tournament data (player IDs, round dicts)
        2. Convert player IDs to Player objects
        3. Convert round dicts to Round objects
        4. Convert player IDs in matches to Player objects
        
        Returns:
            list: Fully hydrated Tournament objects
        """
        # Load basic tournament objects
        tournaments = super().load_items()
        
        # Create a player ID -> Player object map for fast lookups
        all_players_map = {
            player.player_id: player
            for player in self.player_manager.load_items()
        }

        # Hydrate each tournament
        for tournament in tournaments:
            self._hydrate_tournament_players(tournament, all_players_map)
            self._hydrate_tournament_rounds(tournament, all_players_map)
        
        return tournaments

    def _hydrate_tournament_players(self, tournament, players_map):
        """
        Convert player IDs to Player objects in a tournament.
        
        Args:
            tournament (Tournament): Tournament to hydrate
            players_map (dict): Mapping of player_id -> Player object
        """
        hydrated_players = []
        
        for player_id in tournament.players:
            player_obj = players_map.get(player_id)
            if player_obj:
                hydrated_players.append(player_obj)
        
        tournament.players = hydrated_players

    def _hydrate_tournament_rounds(self, tournament, players_map):
        """
        Convert round dicts to Round objects and hydrate matches.
        
        Args:
            tournament (Tournament): Tournament to hydrate
            players_map (dict): Mapping of player_id -> Player object
        """
        hydrated_rounds = []
        
        for round_data in tournament.rounds:
            # Convert dict to Round object if needed
            if isinstance(round_data, Round):
                current_round = round_data
            else:
                current_round = Round(**round_data)
            
            # Hydrate matches within the round
            self._hydrate_round_matches(current_round, players_map)
            hydrated_rounds.append(current_round)
        
        tournament.rounds = hydrated_rounds

    def _hydrate_round_matches(self, round_obj, players_map):
        """
        Convert player IDs to Player objects in match tuples.
        
        Args:
            round_obj (Round): Round to hydrate
            players_map (dict): Mapping of player_id -> Player object
        """
        hydrated_matches = []
        
        for match_tuple in round_obj.matches:
            player_a_id = match_tuple[0][0]
            player_b_id = match_tuple[1][0]
            
            player_a_obj = players_map.get(player_a_id)
            player_b_obj = players_map.get(player_b_id)

            if player_a_obj and player_b_obj:
                hydrated_match = (
                    [player_a_obj, match_tuple[0][1]],
                    [player_b_obj, match_tuple[1][1]]
                )
                hydrated_matches.append(hydrated_match)
        
        round_obj.matches = hydrated_matches

    # ========================================
    # BUSINESS LOGIC: SCORE MANAGEMENT
    # ========================================

    def get_player_score(self, tournament, player_id):
        """
        Get or initialize a player's score data in a tournament.
        
        Args:
            tournament (Tournament): The tournament
            player_id (int): The player's ID
        
        Returns:
            dict: Score data with keys 'total_points' and 'opponents_history'
        """
        if player_id not in tournament.player_scores:
            tournament.player_scores[player_id] = {
                "total_points": 0.0,
                "opponents_history": []
            }
        return tournament.player_scores[player_id]

    def add_points_to_player(self, tournament, player_id, points):
        """
        Add points to a player's tournament score.
        
        Args:
            tournament (Tournament): The tournament
            player_id (int): The player's ID
            points (float): Points to add (1.0=win, 0.5=draw, 0.0=loss)
        """
        score_data = self.get_player_score(tournament, player_id)
        score_data["total_points"] += points

    def add_opponent_to_player(self, tournament, player_id, opponent_id):
        """
        Record an opponent in a player's history.
        
        This prevents rematches in Swiss system pairing.
        Special case: opponent_id = -1 represents a "bye"
        
        Args:
            tournament (Tournament): The tournament
            player_id (int): The player's ID
            opponent_id (int): The opponent's ID (or -1 for bye)
        """
        score_data = self.get_player_score(tournament, player_id)
        if opponent_id not in score_data["opponents_history"]:
            score_data["opponents_history"].append(opponent_id)
