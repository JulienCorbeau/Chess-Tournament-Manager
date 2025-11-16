"""
Chess Tournament Management Application

Main entry point for the application.
Creates and runs the main controller.
"""

from controllers.main_controller import MainController


def main():
    """
    Application entry point.
    
    Creates the main controller and starts the application loop.
    """
    app = MainController()
    app.run()


if __name__ == "__main__":
    main()
