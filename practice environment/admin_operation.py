class AdminOperations:
    def __init__(self, db, prolog):
        self.db = db
        self.prolog = prolog

    def display_menu(self):
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
                self.create_record()
            elif choice == '2':
                self.read_record()
            elif choice == '3':
                self.update_record()
            elif choice == '4':
                self.delete_record()
            elif choice == '5':
                self.view_default_gpa()
            elif choice == '6':
                self.update_default_gpa()
            elif choice == '7':
                break
            else:
                print("Invalid choice. Please try again.")

    def suggest_tables(self):
        tables = ["Students", "StudentUsers", "AdminUsers", "ProgrammeDirectorUsers", "LecturerUsers", "Grades", "Modules", "ProgrammeModules"]
        print("Available tables:")
        for i, table in enumerate(tables, 1):
            print(f"{i}. {table}")
        choice = int(input("Select a table by number: "))
        return tables[choice - 1]

    def prompt_for_data(self, table):
        data = {}
        if table == "Students":
            data["StudentID"] = input("Enter Student ID: ")
            data["StudentName"] = input("Enter Student Name: ")
            data["ProgrammeID"] = input("Enter Programme ID: ")
        elif table == "StudentUsers":
            data["UserID"] = input("Enter User ID: ")
            data["StudentID"] = input("Enter Student ID: ")
            data["Password"] = input("Enter Password: ")
        # Add prompts for other tables as needed
        return data

    def create_record(self):
        table = self.suggest_tables()
        data = self.prompt_for_data(table)
        columns = ", ".join(data.keys())
        values = ", ".join(f"'{v}'" for v in data.values())

        # Check for foreign key constraints
        if table == "StudentUsers":
            if not self.record_exists("Students", f"StudentID = '{data['StudentID']}'"):
                print("Error: StudentID does not exist. Please create the student first.")
                return

        query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
        self.db.execute_update(query)
        print("Record created successfully!")

    def read_record(self):
        table = self.suggest_tables()
        condition = input("Enter condition (e.g., 'StudentID=1001'): ")
        query = f"SELECT * FROM {table} WHERE {condition}"
        results = self.db.execute_query(query)
        for result in results:
            print(result)

    def update_record(self):
        table = self.suggest_tables()
        updates = input("Enter updates (e.g., 'StudentName=\"John\"'): ")
        condition = input("Enter condition (e.g., 'StudentID=1001'): ")
        query = f"UPDATE {table} SET {updates} WHERE {condition}"
        self.db.execute_update(query)
        print("Record updated successfully!")

    def delete_record(self):
        table = self.suggest_tables()
        condition = input("Enter condition (e.g., 'StudentID=1001'): ")
        query = f"DELETE FROM {table} WHERE {condition}"
        self.db.execute_update(query)
        print("Record deleted successfully!")

    def view_default_gpa(self):
        threshold = self.prolog.get_default_gpa()
        print(f"Current Default GPA: {threshold:.2f}")

    def update_default_gpa(self):
        new_gpa = float(input("Enter new default GPA: "))
        self.prolog.update_default_gpa(new_gpa)
        print("Default GPA updated successfully!")

    def record_exists(self, table, condition):
        query = f"SELECT 1 FROM {table} WHERE {condition} LIMIT 1"
        results = self.db.execute_query(query)
        return len(results) > 0