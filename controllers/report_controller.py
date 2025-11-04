# controllers/report_controller.py

from models.player import Player
from models.tournament import Tournament

class ReportController:
    """
    Manages all logic related to generating reports.
    """
    def __init__(self, player_manager, tournament_manager, view, report_view):
        """
        Initializes the ReportController.
        """
        self.player_manager = player_manager
        self.tournament_manager = tournament_manager
        self.view = view  # For selection menus
        self.report_view = report_view  # For displaying the final report

    def show_reports_menu(self):
        """
        Displays and handles the reports sub-menu loop.
        """
        while True:
            choice = self.view.display_reports_menu()
            if choice == "1":  # Players reports
                self.display_all_players_report()
            elif choice == "2":  # Tournament reports
                self.display_all_tournaments_report()
            elif choice == "3":  # Details tournament
                self.display_tournament_details_report()
            elif choice == "4":  # Details players of a tournament
                self.display_tournament_players_report()
            elif choice == "5":
                # Details Round and matchs of a tournament
                self.display_tournament_rounds_report()
            elif choice == "6":  # Return main menu
                break
            else:
                self.view.display_validation_error("Choix invalide.")

    def _hydrate_tournament_players(self, tournament):
            """
            Internal helper method to convert a list of player IDs
            into a list of full Player objects.
            """
            if not tournament.players or hasattr(tournament.players[0], 'player_id'):
                return

            all_players = self.player_manager.load_items()
            hydrated_players = []
            
            player_id_map = {
                player.player_id: player for player in all_players
            }
            
            for player_id in tournament.players:
                if player_id in player_id_map:
                    hydrated_players.append(player_id_map[player_id])
                else:
                    print(f"Attention: Joueur ID {player_id} non trouvé.")
            
            tournament.players = hydrated_players

    def display_all_players_report(self):
        """
        Loads all players and tells the view to display them.
        """
        players = self.player_manager.load_items()
        self.report_view.display_players_list(players)

    def display_all_tournaments_report(self):
        """
        Loads all tournaments and tells the view to display them.
        """
        tournaments = self.tournament_manager.load_items()
        self.report_view.display_tournaments_list(tournaments)

    def display_tournament_players_report(self):
        """
        Handles the logic for showing all players in one tournament.
        """
        # Ask user to select a tournament
        tournaments = self.tournament_manager.load_items()
        selected_tournament = self.view.prompt_for_selection(
            tournaments,
            "Rapport : Joueurs d'un Tournoi",
            "name"
        )
        if selected_tournament is None:
            self.view.display_message("Sélection annulée.")
            return

        # Load the full player objects
        self._hydrate_tournament_players(selected_tournament)

        # Call the correct view to display them
        self.report_view.display_tournament_players(
            selected_tournament.players,
            selected_tournament.name
        )

    # --- Placeholders for future reports ---
    def display_tournament_details_report(self):
        msg = ("\n--- Rapport sur les Détails d'un Tournoi --- (Pas encore implémenté)")
        self.view.display_message(msg)

    def display_tournament_rounds_report(self):
        msg = ("\n--- Rapport sur les Rounds et Matchs d'un Tournoi --- (Pas encore implémenté)")
        self.view.display_message(msg)