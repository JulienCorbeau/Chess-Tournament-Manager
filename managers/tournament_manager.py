from models.tournament import Tournament
from managers.auto_increment_manager import AutoIncrementManager


class TournamentManager(AutoIncrementManager):
    """Manages tournament data storage and retrieval."""

    def __init__(self, file_path='data/tournaments/tournaments.json'):
        """
        Initializes the TournamentManager, passing the file path
        and the Tournament model to the parent.
        """
        super().__init__(
            file_path,
            Tournament,
            'tournament_id'
        )

    def load_tournaments(self):
        """Loads all tournaments using the generic parent method."""
        return self.load_all()

    def save_tournaments(self, tournaments):
        """Saves tournaments using the generic parent method."""
        self.save_all(tournaments)

    def add_tournament(self, tournament):
        """
        Adds a new tournament to the storage.
        """
        tournaments = self.load_tournaments()
        tournaments.append(tournament)
        self.save_tournaments(tournaments)