from views.main_view import MainView
from controllers.player_controller import PlayerController
from controllers.tournament_controller import TournamentController
from controllers.report_controller import ReportController

class MainController:
    """
    Handles the main application loop and menu navigation.
    It creates other controllers "on demand" (lazy instantiation).
    """
    def __init__(self):
        """
        Initializes the MainController.
        We only create the main view, as it's always needed.
        """
        self.view = MainView()

    def run(self):
        """
        Displays and handles the main menu loop.
        """
        self.view.display_welcoming_message()
        
        while True:
            choice = self.view.display_main_menu()
            
            if choice == "1":  # Add new player
                controller = PlayerController() 
                controller.add_new_player()

            elif choice == "2":  # Add new tournament
                controller = TournamentController()
                controller.create_new_tournament()

            elif choice == "3":  # Manage tournament
                controller = TournamentController()
                controller.manage_tournament()

            elif choice == "4":  # Show reports menu
                report_controller = ReportController()
                report_controller.show_reports_menu() 

            elif choice == "5":  # Close application
                self.view.display_goodbye_message()
                break
            else:
                self.view.display_validation_error("Choix invalide.")