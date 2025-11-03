from models.tournament import Tournament
from managers.base_manager import BaseManager


class TournamentManager(BaseManager):
    """Manages tournament data storage and retrieval."""

    def __init__(self, file_path='data/tournaments/tournaments.json'):
        """
        Initializes the TournamentManager, passing the file path,
        the Tournament model, and the ID attribute name to the parent.
        """
        super().__init__(
            file_path,
            Tournament,
            'tournament_id'
        )