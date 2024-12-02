from database_connection import DatabaseConnection
from user_authentication import UserAuthentication
from prolog_integration import PrologIntegration
from main_menu import MainMenu
import logging

def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        # Database connection setup
        db = DatabaseConnection(host="localhost", user="root", password="Abc123@!", database="GPA_Calculator")
        db.connect()
        logger.info("Database connection established.")

        # User authentication setup
        auth = UserAuthentication(db)

        # Prolog integration setup
        prolog = PrologIntegration("gpa_calculator.pl")

        # Main menu setup
        main_menu = MainMenu(db, auth, prolog)
        main_menu.display_menu()

    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        # Close the database connection
        db.close()
        logger.info("Database connection closed.")

if __name__ == "__main__":
    main()