from models.player import Player
from models.tournament import Tournament

class ReportController:
    """
    Manages all logic related to generating reports.
    """
    def __init__(self, player_manager, tournament_manager, view, report_view, tournament_controller):
        """
        Initializes the ReportController.
        """
        self.player_manager = player_manager
        self.tournament_manager = tournament_manager
        self.view = view  
        self.report_view = report_view  
        self.tournament_controller = tournament_controller 

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

    def _hydrate_tournament_players(self, tournament):
            """
            Internal helper.
            Converts a list of player IDs (like [1, 2])
            into a list of full Player Objects ([<Player 1>, <Player 2>]).
            """
            # If list is empty or already has objects, do nothing
            if not tournament.players or hasattr(tournament.players[0], 'player_id'):
                return

            all_players = self.player_manager.load_items()
            hydrated_players = []
            
            # Create a "fast lookup" map (ID -> Object)
            player_id_map = {
                player.player_id: player for player in all_players
            }
            
            # Convert the tournament's ID list
            for player_id in tournament.players:
                if player_id in player_id_map:
                    hydrated_players.append(player_id_map[player_id])
                else:
                    # This case should not happen if data is clean
                    print(f"Attention: Joueur ID {player_id} non trouvé.")
            
            tournament.players = hydrated_players

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

        # 3. Load the full Player objects for this tournament
        self._hydrate_tournament_players(selected_tournament)

        # 4. Sort the players
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