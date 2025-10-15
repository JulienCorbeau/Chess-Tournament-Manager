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
            print("No players found in the database.")
            return

        # Sort players by last name, then by first name
        sorted_players = sorted(
            players,
            key=lambda player: (player.last_name.lower(), player.first_name.lower())
        )

        print(f"{'Last Name':<20} {'First Name':<20} {'Date of Birth':<15} {'National ID'}")
        print("-" * 75)
        for player in sorted_players:
            print(f"{player.last_name:<20} {player.first_name:<20} {player.date_of_birth:<15} {player.national_id}")
        print("-" * 75)