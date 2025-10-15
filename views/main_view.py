class MainView:
    """Handles all user interactions in the console."""

    def display_main_menu(self):
        """
        Displays the main menu and prompts the user for a choice.

        Returns:
            str: The user's choice.
        """
        print("\n--- Menu Principal ---")
        print("1. Ajouter un nouveau joueur")
        print("2. Créer un nouveau tournoi")
        print("3. Gérer un tournoi existant (Pas encore implémenté)")
        print("4. Voir les rapports")
        print("5. Quitter l'application")
        return input("\nEntrez votre choix : ")

    def display_reports_menu(self):
        """
        Displays the reports sub-menu and prompts the user for a choice.

        Returns:
            str: The user's choice.
        """
        print("\n--- Rapports ---")
        print("1. Lister tous les joueurs")
        print("2. Lister tous les tournois")
        print("3. Voir les détails d'un tournoi spécifique")
        print("4. Lister les joueurs d'un tournoi")
        print("5. Lister tous les rounds et matchs d'un tournoi")
        print("6. Retour au menu principal")
        return input("\nEntrez votre choix : ")

    def prompt_for_new_player(self):
        """
        Prompts the user to enter information for a new player.
        The required format for the national chess ID is also specified.

        Returns:
            dict: A dictionary containing the new player's information.
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
    
    
    def display_message(self, message):
        """
        Displays a general message to the user.

        Args:
            message (str): The message to display.
        """
        print(f"\n{message}\n")

    def create_player_message(self, last_name, first_name):
        """
        Displays a message confirming the creation of a new player.

        Args:
            last_name (str): The last name of the newly created player.
            first_name (str): The first name of the newly created player.
        """
        print(f"\nLe joueur {last_name} {first_name} a été créé avec succès!\n")

    def display_welcoming_message(self):
        """
        Displays a welcoming message to the user.
        """
        print("Bienvenue dans le système de gestion des tournois d'échecs!")
    

    def display_goodbye_message(self):
        """
        Displays a welcoming message to the user.
        """
        print("Merci d'avoir utilisé le système de gestion des tournois d'échecs. Au revoir!")

    
    def display_validation_error(self, error_message):
        """
        Displays a validation error message in a noticeable format.

        Args:
            error_message (str): The error message to display.
        """
        print(f"\n[ERROR] {error_message} Please try again.\n")