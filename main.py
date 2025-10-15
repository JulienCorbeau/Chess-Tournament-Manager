from controllers.application_controller import ApplicationController


def main():
    """
    Main entry point for the Chess Tournament Management application.
    """
    app = ApplicationController()
    app.run()


if __name__ == "__main__":
    main()