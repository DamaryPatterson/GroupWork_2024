from admin_operation import AdminOperations
from lecturer_operation import LecturerOperations
from programme_director_operations import ProgrammeDirectorOperations
from student_operations import StudentOperations
import logging

class MainMenu:
    def __init__(self, db, auth, prolog):
        self.db = db
        self.auth = auth
        self.prolog = prolog
        self.lecturer_ops = LecturerOperations(db, prolog)
        self.admin_ops = AdminOperations(db, prolog)
        self.programme_director_ops = ProgrammeDirectorOperations(db, prolog)
        self.student_ops = StudentOperations(db, prolog)
        self.logger = logging.getLogger(__name__)

    def display_menu(self):
        while True:
            print("Welcome to the GPA Calculator System")
            print("1. Authenticate User")
            print("2. Exit")
            choice = input("Enter your choice: ")
            if choice == '1':
                self.authenticate_user()
            elif choice == '2':
                print("Exiting the system.")
                break
            else:
                print("Invalid choice. Please try again.")

    def authenticate_user(self):
        print("Select user type:")
        print("1. Student")
        print("2. Admin")
        print("3. Programme Director")
        print("4. Lecturer")
        user_type_choice = input("Enter your choice: ")
        user_type = self.get_user_type(user_type_choice)
        if user_type:
            user_id = input("Enter user ID: ")
            password = input("Enter password: ")
            try:
                self.logger.debug(f"Authenticating user: {user_id} of type: {user_type}")
                if self.auth.authenticate_user(user_type, user_id, password):
                    print("Authentication successful!")
                    self.handle_user_operations(user_type, user_id)
                else:
                    print("Authentication failed! Please check your user ID and password.")
            except Exception as e:
                self.logger.error(f"An error occurred during authentication: {e}")
                print("An error occurred during authentication. Please try again.")
        else:
            print("Invalid user type choice. Please select a valid option.")

    def get_user_type(self, choice):
        user_types = {
            '1': "StudentUsers",
            '2': "AdminUsers",
            '3': "ProgrammeDirectorUsers",
            '4': "LecturerUsers"
        }
        return user_types.get(choice)

    def handle_user_operations(self, user_type, user_id):
        try:
            self.logger.debug(f"Handling operations for user: {user_id} of type: {user_type}")
            if user_type == "StudentUsers":
                self.student_ops.view_student_report(student_id=user_id)
            elif user_type == "AdminUsers":
                self.admin_ops.display_menu()
            elif user_type == "ProgrammeDirectorUsers":
                self.programme_director_ops.display_menu()
            elif user_type == "LecturerUsers":
                self.lecturer_ops.display_menu()
        except Exception as e:
            self.logger.error(f"An error occurred while handling user operations: {e}")
            print("An error occurred while handling user operations. Please try again.")