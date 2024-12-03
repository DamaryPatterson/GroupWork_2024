from database_connection import DatabaseConnection
from user_authentication import UserAuthentication
from prolog_integration import PrologIntegration
from main_menu import MainMenu

def main():
    # Database connection setup
    db = DatabaseConnection(host="localhost", user="root", password="Abc123@!", database="GPA_Calculator")
    db.connect()

    # User authentication setup
    auth = UserAuthentication(db)

    # Prolog integration setup
    prolog = PrologIntegration("gpa_calculator.pl")

    # Main menu setup
    main_menu = MainMenu(db, auth, prolog)
    main_menu.display_menu()

    # Close the database connection
    db.close()

if __name__ == "__main__":
    main()