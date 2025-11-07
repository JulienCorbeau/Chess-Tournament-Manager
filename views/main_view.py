class MainView:
    """
    Handles all user interactions in the console.
    This class only does 'print' and 'input'.
    """

    # --- Main Menus ---

    def display_main_menu(self):
        """
        Displays the main menu options.
        """
        print("\n--- Menu Principal ---")
        print("1. Ajouter un nouveau joueur")
        print("2. Créer un nouveau tournoi")
        print("3. Gérer un tournoi existant")
        print("4. Voir les rapports")
        print("5. Quitter l'application")
        return input("\nEntrez votre choix : ")

    def display_reports_menu(self):
        """
        Displays the reports sub-menu options.
        """
        print("\n--- Rapports ---")
        print("1. Lister tous les joueurs")
        print("2. Lister tous les tournois")
        print("3. Voir les détails d'un tournoi spécifique")
        print("4. Lister les joueurs d'un tournoi")
        print("5. Lister tous les rounds et matchs d'un tournoi")
        print("6. Retour au menu principal")
        return input("\nEntrez votre choix : ")

    def display_tournament_management_menu(self, tournament):
        """
        Displays the sub-menu for managing a single tournament.
        This menu is "dynamic": it shows different options
        if the tournament has started (if tournament.rounds is not empty).
        """
        print(f"\n--- Gestion du Tournoi : {tournament.name} ---")

        if not tournament.rounds:
            # Show these options if the tournament has not started
            print("1. Inscrire un joueur")
            print("2. Démarrer le tournoi")
        else:
            # Show these options if the tournament is in progress
            print("1. (Inscriptions fermées)")
            print("2. Saisir les résultats du round (Pas encore implémenté)")
            
        print("3. Afficher les résultats (Pas encore implémenté)")
        print("4. Retourner au menu principal")
        return input("\nEntrez votre choix : ")

    # --- Prompts (Asking for data) ---

    def prompt_for_new_player(self):
        """
        Asks the user for new player details.
        Returns the data as a dictionary.
        """
        print("\n--- Ajouter un Nouveau Joueur ---")
        last_name = input("Entrez le nom de famille du joueur : ")
        first_name = input("Entrez le prénom du joueur : ")
        date_of_birth = input("Entrez la date de naissance du joueur (YYYY-MM-DD) : ")
        national_id = input("Entrez l'ID d'échecs national du joueur (ex. : AB12345) : ")

        return {
            "last_name": last_name,
            "first_name": first_name,
            "date_of_birth": date_of_birth,
            "national_id": national_id
        }

    def prompt_for_new_tournament(self):
        """
        Asks the user for new tournament details.
        Returns the data as a dictionary.
        """
        print("\n--- Créer un Nouveau Tournoi ---")
        name = input("Entrez le nom du tournoi : ")
        location = input("Entrez le lieu du tournoi : ")
        start_date = input("Entrez la date de début (YYYY-MM-DD) : ")
        end_date = input("Entrez la date de fin (YYYY-MM-DD) : ")
        description = input("Entrez une description pour le tournoi : ")
        number_of_rounds_str = input("Entrez le nombre de tours (par défaut 4) : ")

        return {
            "name": name,
            "location": location,
            "start_date": start_date,
            "end_date": end_date,
            "description": description,
            "number_of_rounds_str": number_of_rounds_str
        }

    # --- "Dumb" Views (Used by Controllers) ---
    
    def display_selection_list(self, title, items_as_strings):
        """
        A "dumb" method that just prints a list of pre-formatted options.
        The controller builds the list.
        """
        print(f"\n--- {title} ---")
        if not items_as_strings:
            print("Aucune option disponible.")
            return False  # Tell the controller the list was empty

        for line in items_as_strings:
            print(line)
        print("0. Annuler")
        return True  # Tell the controller the list was shown

    def prompt_for_choice(self):
        """
        A "dumb" method that just asks for a number.
        It does no validation.
        """
        return input("\nEntrez le numéro de votre choix : ")

    # --- Feedback Messages (Success, Error, Info) ---

    def create_player_message(self, last_name, first_name):
        """Shows a success message when a player is created."""
        print(f"\nLe joueur {last_name} {first_name} a été créé avec succès!\n")

    def create_tournament_message(self, tournament_name):
        """Shows a success message when a tournament is created."""
        print(f"\nLe tournoi '{tournament_name}' a été créé avec succès!\n")

    def display_round_started(self, round_name, num_matches):
        """Shows a success message when a round starts."""
        print(f"\nSuccès : {round_name} a été généré avec {num_matches} matchs.")

    def display_selection_cancelled(self):
        """Shows an info message when the user cancels a selection."""
        print("\nSélection annulée. Retour au menu précédent.")

    def display_all_players_already_enrolled(self):
        """Shows an error message if no players are available to add."""
        print("\nTous les joueurs de la base de données sont déjà inscrits à ce tournoi.")

    def display_player_added_to_tournament(self, player_name, tournament_name):
        """Shows a success message when a player is added to a tournament."""
        print(f"\nLe joueur {player_name} a été inscrit au tournoi {tournament_name}.")

    def display_validation_error(self, error_message):
        """Displays a formatted validation error."""
        print(f"\n[ERREUR] {error_message} Veuillez réessayer.\n")

    def display_welcoming_message(self):
        """Displays a welcome message at the start of the app."""
        print("Bienvenue dans le système de gestion des tournois d'échecs!")

    def display_goodbye_message(self):
        """Displays a goodbye message when quitting the app."""
        print(
            "Merci d'avoir utilisé le système de gestion des tournois d'échecs. "
            "Au revoir!"
        )