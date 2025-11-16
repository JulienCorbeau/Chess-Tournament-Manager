"""
Main Controller

Entry point controller for the chess tournament application.
Handles main menu navigation and delegates to specialized controllers.
"""

from views.main_view import MainView
from controllers.player_controller import PlayerController
from controllers.tournament_controller import TournamentController
from controllers.report_controller import ReportController


class MainController:
    """
    Main application controller.
    
    Responsibilities:
    - Display and handle main menu
    - Create specialized controllers on demand (lazy instantiation)
    - Delegate tasks to appropriate controllers
    
    Following Principle #2: Autonomous components
    Following Principle #6: Lazy instantiation
    """

    def __init__(self):
        """Initialize the main controller with its view."""
        self.view = MainView()

    def run(self):
        """
        Start the application main loop.
        
        Displays welcome message, then continuously shows menu
        and processes user choices until exit.
        """
        self.view.display_welcoming_message()
        
        while True:
            choice = self.view.display_main_menu()
            
            if choice == "1":
                self._handle_add_player()
            elif choice == "2":
                self._handle_create_tournament()
            elif choice == "3":
                self._handle_manage_tournament()
            elif choice == "4":
                self._handle_show_reports()
            elif choice == "5":
                self._handle_quit()
                break
            else:
                self.view.display_validation_error("Choix invalide.")

    # ========================================
    # MENU HANDLERS
    # ========================================

    def _handle_add_player(self):
        """Handle player creation (delegates to PlayerController)."""
        controller = PlayerController()
        controller.add_new_player()

    def _handle_create_tournament(self):
        """Handle tournament creation (delegates to TournamentController)."""
        controller = TournamentController()
        controller.create_new_tournament()

    def _handle_manage_tournament(self):
        """Handle tournament management (delegates to TournamentController)."""
        controller = TournamentController()
        controller.manage_tournament()

    def _handle_show_reports(self):
        """Handle reports display (delegates to ReportController)."""
        controller = ReportController()
        controller.show_reports_menu()

    def _handle_quit(self):
        """Handle application exit."""
        self.view.display_goodbye_message()
