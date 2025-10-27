from models.player import Player
from managers.base_manager import BaseManager


class PlayerManager(BaseManager):
    """Manages player data storage and retrieval."""

    def __init__(self, file_path='data/players.json'):
        """
        Initializes the PlayerManager, passing the file path
        and the Player model to the parent.
        """
        super().__init__(file_path, Player)

    def load_players(self):
        """Loads all players using the generic parent method."""
        return self.load_all()

    def save_players(self, players):
        """Saves players using the generic parent method."""
        self.save_all(players)

    def add_player(self, player):
        """
        Adds a new player to the storage.
        """
        players = self.load_players()
        players.append(player)
        self.save_players(players)