import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from database_connection import DatabaseConnection
from user_authentication import UserAuthentication
from prolog_integration import PrologIntegration
from gpa_alert import GPAAlert
from student_operations import StudentOperations
from admin_operation import AdminOperations
from programme_director_operations import ProgrammeDirectorOperations
from lecturer_operation import LecturerOperations

class GPACalculatorGUI:
    def __init__(self, root, db, auth, prolog, gpa_alert):
        self.root = root
        self.db = db
        self.auth = auth
        self.prolog = prolog
        self.gpa_alert = gpa_alert

        self.student_ops = StudentOperations(db, prolog)
        self.admin_ops = AdminOperations(db, prolog)
        self.programme_director_ops = ProgrammeDirectorOperations(db, prolog)
        self.lecturer_ops = LecturerOperations(db, prolog)

        self.root.title("GPA Calculator System")
        self.root.geometry("1000x700")  # Set the window size to 1000x700
        self.create_tabs()

    def create_tabs(self):
        style = ttk.Style()
        style.configure('TNotebook.Tab', font=('Arial', '12', 'bold'))
        
        tab_control = ttk.Notebook(self.root)

        # Create tabs for each user type
        student_tab = ttk.Frame(tab_control)
        admin_tab = ttk.Frame(tab_control)
        programme_director_tab = ttk.Frame(tab_control)
        lecturer_tab = ttk.Frame(tab_control)

        tab_control.add(student_tab, text="Student")
        tab_control.add(admin_tab, text="Admin")
        tab_control.add(programme_director_tab, text="Programme Director")
        tab_control.add(lecturer_tab, text="Lecturer")

        tab_control.pack(expand=1, fill="both")

        # Add content to each tab
        self.create_student_tab(student_tab)
        self.create_admin_tab(admin_tab)
        self.create_programme_director_tab(programme_director_tab)
        self.create_lecturer_tab(lecturer_tab)

    def create_student_tab(self, tab):
        label = ttk.Label(tab, text="Student Operations", font=("Arial", 16))
        label.pack(pady=20)

        view_report_button = ttk.Button(tab, text="View Report", command=self.view_student_report)
        view_report_button.pack(pady=10)

    def create_admin_tab(self, tab):
        label = ttk.Label(tab, text="Admin Operations", font=("Arial", 16))
        label.pack(pady=20)

        add_advisor_button = ttk.Button(tab, text="Add Advisor", command=self.add_advisor)
        add_advisor_button.pack(pady=10)

    def create_programme_director_tab(self, tab):
        label = ttk.Label(tab, text="Programme Director Operations", font=("Arial", 16))
        label.pack(pady=20)

        view_programme_details_button = ttk.Button(tab, text="View Programme Details", command=self.view_programme_details)
        view_programme_details_button.pack(pady=10)

        assign_advisor_button = ttk.Button(tab, text="Assign Advisor to Student", command=self.assign_advisor_to_student)
        assign_advisor_button.pack(pady=10)

    def create_lecturer_tab(self, tab):
        label = ttk.Label(tab, text="Lecturer Operations", font=("Arial", 16))
        label.pack(pady=20)

        submit_grades_button = ttk.Button(tab, text="Submit Module Grades", command=self.submit_module_grades)
        submit_grades_button.pack(pady=10)

    def view_student_report(self):
        student_id = simpledialog.askstring("Input", "Enter Student ID:")
        if student_id:
            self.student_ops.view_student_report(student_id)

    def add_advisor(self):
        advisor_name = simpledialog.askstring("Input", "Enter Advisor Name:")
        email = simpledialog.askstring("Input", "Enter Advisor Email:")
        if advisor_name and email:
            self.admin_ops.add_advisor(advisor_name, email)

    def view_programme_details(self):
        self.programme_director_ops.view_programme_details()

    def assign_advisor_to_student(self):
        student_id = simpledialog.askstring("Input", "Enter Student ID:")
        advisor_id = simpledialog.askstring("Input", "Enter Advisor ID:")
        if student_id and advisor_id:
            self.programme_director_ops.assign_advisor_to_student(student_id, advisor_id)

    def submit_module_grades(self):
        lecturer_id = simpledialog.askstring("Input", "Enter Lecturer ID:")
        if lecturer_id:
            self.lecturer_ops.submit_module_grades(lecturer_id)

def main():
    # Database connection setup
    db = DatabaseConnection(host="localhost", user="root", password="Abc123@!", database="GPA_Calculator")
    db.connect()

    # User authentication setup
    auth = UserAuthentication(db)

    # Prolog integration setup
    prolog = PrologIntegration("gpa_calculator.pl")

    # GPA alert setup
    smtp_server = "smtp.gmail.com"
    port = 587
    login = "utechacademicprobation@gmail.com"
    password = "utechprobation"
    gpa_alert = GPAAlert(db, smtp_server, port, login, password)

    # Create the main window
    root = tk.Tk()
    app = GPACalculatorGUI(root, db, auth, prolog, gpa_alert)
    
    # Run the application
    root.mainloop()

    # Close the database connection
    db.close()

if __name__ == "__main__":
    main()