from tabulate import tabulate

class LecturerOperations:
    def __init__(self, db, prolog):
        self.db = db
        self.prolog = prolog

    def display_menu(self):
        while True:
            print("\nLecturer Operations")
            print("1. View Student Grades")
            print("2. Submit Module Grades")
            print("3. View Module Performance")
            print("4. Back to Main Menu")
            choice = input("Enter your choice: ")
            if choice == '1':
                self.view_module_student_grades()
            elif choice == '2':
                self.submit_module_grades()
            elif choice == '3':
                self.view_module_performance()
            elif choice == '4':
                break
            else:
                print("Invalid choice. Please try again.")

    def view_module_student_grades(self):
        lecturer_id = input("Enter Lecturer ID: ")
        
        # Query to get modules taught by the lecturer
        modules_query = """
        SELECT Module FROM LecturerModules 
        WHERE LecturerID = %s
        """
        lecturer_modules = self.db.execute_query(modules_query, (lecturer_id,))
        
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
        results = self.db.execute_query(query, (module,))
        
        if results:
            headers = ["Student ID", "Name", "Year", "Semester", "Grade Points", "Credits"]
            table = tabulate(results, headers, tablefmt="grid")
            print(f"\nGrades for Module {module}:")
            print(table)
        else:
            print(f"No grades found for module {module}.")

    def submit_module_grades(self):
        lecturer_id = input("Enter Lecturer ID: ")
        
        # Query to get modules taught by the lecturer
        modules_query = """
        SELECT lm.Module 
        FROM LecturerModules lm
        WHERE lm.LecturerID = %s
        """
        lecturer_modules = self.db.execute_query(modules_query, (lecturer_id,))
        
        if not lecturer_modules:
            print("No modules found for this lecturer.")
            return
        
        print("\nModules you teach:")
        for module in lecturer_modules:
            print(module[0])
        
        module = input("\nEnter module name to submit grades: ")
        
        # Verify the module belongs to the lecturer
        verify_query = "SELECT 1 FROM LecturerModules WHERE Module = %s AND LecturerID = %s"
        verify_result = self.db.execute_query(verify_query, (module, lecturer_id))
        
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
            grade_point_value = self.prolog.letter_to_grade_point(letter_grade)
            
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
            enrollment_check = self.db.execute_query(check_query, (student_id, module))
            
            if not enrollment_check:
                print(f"Error: Student {student_id} is not enrolled in module {module}.")
                continue
            
            # Insert or update grades
            query = """
            INSERT INTO Grades (StudentID, Module, Year, Semester, GradePoints) 
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE GradePoints = %s
            """
            self.db.execute_update(query, (student_id, module, year, semester, grade_point_value, grade_point_value))
            print(f"Grade {letter_grade} (Grade Points: {grade_point_value}) submitted for Student {student_id}")

    def view_module_performance(self):
        lecturer_id = input("Enter Lecturer ID: ")
        
        # Query to get modules taught by the lecturer
        modules_query = """
        SELECT m.Module, m.NumberOfCredits 
        FROM Modules m
        JOIN LecturerModules lm ON m.Module = lm.Module
        WHERE lm.LecturerID = %s
        """
        lecturer_modules = self.db.execute_query(modules_query, (lecturer_id,))
        
        if not lecturer_modules:
            print("No modules found for this lecturer.")
            return
        
        print("\nPerformance for Modules:")
        default_gpa = self.prolog.get_default_gpa()
        
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
            results = self.db.execute_query(query, (module_code,))
            
            if results and results[0][0] is not None:
                avg_grade, min_grade, max_grade, student_count = results[0]
                
                headers = ["Module", "Credits", "Students", "Average Grade Points", "Minimum Grade Points", "Maximum Grade Points"]
                table = tabulate([(module_code, credits, student_count, avg_grade, min_grade, max_grade)], headers, tablefmt="grid")
                print(table)
                
                # Performance assessment
                if avg_grade < default_gpa:
                    print("!!! WARNING: Module performance below default GPA threshold !!!")
            else:
                print(f"\nModule: {module_code}")
                print("No grades submitted yet.")