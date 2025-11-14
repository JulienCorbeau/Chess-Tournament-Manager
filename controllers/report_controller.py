from models.player import Player
from models.tournament import Tournament
from managers.player_manager import PlayerManager
from managers.tournament_manager import TournamentManager
from views.main_view import MainView
from views.report_view import ReportView
from controllers.tournament_controller import TournamentController

class ReportController:
    """
    Manages all logic related to generating reports.
    """
    def __init__(self):
        """
        Initializes the ReportController.
        It creates its own dependencies.
        """
        self.player_manager = PlayerManager()
        self.tournament_manager = TournamentManager()
        self.view = MainView()
        self.report_view = ReportView()
        self.tournament_controller = TournamentController()
        self.tournament_controller.set_report_controller(self)

    def show_reports_menu(self):
        """
        Displays and handles the reports sub-menu loop.
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
            elif choice == "6":  # Return main menu
                break
            else:
                self.view.display_validation_error("Choix invalide.")

    def display_all_players_report(self):
        """
        Prepares and displays the "All Players" report.
        """
        # 1. Load data
        players = self.player_manager.load_items()

        # 2. Sort data
        sorted_players = sorted(
            players,
            key=lambda p: (p.last_name.lower(), p.first_name.lower())
        )

        # 3. Format data for the view
        title = "Liste de Tous les Joueurs"
        headers = ["ID", "Nom", "Prénom", "Date Naissance", "ID Echecs"]
        rows = []
        for p in sorted_players:
            rows.append([
                p.player_id,
                p.last_name,
                p.first_name,
                p.date_of_birth,
                p.national_id
            ])

        # 4. Send the formatted data to the "dumb" view
        self.report_view.display_table(title, headers, rows)

    def display_all_tournaments_report(self):
        """
        Prepares and displays the "All Tournaments" report.
        """
        # 1. Load data
        tournaments = self.tournament_manager.load_items()

        # 2. Sort data (by start date)
        sorted_tournaments = sorted(
            tournaments,
            key=lambda t: t.start_date
        )

        # 3. Format data
        title = "Liste de Tous les Tournois"
        headers = ["ID", "Nom du Tournoi", "Lieu", "Début", "Fin"]
        rows = []
        for t in sorted_tournaments:
            rows.append([
                t.tournament_id,
                t.name,
                t.location,
                t.start_date,
                t.end_date
            ])
        
        # 4. Send to view
        self.report_view.display_table(title, headers, rows)

    def display_tournament_players_report(self):
        """
        Prepares and displays the "Players in a Tournament" report.
        """
        # 1. Load tournaments
        tournaments = self.tournament_manager.load_items()
        
        # 2. Ask user to pick one (using the tournament_controller's method)
        selected_tournament = self.tournament_controller._prompt_user_for_tournament(
            tournaments
        )
        if selected_tournament is None:
            self.view.display_selection_cancelled()
            return

        # 3. Sort the players
        sorted_players = sorted(
            selected_tournament.players,
            key=lambda p: (p.last_name.lower(), p.first_name.lower())
        )

        # 5. Format the data
        title = f"Joueurs Inscrits au Tournoi : {selected_tournament.name}"
        headers = ["Nom", "Prénom", "ID Echecs"]  # We don't show internal ID
        rows = []
        for p in sorted_players:
            rows.append([
                p.last_name,
                p.first_name,
                p.national_id
            ])

        # 6. Send to view
        self.report_view.display_table(title, headers, rows)
    
    
    # --- Placeholders for future reports ---
    def display_tournament_details_report(self):
        print("\n--- Rapport sur les Détails d'un Tournoi --- (Pas encore implémenté)")
    
    def display_tournament_rounds_report(self):
        print("\n--- Rapport sur les Rounds et Matchs d'un Tournoi --- (Pas encore implémenté)")