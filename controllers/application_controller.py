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
    Main application orchestrator.
    Its role is to build all components and start the app.
    """

    def __init__(self):
        """
        Initializes all managers, views, and specialized controllers.
        """
        # Create views and managers
        self.view = MainView()
        self.report_view = ReportView()
        self.player_manager = PlayerManager()
        self.tournament_manager = TournamentManager()

        # Create specialized controllers
        self.player_controller = PlayerController(
            self.player_manager, self.view
        )
        self.tournament_controller = TournamentController(
            self.tournament_manager, self.player_manager, self.view
        )
        self.report_controller = ReportController(
            self.player_manager, self.tournament_manager,
            self.view, self.report_view
        )

        # Create the menu controller and give it all specialists
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
        self.menu_controller.show_main_menu()