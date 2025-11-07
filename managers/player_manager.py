from models.player import Player
from managers.base_manager import BaseManager


class PlayerManager(BaseManager):
    """
    Manages player data.
    It inherits all its logic from BaseManager.
    Its only job is to tell BaseManager WHAT to manage.
    """

    def __init__(self, file_path='data/players.json'):
        """
        Initializes the PlayerManager.
        It calls the parent (BaseManager) __init__ with
        the correct settings for players.
        """
        # Tell BaseManager:
        # 1. The file path is "data/players.json"
        # 2. The "mold" to use is the Player class
        # 3. The ID field to look for is "player_id"
        super().__init__(file_path, Player, 'player_id')