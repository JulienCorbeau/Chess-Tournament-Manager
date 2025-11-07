import re
from datetime import datetime
from models.player import Player

class PlayerController:
    """
    Manages all logic related to players
    (creation, validation, etc.).
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
        Orchestrates the process of adding a new player.
        """
        while True:
            # 1. Ask view to get data from user
            player_data = self.view.prompt_for_new_player()
            
            # 2. Check if the data is valid
            error = self._validate_player_data(player_data)
            if error:
                self.view.display_validation_error(error)
                continue  # Ask again

            # 3. Get the next available ID from the manager
            new_id = self.player_manager.get_next_id()

            # 4. Create the Player object
            player = Player(
                last_name=player_data["last_name"].upper(),
                first_name=player_data["first_name"].capitalize(),
                date_of_birth=player_data["date_of_birth"],
                national_id=player_data["national_id"],
                player_id=new_id  
            )
            
            # 5. Save the new player
            self.player_manager.add_item(player)
            
            # 6. Show success message
            self.view.create_player_message(
                player.last_name, player.first_name
            )
            break  # Exit loop

    def _validate_player_data(self, player_data):
        """
        Internal helper. Checks if player data is valid.
        Returns an error message (string) or None if valid.
        """
        if not player_data["last_name"] or not player_data["first_name"]:
            return "Le nom et le prénom ne peuvent pas être vides."
        try:
            datetime.strptime(player_data["date_of_birth"], "%Y-%m-%d")
        except ValueError:
            return "Format de date invalide. Veuillez utiliser YYYY-MM-DD."
        
        # Use regex to check for format "AA12345"
        if not re.match(r"^[A-Z]{2}\d{5}$", player_data["national_id"]):
            return (
                "Format d'ID d'échecs national invalide. Il doit être "
                "au format 'AB12345'."
            )
        return None