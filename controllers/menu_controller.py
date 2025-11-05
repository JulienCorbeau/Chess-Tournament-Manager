class MenuController:
    """Handles menu navigation."""

    def __init__(self, player_controller, tournament_controller, 
                 report_controller, view):
        """
        Initializes the MenuController.
        """
        self.player_controller = player_controller
        self.tournament_controller = tournament_controller
        self.report_controller = report_controller 
        self.view = view

    def show_main_menu(self):
        """
        Displays and handles the main menu loop.
        """
        while True:
            choice = self.view.display_main_menu()
            
            if choice == "1":  # Add new player
                self.player_controller.add_new_player()
            elif choice == "2":  # Add new tournament
                self.tournament_controller.create_new_tournament()
            elif choice == "3":  # Manage tournament
                self.tournament_controller.manage_tournament()
            elif choice == "4":  # Show reports menu
                self.report_controller.show_reports_menu() 
            elif choice == "5":  # Close application
                self.view.display_goodbye_message()
                break
            else:
                self.view.display_validation_error("Choix invalide.")