class MenuController:
    """
    Handles the main menu navigation.
    It acts as a "navigator" or "receptionist"
    that directs the user to the correct controller.
    """

    def __init__(self, player_controller, tournament_controller, 
                 report_controller, view):
        """
        Initializes the MenuController.
        It receives all the specialized controllers it needs to call.
        """
        self.player_controller = player_controller
        self.tournament_controller = tournament_controller
        self.report_controller = report_controller 
        self.view = view  # Get the view for simple messages and menu display

    def show_main_menu(self):
        """
        Displays and handles the main menu loop.
        This loop runs forever until the user quits.
        """
        while True:
            # 1. Show the menu options
            choice = self.view.display_main_menu()
            
            # 2. Call the correct controller based on user choice
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
                break  # Exit the loop
            else:
                self.view.display_validation_error("Choix invalide.")