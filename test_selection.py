def prompt_for_tournament_selection(self, tournaments):
        """
        Affiche une liste numérotée de tournois et demande à 
        l'utilisateur d'en choisir un.

        Args:
            tournaments (list): La liste des objets Tournoi.

        Returns:
            Tournament: L'objet Tournoi sélectionné, ou None si annulé.
        """
        print("\n--- Sélection d'un Tournoi ---")
        if not tournaments:
            print("Aucun tournoi disponible.")
            return None

        # Display numbered list of tournaments
        for i, tournament in enumerate(tournaments, 1):
            print(f"{i}. {tournament.name} (ID: {tournament.tournament_id})")

        print("0. Annuler")
        
        while True:
            choice = input("Entrez le numéro de votre choix : ")
            if not choice.isdigit():
                self.display_validation_error("Veuillez entrer un numéro valide.")
                continue

            choice_int = int(choice)
            if choice_int == 0:
                return None
            if 1 <= choice_int <= len(tournaments):
                return tournaments[choice_int - 1]  # Return the selected tournament object
            else:
                self.display_validation_error("Ce numéro n'est pas dans la liste.")

    def prompt_for_player_selection(self, players):
        """
        Affiche une liste numérotée de joueurs et demande à 
        l'utilisateur d'en choisir un.

        Args:
            players (list): La liste des objets Player.

        Returns:
            Player: L'objet Player sélectionné, ou None si annulé.
        """
        print("\n--- Sélection d'un Joueur ---")
        if not players:
            print("Aucun joueur disponible.")
            return None

        # Display numbered list of players
        for i, player in enumerate(players, 1):
            print(f"{i}. {player.last_name} {player.first_name} (ID: {player.national_id})")

        print("0. Annuler")
        
        while True:
            choice = input("Entrez le numéro de votre choix : ")
            if not choice.isdigit():
                self.display_validation_error("Veuillez entrer un numéro valide.")
                continue

            choice_int = int(choice)
            if choice_int == 0:
                return None
            if 1 <= choice_int <= len(players):
                return players[choice_int - 1]  # Return the selected player object
            else:
                self.display_validation_error("Ce numéro n'est pas dans la liste.")