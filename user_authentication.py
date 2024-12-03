class UserAuthentication:
    def __init__(self, db_connection):
        self.db_connection = db_connection


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