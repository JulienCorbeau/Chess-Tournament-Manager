import json
import os

from models.tournament import Tournament

class TournamentManager:
    """Manages tournament data storage and retrieval."""

    def __init__(self, file_path='data/tournaments/tournaments.json'):
        """
        Initializes the TournamentManager.

        Args:
            file_path (str): The path to the JSON file where tournaments are stored.
                             Defaults to the path from the architecture diagram.
        """
        self.file_path = file_path
        # Ensure the directory exists (e.g., data/tournaments/)
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        # Ensure the file exists
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump([], f)  # Start with an empty list

    def load_tournaments(self):
        """
        Loads all tournaments from the JSON file using the
        dictionary unpacking method.

        Returns:
            list: A list of Tournament instances.
        """
        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
            # Use dictionary unpacking (**data) to initialize Tournament objects
            return [Tournament(**tournament_data) for tournament_data in data]
        except (json.JSONDecodeError, FileNotFoundError):
            return []  # Return an empty list if file is empty, corrupt, or not found

    def save_tournaments(self, tournaments):
        """
        Saves a list of tournaments to the JSON file.
        Calls .to_dict() on each tournament object.

        Args:
            tournaments (list): A list of Tournament instances to save.
        """
        with open(self.file_path, 'w') as f:
            # Convert each Tournament object to its dict representation
            data_to_save = [tournament.to_dict() for tournament in tournaments]
            json.dump(data_to_save, f, indent=4)

    def add_tournament(self, tournament):
        """
        Adds a new tournament to the storage by loading all,
        appending the new one, and saving back.

        Args:
            tournament (Tournament): The Tournament instance to add.
        """
        tournaments = self.load_tournaments()
        tournaments.append(tournament)
        self.save_tournaments(tournaments)