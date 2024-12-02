from database_connection import DatabaseConnection
from user_authentication import UserAuthentication
from prolog_integration import PrologIntegration

def main():
    # Database connection setup
    db = DatabaseConnection(host="localhost", user="root", password="Abc123@!", database="GPA_Calculator")
    db.connect()

    # User authentication setup
    auth = UserAuthentication(db)

    # Prolog integration setup
    prolog = PrologIntegration("gpa_calculator.pl")

    # Main menu
    while True:
        print("Welcome to the GPA Calculator System")
        print("1. Authenticate User")
        print("2. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            print("Select user type:")
            print("1. Student")
            print("2. Admin")
            print("3. Programme Director")
            print("4. Lecturer")
            user_type_choice = input("Enter your choice: ")
            user_type = get_user_type(user_type_choice)
            if user_type:
                user_id = input("Enter user ID: ")
                password = input("Enter password: ")
                if auth.authenticate_user(user_type, user_id, password):
                    print("Authentication successful!")
                    if user_type == "StudentUsers":
                        view_student_report(db, prolog, user_id)
                    elif user_type == "AdminUsers":
                        admin_operations(db, prolog)
                    elif user_type == "ProgrammeDirectorUsers":
                        programme_director_operations(db, prolog)
                    elif user_type == "LecturerUsers":
                        lecturer_operations(db, prolog)
                else:
                    print("Authentication failed!")
            else:
                print("Invalid user type choice.")

        elif choice == '2':
            print("Exiting the system.")
            break

        else:
            print("Invalid choice. Please try again.")

    db.close()

def get_user_type(choice):
    if choice == '1':
        return "StudentUsers"
    elif choice == '2':
        return "AdminUsers"
    elif choice == '3':
        return "ProgrammeDirectorUsers"
    elif choice == '4':
        return "LecturerUsers"
    else:
        return None

def lecturer_operations(db, prolog):
    while True:
        print("\nLecturer Operations")
        print("1. View Student Grades")
        print("2. Submit Module Grades")
        print("3. View Module Performance")
        print("4. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            view_module_student_grades(db)

        elif choice == '2':
            submit_module_grades(db,prolog)

        elif choice == '3':
            view_module_performance(db, prolog)

        elif choice == '4':
            break

        else:
            print("Invalid choice. Please try again.")

def view_module_student_grades(db):
    lecturer_id = input("Enter Lecturer ID: ")
    
    # Query to get modules taught by the lecturer
    modules_query = """
    SELECT Module FROM LecturerModules 
    WHERE LecturerID = %s
    """
    lecturer_modules = db.execute_query(modules_query, (lecturer_id,))
    
    if not lecturer_modules:
        print("No modules found for this lecturer.")
        return
    
    print("\nModules you teach:")
    for module in lecturer_modules:
        print(module[0])
    
    module = input("\nEnter module name to view student grades: ")
    
    # Query to fetch student grades for the selected module
    query = """
    SELECT s.StudentID, s.StudentName, g.Year, g.Semester, 
           g.GradePoints, m.NumberOfCredits
    FROM Students s
    JOIN Grades g ON s.StudentID = g.StudentID
    JOIN Modules m ON g.Module = m.Module
    WHERE g.Module = %s
    ORDER BY s.StudentID
    """
    results = db.execute_query(query, (module,))
    
    if results:
        print(f"\nGrades for Module {module}:")
        print("Student ID | Name | Year | Semester | Grade Points | Credits")
        print("-" * 70)
        for result in results:
            print(f"{result[0]} | {result[1]} | {result[2]} | {result[3]} | {result[4]} | {result[5]}")
    else:
        print(f"No grades found for module {module}.")

def submit_module_grades(db, prolog):
    lecturer_id = input("Enter Lecturer ID: ")
    
    # Query to get modules taught by the lecturer
    modules_query = """
    SELECT lm.Module 
    FROM LecturerModules lm
    WHERE lm.LecturerID = %s
    """
    lecturer_modules = db.execute_query(modules_query, (lecturer_id,))
    
    if not lecturer_modules:
        print("No modules found for this lecturer.")
        return
    
    print("\nModules you teach:")
    for module in lecturer_modules:
        print(module[0])
    
    module = input("\nEnter module name to submit grades: ")
    
    # Verify the module belongs to the lecturer
    verify_query = "SELECT 1 FROM LecturerModules WHERE Module = %s AND LecturerID = %s"
    verify_result = db.execute_query(verify_query, (module, lecturer_id))
    
    if not verify_result:
        print("You are not authorized to submit grades for this module.")
        return
    
    while True:
        student_id = input("Enter Student ID (or 'done' to finish): ")
        if student_id.lower() == 'done':
            break
        
        year = input("Enter Academic Year: ")
        semester = input("Enter Semester: ")
        letter_grade = input("Enter Letter Grade (e.g., A, B+, C-): ")
        
        # Convert letter grade to grade point using Prolog
        grade_point_value = prolog.letter_to_grade_point(letter_grade)
        
        if grade_point_value is None:
            print("Invalid letter grade entered. Please try again.")
            continue
        
        # Check if student is enrolled in this module
        check_query = """
        SELECT 1 
        FROM ProgrammeModules pm
        JOIN Students s ON pm.ProgrammeID = s.ProgrammeID
        WHERE s.StudentID = %s AND pm.Module = %s
        """
        enrollment_check = db.execute_query(check_query, (student_id, module))
        
        if not enrollment_check:
            print(f"Error: Student {student_id} is not enrolled in module {module}.")
            continue
        
        # Insert or update grades
        query = """
        INSERT INTO Grades (StudentID, Module, Year, Semester, GradePoints) 
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE GradePoints = %s
        """
        db.execute_update(query, (student_id, module, year, semester, grade_point_value, grade_point_value))
        print(f"Grade {letter_grade} (Grade Points: {grade_point_value}) submitted for Student {student_id}")

def view_module_performance(db, prolog):
    lecturer_id = input("Enter Lecturer ID: ")
    
    # Query to get modules taught by the lecturer
    modules_query = """
    SELECT m.Module, m.NumberOfCredits 
    FROM Modules m
    JOIN LecturerModules lm ON m.Module = lm.Module
    WHERE lm.LecturerID = %s
    """
    lecturer_modules = db.execute_query(modules_query, (lecturer_id,))
    
    if not lecturer_modules:
        print("No modules found for this lecturer.")
        return
    
    print("\nPerformance for Modules:")
    default_gpa = prolog.get_default_gpa()
    
    for module in lecturer_modules:
        module_code, credits = module
        
        # Query to calculate module performance
        query = """
        SELECT 
            ROUND(AVG(GradePoints), 2) AS AverageGrade,
            ROUND(MIN(GradePoints), 2) AS MinGrade,
            ROUND(MAX(GradePoints), 2) AS MaxGrade,
            COUNT(DISTINCT StudentID) AS StudentCount
        FROM Grades
        WHERE Module = %s
        """
        results = db.execute_query(query, (module_code,))
        
        if results and results[0][0] is not None:
            avg_grade, min_grade, max_grade, student_count = results[0]
            
            print(f"\nModule: {module_code}")
            print(f"Credits: {credits}")
            print(f"Students: {student_count}")
            print(f"Average Grade Points: {avg_grade}")
            print(f"Minimum Grade Points: {min_grade}")
            print(f"Maximum Grade Points: {max_grade}")
            
            # Performance assessment
            if avg_grade < default_gpa:
                print("!!! WARNING: Module performance below default GPA threshold !!!")
        else:
            print(f"\nModule: {module_code}")
            print("No grades submitted yet.")

def view_student_report(db, prolog, student_id):
    query = """
    SELECT Year, Semester, SUM(GradePoints * NumberOfCredits) AS TotalGradePoints, 
           SUM(NumberOfCredits) AS TotalCredits
    FROM Grades g
    JOIN Modules m ON g.Module = m.Module
    WHERE StudentID = %s
    GROUP BY Year, Semester
    ORDER BY Year, Semester
    """
    results = db.execute_query(query, (student_id,))
    if results:
        cumulative_grade_points = 0
        cumulative_credits = 0
        print("GPA Report")
        print("Year | Semester | GPA")
        for result in results:
            year, semester, total_grade_points, total_credits = result
            total_grade_points = float(total_grade_points)
            total_credits = float(total_credits)
            gpa = total_grade_points / total_credits
            cumulative_grade_points += total_grade_points
            cumulative_credits += total_credits
            print(f"{year} | {semester} | {gpa:.2f}")
        cumulative_gpa = cumulative_grade_points / cumulative_credits
        print(f"Cumulative GPA: {cumulative_gpa:.2f}")
        
        # Get default GPA threshold
        default_gpa = prolog.get_default_gpa()
        print(f"Default GPA Threshold: {default_gpa:.2f}")
        
        # Check if cumulative GPA is below threshold
        if cumulative_gpa < default_gpa:
            print("Warning: Your cumulative GPA is below the default threshold.")
    else:
        print("No grades found for the given student ID.")

def admin_operations(db, prolog):
    while True:
        print("Admin Operations")
        print("1. Create Record")
        print("2. Read Record")
        print("3. Update Record")
        print("4. Delete Record")
        print("5. View Default GPA")
        print("6. Update Default GPA")
        print("7. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            table = input("Enter table name: ")
            columns = input("Enter columns (comma-separated): ")
            values = input("Enter values (comma-separated): ")
            create_record(db, table, columns, values)

        elif choice == '2':
            table = input("Enter table name: ")
            condition = input("Enter condition (e.g., 'StudentID=1001'): ")
            read_record(db, table, condition)

        elif choice == '3':
            table = input("Enter table name: ")
            updates = input("Enter updates (e.g., 'StudentName=\"John\"'): ")
            condition = input("Enter condition (e.g., 'StudentID=1001'): ")
            update_record(db, table, updates, condition)

        elif choice == '4':
            table = input("Enter table name: ")
            condition = input("Enter condition (e.g., 'StudentID=1001'): ")
            delete_record(db, table, condition)

        elif choice == '5':
            threshold = prolog.get_default_gpa()
            print(f"Current Default GPA: {threshold:.2f}")

        elif choice == '6':
            new_gpa = float(input("Enter new default GPA: "))
            prolog.update_default_gpa(new_gpa)
            print("Default GPA updated successfully!")

        elif choice == '7':
            break

        else:
            print("Invalid choice. Please try again.")

def create_record(db, table, columns, values):
    # Check for foreign key constraints
    if table == "Students":
        programme_id = values.split(",")[4].strip()
        if not record_exists(db, "Programmes", f"ProgrammeID = {programme_id}"):
            print("Error: ProgrammeID does not exist. Please create the programme first.")
            return
    elif table == "Grades":
        student_id = values.split(",")[3].strip()
        module = values.split(",")[0].strip()
        if not record_exists(db, "Students", f"StudentID = {student_id}"):
            print("Error: StudentID does not exist. Please create the student first.")
            return
        if not record_exists(db, "Modules", f"Module = '{module}'"):
            print("Error: Module does not exist. Please create the module first.")
            return

    query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
    db.execute_update(query)
    print("Record created successfully!")

def read_record(db, table, condition):
    query = f"SELECT * FROM {table} WHERE {condition}"
    results = db.execute_query(query)
    for result in results:
        print(result)

def update_record(db, table, updates, condition):
    query = f"UPDATE {table} SET {updates} WHERE {condition}"
    db.execute_update(query)
    print("Record updated successfully!")

def delete_record(db, table, condition):
    query = f"DELETE FROM {table} WHERE {condition}"
    db.execute_update(query)
    print("Record deleted successfully!")

def record_exists(db, table, condition):
    query = f"SELECT 1 FROM {table} WHERE {condition} LIMIT 1"
    results = db.execute_query(query)
    return len(results) > 0

def programme_director_operations(db, prolog):
    while True:
        print("\nProgramme Director Operations")
        print("1. View Programme Details")
        print("2. View Student Performance")
        print("3. Generate Programme Performance Report")
        print("4. Manage Programme Modules")
        print("5. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            view_programme_details(db)

        elif choice == '2':
            view_students_performance(db)

        elif choice == '3':
            generate_programme_performance_report(db, prolog)

        elif choice == '4':
            manage_programme_modules(db)

        elif choice == '5':
            break

        else:
            print("Invalid choice. Please try again.")

def view_programme_details(db):
    query = """
    SELECT p.ProgrammeID, p.ProgrammeName, p.School, 
           COUNT(DISTINCT s.StudentID) AS TotalStudents,
           COUNT(DISTINCT pm.Module) AS TotalModules
    FROM Programmes p
    LEFT JOIN Students s ON p.ProgrammeID = s.ProgrammeID
    LEFT JOIN ProgrammeModules pm ON p.ProgrammeID = pm.ProgrammeID
    GROUP BY p.ProgrammeID, p.ProgrammeName, p.School
    """
    results = db.execute_query(query)
    
    if results:
        print("\nProgramme Details:")
        print("ID | Name | School | Total Students | Total Modules")
        print("-" * 60)
        for result in results:
            print(f"{result[0]} | {result[1]} | {result[2]} | {result[3]} | {result[4]}")
    else:
        print("No programme details found.")

def view_students_performance(db):
    programme_id = input("Enter Programme ID to view students' performance: ")
    
    query = """
    SELECT 
        s.StudentID, 
        s.StudentName, 
        ROUND(AVG(g.GradePoints), 2) AS AverageGPA
    FROM 
        Students s
    LEFT JOIN 
        Grades g ON s.StudentID = g.StudentID
    WHERE 
        s.ProgrammeID = %s
    GROUP BY 
        s.StudentID, s.StudentName
    ORDER BY 
        AverageGPA DESC
    """
    results = db.execute_query(query, (programme_id,))
    
    if results:
        print(f"\nStudent Performance for Programme {programme_id}:")
        print("Student ID | Name | Average GPA")
        print("-" * 40)
        for result in results:
            print(f"{result[0]} | {result[1]} | {result[2]}")
    else:
        print(f"No students found for Programme {programme_id}.")

def generate_programme_performance_report(db, prolog):
    programme_id = input("Enter Programme ID to generate performance report: ")
    
    # Get programme-level statistics
    query = """
    SELECT 
        p.ProgrammeName,
        COUNT(DISTINCT s.StudentID) AS TotalStudents,
        ROUND(AVG(g.GradePoints), 2) AS ProgrammeAverageGPA,
        ROUND(MIN(g.GradePoints), 2) AS LowestGPA,
        ROUND(MAX(g.GradePoints), 2) AS HighestGPA
    FROM 
        Programmes p
    LEFT JOIN 
        Students s ON p.ProgrammeID = s.ProgrammeID
    LEFT JOIN 
        Grades g ON s.StudentID = g.StudentID
    WHERE 
        p.ProgrammeID = %s
    GROUP BY 
        p.ProgrammeName
    """
    programme_stats = db.execute_query(query, (programme_id,))
    
    # Get default GPA threshold from Prolog
    default_gpa = prolog.get_default_gpa()
    
    if programme_stats:
        stats = programme_stats[0]
        print("\n--- Programme Performance Report ---")
        print(f"Programme: {stats[0]}")
        print(f"Total Students: {stats[1]}")
        print(f"Programme Average GPA: {stats[2]}")
        print(f"Lowest GPA: {stats[3]}")
        print(f"Highest GPA: {stats[4]}")
        print(f"Default GPA Threshold: {default_gpa}")
        
        # Check if programme is performing below threshold
        if stats[2] < default_gpa:
            print("\n!!! WARNING: Programme Performance Below Threshold !!!")
    else:
        print(f"No data found for Programme {programme_id}.")

def manage_programme_modules(db):
    programme_id = input("Enter Programme ID to manage modules: ")
    
    while True:
        print("\nManage Programme Modules")
        print("1. View Current Modules")
        print("2. Add Module to Programme")
        print("3. Remove Module from Programme")
        print("4. Back to Previous Menu")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            view_programme_modules(db, programme_id)
        
        elif choice == '2':
            add_module_to_programme(db, programme_id)
        
        elif choice == '3':
            remove_module_from_programme(db, programme_id)
        
        elif choice == '4':
            break
        
        else:
            print("Invalid choice. Please try again.")

def view_programme_modules(db, programme_id):
    query = """
    SELECT m.Module, m.NumberOfCredits
    FROM Modules m
    JOIN ProgrammeModules pm ON m.Module = pm.Module
    WHERE pm.ProgrammeID = %s
    """
    results = db.execute_query(query, (programme_id,))
    
    if results:
        print(f"\nModules for Programme {programme_id}:")
        print("Module Name | Credits")
        print("-" * 30)
        for result in results:
            print(f"{result[0]} | {result[1]}")
    else:
        print(f"No modules found for Programme {programme_id}.")

def add_module_to_programme(db, programme_id):
    module = input("Enter Module Code to add: ")
    
    # Check if module exists
    if not record_exists(db, "Modules", f"Module = '{module}'"):
        print("Error: Module does not exist. Create the module first.")
        return
    
    # Check if module is already in programme
    if record_exists(db, "ProgrammeModules", f"ProgrammeID = {programme_id} AND Module = '{module}'"):
        print("Error: Module already exists in this programme.")
        return
    
    query = "INSERT INTO ProgrammeModules (ProgrammeID, Module) VALUES (%s, %s)"
    db.execute_update(query, (programme_id, module))
    print(f"Module {module} added to Programme {programme_id} successfully!")

def remove_module_from_programme(db, programme_id):
    module = input("Enter Module Code to remove: ")
    
    # Check if module is in programme
    if not record_exists(db, "ProgrammeModules", f"ProgrammeID = {programme_id} AND Module = '{module}'"):
        print("Error: Module not found in this programme.")
        return
    
    query = "DELETE FROM ProgrammeModules WHERE ProgrammeID = %s AND Module = %s"
    db.execute_update(query, (programme_id, module))
    print(f"Module {module} removed from Programme {programme_id} successfully!")

if __name__ == "__main__":
    main()