"""
Main View

Handles all user interface interactions for the chess tournament application.
This is a "dumb" view - it only displays information and collects input.
All logic and data processing is done in controllers.

Sections:
    1. Main Menus - Display navigation menus
    2. Data Prompts - Collect information from user
    3. Feedback Messages - Display success/error/info messages
"""


class MainView:
    """
    Console-based user interface for the tournament application.
    
    This view follows the "dumb view" principle:
    - No business logic
    - No data manipulation
    - Only print() and input() operations
    """

    # ========================================
    # SECTION 1: MAIN MENUS
    # ========================================

    def display_main_menu(self):
        """
        Display the application's main menu.
        
        Returns:
            str: User's menu choice
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
        Display the reports sub-menu.
        
        Returns:
            str: User's menu choice
        """
        print("\n--- Rapports ---")
        print("1. Lister tous les joueurs")
        print("2. Lister tous les tournois")
        print("3. Voir les détails d'un tournoi spécifique")
        print("4. Lister les joueurs d'un tournoi")
        print("5. Lister tous les rounds et matchs d'un tournoi")
        print("6. Retour au menu principal")
        return input("\nEntrez votre choix : ")

    def display_tournament_management_menu(
        self, tournament, current_round_name=None, is_tournament_finished=False
    ):
        """
        Display the tournament management sub-menu.
        
        Menu options adapt based on tournament state:
        - Before start: Can add players and start tournament
        - In progress: Can enter round results
        - Finished: All modifications blocked
        
        Args:
            tournament (Tournament): The tournament being managed
            current_round_name (str, optional): Name of current round (e.g., "Round 2")
            is_tournament_finished (bool): True if all rounds completed
        
        Returns:
            str: User's menu choice
        """
        print(f"\n--- Gestion du Tournoi : {tournament.name} ---")
        
        if current_round_name:
            print(f"Round actuel : {current_round_name}")
        
        if not tournament.rounds:
            print("1. Inscrire un joueur")
            print("2. Démarrer le tournoi")
        elif is_tournament_finished:
            print("1. (Inscriptions fermées)")
            print("2. (Tournoi fini)")
        else:
            print("1. (Inscriptions fermées)")
            print("2. Saisir les résultats du round")
            
        print("3. Afficher les résultats (Pas encore implémenté)")
        print("4. Retourner au menu principal")
        return input("\nEntrez votre choix : ")

    # ========================================
    # SECTION 2: DATA PROMPTS
    # ========================================

    def prompt_for_new_player(self):
        """
        Collect information for creating a new player.
        
        Returns:
            dict: Player data with keys: last_name, first_name,
                  date_of_birth, national_id
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
        Collect information for creating a new tournament.
        
        Returns:
            dict: Tournament data with keys: name, location, start_date,
                  end_date, description, number_of_rounds_str
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

    def display_selection_list(self, title, items_as_strings):
        """
        Display a numbered list of items for selection.
        
        Args:
            title (str): List title
            items_as_strings (list): Pre-formatted list items
        
        Returns:
            bool: True if list has items, False if empty
        """
        print(f"\n--- {title} ---")
        
        if not items_as_strings:
            print("Aucune option disponible.")
            return False

        for line in items_as_strings:
            print(line)
        print("0. Annuler")
        return True

    def prompt_for_choice(self):
        """
        Prompt user for a numeric choice.
        
        Returns:
            str: User's input (not validated)
        """
        return input("\nEntrez le numéro de votre choix : ")

    def prompt_for_match_result(self, player_a, player_b):
        """
        Prompt for the result of a match between two players.
        
        Args:
            player_a (Player): First player
            player_b (Player): Second player
        
        Returns:
            str: User's choice ("1", "2", or "3")
        """
        p_a_name = f"{player_a.first_name} {player_a.last_name}"
        p_b_name = f"{player_b.first_name} {player_b.last_name}"
        
        print(f"\nMatch : {p_a_name} vs {p_b_name}")
        print(f"  1. {p_a_name} (Gagnant)")
        print(f"  2. {p_b_name} (Gagnant)")
        print("  3. Match Nul")
        return input("Entrez le résultat (1, 2, ou 3) : ")

    # ========================================
    # SECTION 3: FEEDBACK MESSAGES
    # ========================================

    # --- Success Messages ---

    def create_player_message(self, last_name, first_name):
        """Display success message for player creation."""
        print(f"\nLe joueur {last_name} {first_name} a été créé avec succès!\n")

    def create_tournament_message(self, tournament_name):
        """Display success message for tournament creation."""
        print(f"\nLe tournoi '{tournament_name}' a été créé avec succès!\n")

    def display_round_started(self, round_name, num_matches):
        """Display success message for round generation."""
        print(f"\nSuccès : {round_name} a été généré avec {num_matches} matchs.")

    def display_player_added_to_tournament(self, player_name, tournament_name):
        """Display success message for player enrollment."""
        print(f"\nLe joueur {player_name} a été inscrit au tournoi {tournament_name}.")

    def display_results_saved(self, round_name):
        """Display success message after saving round results."""
        print(f"\nLes résultats pour le {round_name} ont été enregistrés avec succès.")

    def display_tournament_finished(self):
        """Display message when tournament is completed."""
        print("\n🏆 Le tournoi est terminé ! Tous les rounds ont été joués.")

    # --- Info Messages ---

    def display_selection_cancelled(self):
        """Display info message when user cancels a selection."""
        print("\nSélection annulée. Retour au menu précédent.")

    def display_welcoming_message(self):
        """Display welcome message at application start."""
        print("Bienvenue dans le système de gestion des tournois d'échecs!")

    def display_goodbye_message(self):
        """Display goodbye message when quitting."""
        print(
            "Merci d'avoir utilisé le système de gestion des tournois d'échecs. "
            "Au revoir!"
        )

    # --- Error Messages ---

    def display_validation_error(self, error_message):
        """
        Display a validation error message.
        
        Args:
            error_message (str): The error description
        """
        print(f"\n[ERREUR] {error_message} Veuillez réessayer.\n")

    def display_all_players_already_enrolled(self):
        """Display error when no players are available to add."""
        print("\nTous les joueurs de la base de données sont déjà inscrits à ce tournoi.")
