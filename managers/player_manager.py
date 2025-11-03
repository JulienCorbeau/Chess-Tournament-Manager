from models.player import Player
from managers.base_manager import BaseManager


class PlayerManager(BaseManager):
    """Manages player data storage and retrieval."""

    def __init__(self, file_path='data/players.json'):
        """
        Initializes the PlayerManager, passing the file path,
        the Player model, and the ID attribute name to the parent.
        """
        super().__init__(file_path, Player, 'player_id')