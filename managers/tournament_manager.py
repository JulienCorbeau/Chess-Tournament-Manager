from models.tournament import Tournament
from managers.base_manager import BaseManager


class TournamentManager(BaseManager):
    """
    Manages tournament data.
    It inherits all its logic from BaseManager.
    Its only job is to tell BaseManager WHAT to manage.
    """

    def __init__(self, file_path='data/tournaments/tournaments.json'):
        """
        Initializes the TournamentManager.
        It calls the parent (BaseManager) __init__ with
        the correct settings for tournaments.
        """
        # Tell BaseManager:
        # 1. The file path is "data/tournaments/tournaments.json"
        # 2. The "mold" to use is the Tournament class
        # 3. The ID field to look for is "tournament_id"
        super().__init__(
            file_path,
            Tournament,
            'tournament_id'
        )