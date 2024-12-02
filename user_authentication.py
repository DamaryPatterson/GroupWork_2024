class UserAuthentication:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def register_user(self, table, user_id, password):
        if table == "StudentUsers":
            student_name = input("Enter student name: ")
            student_email = input("Enter student email: ")
            school = input("Enter school: ")
            programme_id = input("Enter programme ID: ")
            if not self.record_exists("Programmes", f"ProgrammeID = {programme_id}"):
                print("Error: ProgrammeID does not exist. Please create the programme first.")
                return
            self.create_student(user_id, student_name, student_email, school, programme_id)
            query = "INSERT INTO StudentUsers (StudentID, PasswordHash) VALUES (%s, %s)"
        elif table == "AdminUsers":
            admin_name = input("Enter admin name: ")
            admin_email = input("Enter admin email: ")
            self.create_admin(user_id, admin_name, admin_email)
            query = "INSERT INTO AdminUsers (AdminID, PasswordHash) VALUES (%s, %s)"
        elif table == "ProgrammeDirectorUsers":
            director_name = input("Enter programme director name: ")
            director_email = input("Enter programme director email: ")
            programme_id = input("Enter programme ID: ")
            if not self.record_exists("Programmes", f"ProgrammeID = {programme_id}"):
                print("Error: ProgrammeID does not exist. Please create the programme first.")
                return
            self.create_programme_director(user_id, director_name, director_email, programme_id)
            query = "INSERT INTO ProgrammeDirectorUsers (ProgrammeDirectorID, PasswordHash) VALUES (%s, %s)"
        elif table == "LecturerUsers":
            lecturer_name = input("Enter lecturer name: ")
            lecturer_email = input("Enter school: ")
            school = input("Enter school: ")
            self.create_lecturer(user_id, lecturer_name, lecturer_email, school)
            query = "INSERT INTO LecturerUsers (LecturerID, PasswordHash) VALUES (%s, %s)"
        self.db_connection.execute_update(query, (user_id, password))
        print("User registered successfully!")

    def create_student(self, student_id, student_name, student_email, school, programme_id):
        query = "INSERT INTO Students (StudentID, StudentName, StudentEmail, School, ProgrammeID) VALUES (%s, %s, %s, %s, %s)"
        self.db_connection.execute_update(query, (student_id, student_name, student_email, school, programme_id))

    def create_admin(self, admin_id, admin_name, admin_email):
        query = "INSERT INTO Admins (AdminID, AdminName, AdminEmail) VALUES (%s, %s, %s)"
        self.db_connection.execute_update(query, (admin_id, admin_name, admin_email))

    def create_programme_director(self, director_id, director_name, director_email, programme_id):
        query = "INSERT INTO ProgrammeDirectors (ProgrammeDirectorID, ProgrammeDirectorName, ProgrammeDirectorEmail, ProgrammeID) VALUES (%s, %s, %s, %s)"
        self.db_connection.execute_update(query, (director_id, director_name, director_email, programme_id))

    def create_lecturer(self, lecturer_id, lecturer_name, lecturer_email, school):
        query = "INSERT INTO Lecturers (LecturerID, LecturerName, LecturerEmail, School) VALUES (%s, %s, %s, %s)"
        self.db_connection.execute_update(query, (lecturer_id, lecturer_name, lecturer_email, school))

    def authenticate_user(self, table, user_id, password):
        if table == "StudentUsers":
            query = "SELECT PasswordHash FROM StudentUsers WHERE StudentID = %s"
        elif table == "AdminUsers":
            query = "SELECT PasswordHash FROM AdminUsers WHERE AdminID = %s"
        elif table == "ProgrammeDirectorUsers":
            query = "SELECT PasswordHash FROM ProgrammeDirectorUsers WHERE ProgrammeDirectorID = %s"
        elif table == "LecturerUsers":
            query = "SELECT PasswordHash FROM LecturerUsers WHERE LecturerID = %s"
        result = self.db_connection.execute_query(query, (user_id,))
        if result:
            stored_password = result[0][0]
            return password == stored_password
        return False

    def record_exists(self, table, condition):
        query = f"SELECT 1 FROM {table} WHERE {condition} LIMIT 1"
        results = self.db_connection.execute_query(query)
        return len(results) > 0