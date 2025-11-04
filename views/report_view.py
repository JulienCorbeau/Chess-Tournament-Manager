class ReportView:
    """Handles the display of all reports."""
    
    def display_players_list(self, players):
        """
        Displays a formatted list of players.
        """
        print("\n--- List of All Players ---")
        if not players:
            print("Pas de joueurs présents dans la base de données.")
            return

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

    def display_tournament_players(self, players, tournament_name):
        """
        Affiche la liste des joueurs d'un tournoi, triés par ordre alphabétique.

        Args:
            players (list): Une liste d'objets Player.
            tournament_name (str): Le nom du tournoi pour le titre.
        """
        print(f"\n--- Joueurs Inscrits au Tournoi : {tournament_name} ---")
        if not players:
            print("Aucun joueur n'est encore inscrit à ce tournoi.")
            return

        sorted_players = sorted(
            players,
            key=lambda player: (player.last_name.lower(), player.first_name.lower())
        )

        print(f"{'Nom':<20} {'Prénom':<20} {'ID Nationale'}")
        print("-" * 60)
        for player in sorted_players:
            line = (
                f"{player.last_name:<20} {player.first_name:<20} "
                f"{player.national_id}"
            )
            print(line)
        print("-" * 60)