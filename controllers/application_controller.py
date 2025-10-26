import re
from datetime import datetime

from models.player import Player
from models.tournament import Tournament
from views.main_view import MainView
from managers.player_manager import PlayerManager
from controllers.menu_controller import MenuController
from views.report_view import ReportView
from managers.tournament_manager import TournamentManager


class ApplicationController:
    """Main controller for the application logic."""

    def __init__(self):
        """Initializes the main controller."""
        self.view = MainView()
        self.player_manager = PlayerManager()
        self.tournament_manager = TournamentManager()
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
        Orchestrates the process of adding a new player with data
        validation.
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
                national_id=player_data["national_id"],
            )
            self.player_manager.add_player(player)
            self.view.create_player_message(
                player.last_name, player.first_name
            )
            break

    def _validate_player_data(self, player_data):
        """
        Validates the data collected for a new player.
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
            return (
                "Format d'ID d'échecs national invalide. Il doit être "
                "au format 'AB12345'."
            )

        return None

    def display_all_players_report(self):
        """
        Loads all players, sorts them, and displays them using the
        report view.
        """
        players = self.player_manager.load_players()
        self.report_view.display_players_list(players)

    def _validate_tournament_data(self, tournament_data):
        """
        Validates the data collected for a new tournament.
        """
        if not tournament_data["name"] or not tournament_data["location"]:
            return "Le nom et le lieu ne peuvent pas être vides."

        try:
            datetime.strptime(tournament_data["start_date"], "%Y-%m-%d")
            datetime.strptime(tournament_data["end_date"], "%Y-%m-%d")
        except ValueError:
            return "Format de date invalide. Veuillez utiliser YYYY-MM-DD."

        start = datetime.strptime(tournament_data["start_date"], "%Y-%m-%d")
        end = datetime.strptime(tournament_data["end_date"], "%Y-%m-%d")
        if end < start:
            return (
                "La date de fin ne peut pas être antérieure à la date de "
                "début."
            )

        rounds_str = tournament_data["number_of_rounds_str"]
        if rounds_str:
            try:
                num_rounds = int(rounds_str)
                if num_rounds <= 0:
                    return (
                        "Le nombre de tours doit être un entier positif."
                    )
            except ValueError:
                return "Le nombre de tours doit être un nombre valide."

        return None

    def create_new_tournament(self):
        """
        Orchestrates the process of creating a new tournament.
        """
        while True:
            tournament_data = self.view.prompt_for_new_tournament()
            error = self._validate_tournament_data(tournament_data)
            if error:
                self.view.display_validation_error(error)
                continue
            rounds_str = tournament_data["number_of_rounds_str"]
            number_of_rounds = int(rounds_str) if rounds_str else 4
            tournament = Tournament(
                name=tournament_data["name"],
                location=tournament_data["location"],
                start_date=tournament_data["start_date"],
                end_date=tournament_data["end_date"],
                description=tournament_data["description"],
                number_of_rounds=number_of_rounds,
            )
            self.tournament_manager.add_tournament(tournament)
            self.view.create_tournament_message(tournament.name)
            break

    def display_all_tournaments_report(self):
        """
        Loads tournaments and passes them to the report view.
        """
        tournaments = self.tournament_manager.load_tournaments()
        self.report_view.display_tournaments_list(tournaments)

    # --- Need to implement ---
    def display_tournament_details_report(self):
        msg = ("\n--- Rapport sur les Détails d'un Tournoi --- "
               "(Pas encore implémenté)")
        self.view.display_message(msg)

    def display_tournament_players_report(self):
        msg = ("\n--- Rapport sur les Joueurs d'un Tournoi --- "
               "(Pas encore implémenté)")
        self.view.display_message(msg)

    def display_tournament_rounds_report(self):
        msg = ("\n--- Rapport sur les Rounds et Matchs d'un Tournoi --- "
               "(Pas encore implémenté)")
        self.view.display_message(msg)