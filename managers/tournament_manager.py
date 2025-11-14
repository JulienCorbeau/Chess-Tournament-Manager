from models.tournament import Tournament
from managers.base_manager import BaseManager
from managers.player_manager import PlayerManager
from models.round import Round

class TournamentManager(BaseManager):
    """Manages tournament data storage and retrieval."""

    def __init__(self, file_path='data/tournaments/tournaments.json'):
        """
        Initializes the TournamentManager.
        """
        super().__init__(
            file_path,
            Tournament,
            'tournament_id'
        )
        self.player_manager = PlayerManager()

    def load_items(self):
        """
        Loads all tournaments and automatically hydrates
        their player and round lists.
        """
        # 1. Obtenir les objets de base (avec des ID)
        tournaments = super().load_items() 
        
        # 2. Obtenir tous les joueurs (une seule fois)
        all_players_map = {
            player.player_id: player 
            for player in self.player_manager.load_items()
        }

        # 3. Hydrater chaque tournoi
        for tournament in tournaments:
            # Hydrater les joueurs
            hydrated_players = []
            for player_id in tournament.players:
                if player_id in all_players_map:
                    hydrated_players.append(all_players_map[player_id])
            tournament.players = hydrated_players
            
            # Hydrater les rounds
            hydrated_rounds = []
            for round_data in tournament.rounds:
                if isinstance(round_data, Round):
                    hydrated_rounds.append(round_data)
                else:
                    hydrated_rounds.append(Round(**round_data))
            tournament.rounds = hydrated_rounds
            
        # 4. Retourner les tournois complets
        return tournaments