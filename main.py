from controllers.application_controller import ApplicationController


def main():
    """
    Main entry point for the Chess Tournament Management application.
    """
    # 1. Create the main application controller
    app = ApplicationController()
    
    # 2. Start the application
    app.run()


# This line checks if the script is run directly (not imported)
if __name__ == "__main__":
    main()