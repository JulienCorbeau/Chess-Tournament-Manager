class MenuController:
    """Handles menu navigation."""

    def __init__(self, app_controller):
        """
        Initializes the MenuController.

        Args:
            app_controller (ApplicationController): The main application controller instance.
        """
        self.app_controller = app_controller
        self.view = app_controller.view

    def show_main_menu(self):
        """
        Displays and handles the main menu loop.
        """
        while True:
            choice = self.view.display_main_menu()
            if choice == "1":
                self.app_controller.add_new_player()
            elif choice == "2":
                self.view.display_message("\n Pas encore implémenté.")
            elif choice == "3":
                self.view.display_message("\n Pas encore implémenté.")
            elif choice == "4":
                self.show_reports_menu()
            elif choice == "5":
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
            if choice == "1":
                self.app_controller.display_all_players_report()
            elif choice == "2":
                self.app_controller.display_all_tournaments_report()
            elif choice == "3":
                self.app_controller.display_tournament_details_report()
            elif choice == "4":
                self.app_controller.display_tournament_players_report()
            elif choice == "5":
                self.app_controller.display_tournament_rounds_report()
            elif choice == "6":
                break  
            else:
                self.view.display_validation_error("Choix invalide.")