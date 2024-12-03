from database_connection import DatabaseConnection
from user_authentication import UserAuthentication
from prolog_integration import PrologIntegration
from main_menu import MainMenu
from gpa_alert import GPAAlert
import logging

def main():
    logging.basicConfig(level=logging.DEBUG)  # Set to DEBUG level for more detailed logs
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

        # GPA alert setup
        smtp_server = "smtp.gmail.com"
        port = 587
        login = "damaryp90@gmail.com"
        password = "rpmz cbtz jdqr nega"
        gpa_alert = GPAAlert(db, smtp_server, port, login, password)

        # Main menu setup
        main_menu = MainMenu(db, auth, prolog)
        main_menu.display_menu()

        # Check and send GPA alerts
        default_gpa = prolog.get_default_gpa()
        logger.debug(f"Default GPA: {default_gpa}")
        students_below_gpa = gpa_alert.get_students_below_gpa(default_gpa)
        logger.debug(f"Students below GPA: {students_below_gpa}")
        
        if students_below_gpa:
            gpa_alert.send_email_alerts(students_below_gpa)
            logger.info("Email alerts sent successfully.")
        else:
            logger.info("No students below the GPA threshold. No emails sent.")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        # Close the database connection
        db.close()
        logger.info("Database connection closed.")

if __name__ == "__main__":
    main()