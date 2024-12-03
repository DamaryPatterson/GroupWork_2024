from tabulate import tabulate

class StudentOperations:
    def __init__(self, db, prolog):
        self.db = db
        self.prolog = prolog


    def view_student_report(self, student_id):
        query = """
        SELECT Year, Semester, SUM(lg.GradePoint * m.NumberOfCredits) AS TotalGradePoints, 
        SUM(m.NumberOfCredits) AS TotalCredits
        FROM Grades g
        JOIN Modules m ON g.Module = m.Module
        JOIN LetterGrades lg ON g.LetterGrade = lg.LetterGrade
        WHERE g.StudentID = %s
        GROUP BY Year, Semester
        ORDER BY Year, Semester
        """
        results = self.db.execute_query(query, (student_id,))
        
        student_query = """
        SELECT StudentName, ProgrammeID 
        FROM Students 
        WHERE StudentID = %s
        """
        student_details = self.db.execute_query(student_query, (student_id,))
        
        if not student_details:
            print("No student found.")
            return
        
        student_name = student_details[0][0]
        default_gpa = self.prolog.get_default_gpa()
        
        if results:
            print("\n--- University of Technology ---")
            print("Academic Probation Alert GPA Report")
            print(f"Student ID: {student_id}")
            print(f"Name: {student_name}")
            print(f"Default GPA Threshold: {default_gpa}")
            print("\nSemester-wise Performance:")
            
            headers = ["Year", "Semester", "GPA"]
            table_data = []
            
            cumulative_grade_points = 0
            cumulative_credits = 0
            semester_details = {}
            
            for result in results:
                year, semester, total_grade_points, total_credits = result
                total_grade_points = float(total_grade_points)
                total_credits = float(total_credits)
                
                semester_gpa = total_grade_points / total_credits
                cumulative_grade_points += total_grade_points
                cumulative_credits += total_credits
                
                if year not in semester_details:
                    semester_details[year] = {}
                semester_details[year][semester] = semester_gpa
                
                table_data.append([year, semester, f"{semester_gpa:.2f}"])
            
            table = tabulate(table_data, headers, tablefmt="grid")
            print(table)
            
            cumulative_gpa = cumulative_grade_points / cumulative_credits
            print("\nCumulative GPA Summary:")
            print(f"Cumulative GPA: {cumulative_gpa:.2f}")
            
            if cumulative_gpa <= default_gpa:
                print("\n!!! ACADEMIC PROBATION ALERT !!!")
                print(f"Your Cumulative GPA ({cumulative_gpa:.2f}) is at or below the threshold of {default_gpa}")
                print("You may require additional academic support.")
            
            print("\nDetailed Semester Performance:")
            
            detailed_headers = ["Year", "Semester", "GPA"]
            detailed_table_data = []
            
            for year, semesters in semester_details.items():
                for semester, gpa in semesters.items():
                    detailed_table_data.append([year, semester, f"{gpa:.2f}"])
                    if gpa <= default_gpa:
                        detailed_table_data.append(["", "", "!!! Warning: Semester GPA below threshold !!!"])
            
            detailed_table = tabulate(detailed_table_data, detailed_headers, tablefmt="grid")
            print(detailed_table)
        else:
            print("No grades found for the given student ID.")