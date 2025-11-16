"""
Report Controller

Manages report generation and display.
Prepares data from managers and formats it for views.
"""

from managers.player_manager import PlayerManager
from managers.tournament_manager import TournamentManager
from views.main_view import MainView
from views.report_view import ReportView
from controllers.tournament_controller import TournamentController


class ReportController:
    """
    Controller for report generation.
    
    Responsibilities:
    - Handle report menu navigation
    - Load data from managers
    - Format data for display
    - Delegate display to views
    
    Following Principle #2: Autonomous components
    Following Principle #4: Single responsibility (only handles reports)
    Following Principle #5: Dumb views (all logic here, views just display)
    """

    def __init__(self):
        """Initialize controller with its dependencies."""
        self.player_manager = PlayerManager()
        self.tournament_manager = TournamentManager()
        self.view = MainView()
        self.report_view = ReportView()
        self.tournament_controller = TournamentController()
        self.tournament_controller.set_report_controller(self)

    # ========================================
    # MENU NAVIGATION
    # ========================================

    def show_reports_menu(self):
        """
        Display and handle the reports menu loop.
        """
        while True:
            choice = self.view.display_reports_menu()
            
            if choice == "1":
                self.display_all_players_report()
            elif choice == "2":
                self.display_all_tournaments_report()
            elif choice == "3":
                self.display_tournament_details_report()
            elif choice == "4":
                self.display_tournament_players_report()
            elif choice == "5":
                self.display_tournament_rounds_report()
            elif choice == "6":
                break
            else:
                self.view.display_validation_error("Choix invalide.")

    # ========================================
    # REPORT GENERATORS
    # ========================================

    def display_all_players_report(self):
        """
        Generate and display a report of all players.
        
        Steps:
        1. Load all players
        2. Sort alphabetically by last name, then first name
        3. Format as table rows
        4. Send to view for display
        """
        players = self.player_manager.load_items()

        sorted_players = sorted(
            players,
            key=lambda p: (p.last_name.lower(), p.first_name.lower())
        )

        title = "Liste de Tous les Joueurs"
        headers = ["ID", "Nom", "Prénom", "Date Naissance", "ID Echecs"]
        rows = [
            [p.player_id, p.last_name, p.first_name, p.date_of_birth, p.national_id]
            for p in sorted_players
        ]

        self.report_view.display_table(title, headers, rows)

    def display_all_tournaments_report(self):
        """
        Generate and display a report of all tournaments.
        
        Steps:
        1. Load all tournaments
        2. Sort by start date
        3. Format as table rows
        4. Send to view for display
        """
        tournaments = self.tournament_manager.load_items()

        sorted_tournaments = sorted(
            tournaments,
            key=lambda t: t.start_date
        )

        title = "Liste de Tous les Tournois"
        headers = ["ID", "Nom du Tournoi", "Lieu", "Début", "Fin"]
        rows = [
            [t.tournament_id, t.name, t.location, t.start_date, t.end_date]
            for t in sorted_tournaments
        ]
        
        self.report_view.display_table(title, headers, rows)

    def display_tournament_players_report(self):
        """
        Generate and display players enrolled in a specific tournament.
        
        Steps:
        1. Load all tournaments
        2. Let user select one
        3. Sort enrolled players alphabetically
        4. Format as table rows
        5. Send to view for display
        """
        tournaments = self.tournament_manager.load_items()
        
        selected_tournament = self.tournament_controller._prompt_user_for_tournament(
            tournaments
        )
        if selected_tournament is None:
            self.view.display_selection_cancelled()
            return

        sorted_players = sorted(
            selected_tournament.players,
            key=lambda p: (p.last_name.lower(), p.first_name.lower())
        )

        title = f"Joueurs Inscrits au Tournoi : {selected_tournament.name}"
        headers = ["Nom", "Prénom", "ID Echecs"]
        rows = [
            [p.last_name, p.first_name, p.national_id]
            for p in sorted_players
        ]

        self.report_view.display_table(title, headers, rows)

    # ========================================
    # PLACEHOLDER REPORTS
    # ========================================

    def display_tournament_details_report(self):
        """Placeholder for tournament details report."""
        print("\n--- Rapport sur les Détails d'un Tournoi --- (Pas encore implémenté)")

    def display_tournament_rounds_report(self):
        """Placeholder for tournament rounds report."""
        print("\n--- Rapport sur les Rounds et Matchs d'un Tournoi --- (Pas encore implémenté)")
