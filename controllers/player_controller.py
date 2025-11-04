import re
from datetime import datetime
from models.player import Player

class PlayerController:
    """
    Manages all logic related to players.
    (Creation, validation, etc.)
    """
    def __init__(self, player_manager, view):
        """
        Initializes the PlayerController.

        Args:
            player_manager (PlayerManager): The manager for player data.
            view (MainView): The main view for user interaction.
        """
        self.player_manager = player_manager
        self.view = view

    def add_new_player(self):
        """
        Orchestrates the process of adding a new player with data
        validation.
        """
        while True:
            player_data = self.view.prompt_for_new_player()
            error = self._validate_player_data(player_data)
            if error:
                self.view.display_validation_error(error)
                continue

            new_id = self.player_manager.get_next_id()

            player = Player(
                last_name=player_data["last_name"].upper(),
                first_name=player_data["first_name"].capitalize(),
                date_of_birth=player_data["date_of_birth"],
                national_id=player_data["national_id"],
                player_id=new_id  
            )
            
            self.player_manager.add_item(player)
            
            self.view.create_player_message(
                player.last_name, player.first_name
            )
            break

    def _validate_player_data(self, player_data):
        """
        Validates the data collected for a new player.
        """
        if not player_data["last_name"] or not player_data["first_name"]:
            return "Le nom et le prénom ne peuvent pas être vides."
        try:
            datetime.strptime(player_data["date_of_birth"], "%Y-%m-%d")
        except ValueError:
            return "Format de date invalide. Veuillez utiliser YYYY-MM-DD."
        if not re.match(r"^[A-Z]{2}\d{5}$", player_data["national_id"]):
            return (
                "Format d'ID d'échecs national invalide. Il doit être "
                "au format 'AB12345'."
            )
        return None