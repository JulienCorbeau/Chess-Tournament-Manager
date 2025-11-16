"""
Player Manager

Specialized manager for Player model persistence.
Inherits all functionality from BaseManager.
"""

from models.player import Player
from managers.base_manager import BaseManager


class PlayerManager(BaseManager):
    """
    Manager for Player data operations.
    
    Handles loading, saving, and querying players from JSON storage.
    All logic is inherited from BaseManager.
    """

    def __init__(self, file_path='data/players.json'):
        """
        Initialize the PlayerManager.
        
        Args:
            file_path (str, optional): Path to players JSON file.
                                      Defaults to 'data/players.json'.
        """
        super().__init__(
            file_path=file_path,
            model_class=Player,
            id_attribute_name='player_id'
        )
