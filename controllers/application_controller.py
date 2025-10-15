# controllers/application_controller.py

import re
from datetime import datetime
from models.player import Player
from views.main_view import MainView
from managers.player_manager import PlayerManager
from controllers.menu_controller import MenuController
from views.report_view import ReportView  


class ApplicationController:
    """Main controller for the application logic."""

    def __init__(self):
        """Initializes the main controller."""
        self.view = MainView()
        self.player_manager = PlayerManager()
        self.report_view = ReportView()
        self.menu_controller = MenuController(self)

    def run(self):
        """
        Starts the application by running the main menu.
        """
        self.view.display_welcoming_message()
        self.menu_controller.show_main_menu()


    def add_new_player(self):
        """
        Orchestrates the process of adding a new player with data validation.
        """
        while True:
            player_data = self.view.prompt_for_new_player()
            error = self._validate_player_data(player_data)
            if error:
                self.view.display_validation_error(error)
                continue

            player = Player(
                last_name=player_data["last_name"].upper(),
                first_name=player_data["first_name"].capitalize(),
                date_of_birth=player_data["date_of_birth"],
                national_id=player_data["national_id"]
            )
            self.player_manager.add_player(player)
            self.view.create_player_message(player.last_name, player.first_name)
            break


    def _validate_player_data(self, player_data):
        """
        Validates the data collected for a new player.

        Args:
            player_data (dict): A dictionary with player information.

        Returns:
            str or None: An error message if validation fails, otherwise None.
        """
        # Validate names are not empty
        if not player_data["last_name"] or not player_data["first_name"]:
            return "Le nom et le prénom ne peuvent pas être vides."

        # Validate date format
        try:
            datetime.strptime(player_data["date_of_birth"], "%Y-%m-%d")
        except ValueError:
            return "Format de date invalide. Veuillez utiliser YYYY-MM-DD."

        # Validate national chess ID format (two letters, five numbers)
        if not re.match(r"^[A-Z]{2}\d{5}$", player_data["national_id"]):
            return "Format d'ID d'échecs national invalide. Il doit être au format 'AB12345'."

        return None


    # --- Placeholder methods for future features ---

    def create_new_tournament(self):
        self.view.display_message("\n--- Création d'un Nouveau Tournoi --- (Pas encore implémenté)")

    def display_all_players_report(self):
        """
        Loads all players, sorts them, and displays them using the report view.
        """
        # 1. Load players using the manager
        players = self.player_manager.load_players()
        # 2. Pass the list to the report view for display
        self.report_view.display_players_list(players)

    def display_all_tournaments_report(self):
        self.view.display_message("\n--- Rapport sur Tous les Tournois --- (Pas encore implémenté)")

    def display_tournament_details_report(self):
        self.view.display_message("\n--- Rapport sur les Détails d'un Tournoi --- (Pas encore implémenté)")

    def display_tournament_players_report(self):
        self.view.display_message("\n--- Rapport sur les Joueurs d'un Tournoi --- (Pas encore implémenté)")

    def display_tournament_rounds_report(self):
        self.view.display_message("\n--- Rapport sur les Rounds et Matchs d'un Tournoi --- (Pas encore implémenté)")