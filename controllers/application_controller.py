from views.main_view import MainView
from managers.player_manager import PlayerManager
from controllers.menu_controller import MenuController
from views.report_view import ReportView
from managers.tournament_manager import TournamentManager
from controllers.player_controller import PlayerController
from controllers.tournament_controller import TournamentController
from controllers.report_controller import ReportController


class ApplicationController:
    """
    Main application orchestrator (the "builder").
    Its only job is to build all the components and start the app.
    """

    def __init__(self):
        """
        Initializes all managers, views, and specialized controllers.
        This is where all the app's objects are created.
        """
        # --- 1. Create Managers (for data) ---
        self.player_manager = PlayerManager()
        self.tournament_manager = TournamentManager()
        
        # --- 2. Create Views (for display) ---
        self.view = MainView()
        self.report_view = ReportView()
        
        # --- 3. Create Controllers (for logic) ---
        # Create the player specialist
        self.player_controller = PlayerController(
            self.player_manager, self.view
        )
        
        # Create the tournament specialist
        self.tournament_controller = TournamentController(
            self.tournament_manager, self.player_manager, self.view
        )
        
        # Create the report specialist
        self.report_controller = ReportController(
            self.player_manager, self.tournament_manager,
            self.view, self.report_view,
            self.tournament_controller 
        )

        # Create the main menu (the "navigator")
        self.menu_controller = MenuController(
            self.player_controller,
            self.tournament_controller,
            self.report_controller,
            self.view
        )

    def run(self):
        """
        Starts the application by running the main menu.
        """
        self.view.display_welcoming_message()
        # Hand off control to the menu
        self.menu_controller.show_main_menu()