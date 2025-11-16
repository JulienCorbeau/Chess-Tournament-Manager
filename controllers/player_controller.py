"""
Player Controller

Manages player creation and validation logic.
"""

import re
from datetime import datetime
from models.player import Player
from managers.player_manager import PlayerManager
from views.main_view import MainView


class PlayerController:
    """
    Controller for player-related operations.
    
    Responsibilities:
    - Orchestrate player creation workflow
    - Validate player data
    - Coordinate between view and manager
    
    Following Principle #2: Autonomous components (creates own dependencies)
    Following Principle #4: Single responsibility (only handles players)
    """

    def __init__(self):
        """Initialize controller with its dependencies."""
        self.player_manager = PlayerManager()
        self.view = MainView()

    # ========================================
    # PUBLIC METHODS
    # ========================================

    def add_new_player(self):
        """
        Orchestrate the player creation workflow.
        
        Workflow:
        1. Prompt user for player data
        2. Validate data
        3. Generate new ID
        4. Create Player object
        5. Save to storage
        6. Display success message
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
            
            self.view.create_player_message(player.last_name, player.first_name)
            break

    # ========================================
    # VALIDATION
    # ========================================

    def _validate_player_data(self, player_data):
        """
        Validate player data before creation.
        
        Validation rules:
        - Names cannot be empty
        - Date must be in YYYY-MM-DD format
        - National ID must match pattern: 2 letters + 5 digits
        
        Args:
            player_data (dict): Player data to validate
        
        Returns:
            str: Error message if invalid, None if valid
        """
        if not player_data["last_name"] or not player_data["first_name"]:
            return "Le nom et le prénom ne peuvent pas être vides."
        
        try:
            datetime.strptime(player_data["date_of_birth"], "%Y-%m-%d")
        except ValueError:
            return "Format de date invalide. Veuillez utiliser YYYY-MM-DD."
        
        if not re.match(r"^[A-Z]{2}\d{5}$", player_data["national_id"]):
            return (
                "Format d'ID d'échecs national invalide. "
                "Il doit être au format 'AB12345'."
            )
        
        return None
