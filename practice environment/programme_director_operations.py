from admin_operation import AdminOperations


from tabulate import tabulate

class ProgrammeDirectorOperations:
    def __init__(self, db, prolog):
        self.db = db
        self.prolog = prolog
        self.admin_ops = AdminOperations(db, prolog)

    def display_menu(self):
        while True:
            print("\nProgramme Director Operations")
            print("1. View Programme Details")
            print("2. View Student Performance")
            print("3. Generate Programme Performance Report")
            print("4. Manage Programme Modules")
            print("5. Back to Main Menu")
            choice = input("Enter your choice: ")
            if choice == '1':
                self.view_programme_details()
            elif choice == '2':
                self.view_students_performance()
            elif choice == '3':
                self.generate_programme_performance_report()
            elif choice == '4':
                self.manage_programme_modules()
            elif choice == '5':
                break
            else:
                print("Invalid choice. Please try again.")

    def view_programme_details(self):
        query = """
        SELECT p.ProgrammeID, p.ProgrammeName, p.School, 
        COUNT(DISTINCT s.StudentID) AS TotalStudents,
        COUNT(DISTINCT pm.Module) AS TotalModules
        FROM Programmes p
        LEFT JOIN Students s ON p.ProgrammeID = s.ProgrammeID
        LEFT JOIN ProgrammeModules pm ON p.ProgrammeID = pm.ProgrammeID
        GROUP BY p.ProgrammeID, p.ProgrammeName, p.School
        """
        results = self.db.execute_query(query)
        
        if results:
            headers = ["ID", "Name", "School", "Total Students", "Total Modules"]
            table = tabulate(results, headers, tablefmt="grid")
            print("\nProgramme Details:")
            print(table)
        else:
            print("No programme details found.")

    def view_students_performance(self):
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
        results = self.db.execute_query(query, (programme_id,))
        
        if results:
            headers = ["Student ID", "Name", "Average GPA"]
            table = tabulate(results, headers, tablefmt="grid")
            print(f"\nStudent Performance for Programme {programme_id}:")
            print(table)
        else:
            print(f"No students found for Programme {programme_id}.")

    def generate_programme_performance_report(self):
        programme_id = input("Enter Programme ID to generate performance report: ")
        
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
        programme_stats = self.db.execute_query(query, (programme_id,))
        
        default_gpa = self.prolog.get_default_gpa()
        
        if programme_stats:
            stats = programme_stats[0]
            headers = ["Programme", "Total Students", "Average GPA", "Lowest GPA", "Highest GPA", "Default GPA Threshold"]
            table = tabulate([stats + (default_gpa,)], headers, tablefmt="grid")
            print("\n--- Programme Performance Report ---")
            print(table)
            
            if stats[2] < default_gpa:
                print("\n!!! WARNING: Programme Performance Below Threshold !!!")
        else:
            print(f"No data found for Programme {programme_id}.")

    def manage_programme_modules(self):
        programme_id = input("Enter Programme ID to manage modules: ")
        
        while True:
            print("\nManage Programme Modules")
            print("1. View Current Modules")
            print("2. Add Module to Programme")
            print("3. Remove Module from Programme")
            print("4. Back to Previous Menu")
            
            choice = input("Enter your choice: ")
            
            if choice == '1':
                self.view_programme_modules(programme_id)
            elif choice == '2':
                self.add_module_to_programme(programme_id)
            elif choice == '3':
                self.remove_module_from_programme(programme_id)
            elif choice == '4':
                break
            else:
                print("Invalid choice. Please try again.")

    def view_programme_modules(self, programme_id):
        query = """
        SELECT m.Module, m.NumberOfCredits
        FROM Modules m
        JOIN ProgrammeModules pm ON m.Module = pm.Module
        WHERE pm.ProgrammeID = %s
        """
        results = self.db.execute_query(query, (programme_id,))
        
        if results:
            headers = ["Module Name", "Credits"]
            table = tabulate(results, headers, tablefmt="grid")
            print(f"\nModules for Programme {programme_id}:")
            print(table)
        else:
            print(f"No modules found for Programme {programme_id}.")

    def add_module_to_programme(self, programme_id):
        module = input("Enter Module Code to add: ")
        
        # Check if module exists
        if not self.admin_ops.record_exists("Modules", f"Module = '{module}'"):
            print("Error: Module does not exist. Create the module first.")
            return
        
        # Check if module is already in programme
        if self.admin_ops.record_exists("ProgrammeModules", f"ProgrammeID = {programme_id} AND Module = '{module}'"):
            print("Error: Module already exists in this programme.")
            return
        
        query = "INSERT INTO ProgrammeModules (ProgrammeID, Module) VALUES (%s, %s)"
        self.db.execute_update(query, (programme_id, module))
        print(f"Module {module} added to Programme {programme_id} successfully!")

    def remove_module_from_programme(self, programme_id):
        module = input("Enter Module Code to remove: ")
        
        # Check if module is in programme
        if not self.admin_ops.record_exists("ProgrammeModules", f"ProgrammeID = {programme_id} AND Module = '{module}'"):
            print("Error: Module not found in this programme.")
            return
        
        query = "DELETE FROM ProgrammeModules WHERE ProgrammeID = %s AND Module = %s"
        self.db.execute_update(query, (programme_id, module))
        print(f"Module {module} removed from Programme {programme_id} successfully!")