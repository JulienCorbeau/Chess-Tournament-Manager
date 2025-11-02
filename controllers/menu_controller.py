class MenuController:
    """Handles menu navigation."""

    def __init__(self, app_controller):
        """
        Initializes the MenuController.

        Args:
            app_controller (ApplicationController): The main application
                controller instance.
        """
        self.app_controller = app_controller
        self.view = app_controller.view

    def show_main_menu(self):
        """
        Displays and handles the main menu loop.
        """
        while True:
            choice = self.view.display_main_menu()
            if choice == "1":  # Add new player
                self.app_controller.add_new_player()
            elif choice == "2":  # Add new tournament
                self.app_controller.create_new_tournament()
            elif choice == "3":  # Manage tournament
                self.app_controller.manage_tournament()
            elif choice == "4":  # Show repports menu
                self.show_reports_menu()
            elif choice == "5":  # Close application
                self.view.display_goodbye_message()
                break
            else:
                self.view.display_validation_error("Choix invalide.")

    def show_reports_menu(self):
        """
        Displays and handles the reports sub-menu loop.
        """
        while True:
            choice = self.view.display_reports_menu()
            if choice == "1":  # Players repports
                self.app_controller.display_all_players_report()
            elif choice == "2":  # Tournament repports
                self.app_controller.display_all_tournaments_report()
            elif choice == "3":  # Details tournament
                self.app_controller.display_tournament_details_report()
            elif choice == "4":  # Details players of a tournament
                self.app_controller.display_tournament_players_report()
            elif choice == "5":
                # Details Round and matchs of a tournament
                self.app_controller.display_tournament_rounds_report()
            elif choice == "6":  # Return main menu
                break
            else:
                self.view.display_validation_error("Choix invalide.")