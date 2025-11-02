class ReportView:
    """Handles the display of all reports."""

    def display_players_list(self, players):
        """
        Displays a formatted list of players.

        Args:
            players (list): A list of Player instances to display.
        """
        print("\n--- List of All Players ---")
        if not players:
            print("Pas de joueurs présents dans la base de données.")
            return

        # Sort players by last name, then by first name
        sorted_players = sorted(
            players,
            key=lambda player: (player.last_name.lower(), player.first_name.lower())
        )

        print(f"{'Nom':<20} {'Prénom':<20} {'Né(e) le':<15} {'ID Nationale'}")
        print("-" * 75)
        for player in sorted_players:
            line = (
                f"{player.last_name:<20} {player.first_name:<20} "
                f"{player.date_of_birth:<15} {player.national_id}"
            )
            print(line)
        print("-" * 75)

    def display_tournaments_list(self, tournaments):
        """
        Displays a formatted list of all tournaments.

        Args:
            tournaments (list): A list of Tournament instances to display.
        """
        print("\n--- Liste de Tous les Tournois ---")
        if not tournaments:
            print("Aucun tournoi trouvé dans la base de données.")
            return
        
        sorted_tournaments = sorted(
            tournaments,
            key=lambda tournament: tournament.start_date
        )
        
        print(f"{'Nom du Tournoi':<30} {'Lieu':<25} {'Début':<12} {'Fin':<12}")
        print("-" * 80)
        for tournament in sorted_tournaments:
            line = (
                f"{tournament.name:<30} {tournament.location:<25} "
                f"{tournament.start_date:<12} {tournament.end_date:<12}"
            )
            print(line)
        print("-" * 80)