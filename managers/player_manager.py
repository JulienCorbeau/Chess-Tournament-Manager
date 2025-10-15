import json
import os

from models.player import Player


class PlayerManager:
    """Manages player data storage and retrieval."""

    def __init__(self, file_path='data/players.json'):
        """
        Initializes the PlayerManager.

        Args:
            file_path (str): The path to the JSON file where players are stored.
        """
        self.file_path = file_path
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        # Ensure the file exists
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump([], f)

    def load_players(self):
        """
        Loads all players from the JSON file.

        Returns:
            list: A list of Player instances.
        """
        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
            return [Player.from_dict(player_data) for player_data in data]
        except (json.JSONDecodeError, FileNotFoundError):
            return []  # Return an empty list if the file is empty or doesn't exist

    def save_players(self, players):
        """
        Saves a list of players to the JSON file.

        Args:
            players (list): A list of Player instances to save.
        """
        with open(self.file_path, 'w') as f:                                                    #Aurélien : Réecriture totale du fichier, qu'en penses tu ? 
            json.dump([player.to_dict() for player in players], f, indent=4)

    def add_player(self, player):
        """
        Adds a new player to the storage.

        Args:
            player (Player): The Player instance to add.
        """
        players = self.load_players()
        players.append(player)
        self.save_players(players)