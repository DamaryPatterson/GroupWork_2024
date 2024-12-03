import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

class GPAAlert:
    def __init__(self, db, smtp_server, port, login, password):
        self.db = db
        self.smtp_server = smtp_server
        self.port = port
        self.login = login
        self.password = password
        self.logger = logging.getLogger(__name__)

    def get_students_below_gpa(self, default_gpa):
        query = """
        SELECT s.StudentID, s.StudentName, s.StudentEmail, s.ProgrammeID, s.School, 
               p.ProgrammeName, a.AdvisorName, a.Email AS AdvisorEmail, pd.ProgrammeDirectorName, 
               pd.ProgrammeDirectorEmail, fa.AdminName AS FacultyAdminName, fa.AdminEmail AS FacultyAdminEmail
        FROM Students s
        JOIN Programmes p ON s.ProgrammeID = p.ProgrammeID
        LEFT JOIN Advisors a ON s.AdvisorID = a.AdvisorID
        LEFT JOIN ProgrammeDirectors pd ON p.ProgrammeID = pd.ProgrammeID
        LEFT JOIN Admins fa ON fa.AdminID = 1 -- Assuming there's a single faculty admin
        WHERE (SELECT AVG(lg.GradePoint) 
               FROM Grades g 
               JOIN LetterGrades lg ON g.LetterGrade = lg.LetterGrade 
               WHERE g.StudentID = s.StudentID) <= %s
        """
        self.logger.debug("Executing query to get students below GPA threshold.")
        students = self.db.execute_query(query, (default_gpa,))
        self.logger.debug(f"Query executed. Number of students found: {len(students)}")
        return students

    def send_email_alerts(self, students):
        for student in students:
            student_id, student_name, student_email, programme_id, school, programme_name, advisor_name, advisor_email, programme_director_name, programme_director_email, faculty_admin_name, faculty_admin_email = student
            
            subject = "Academic Probation Alert"
            body = f"""
            Dear {student_name},

            Your current GPA is below the required threshold. Please contact your advisor for further assistance.

            Programme: {programme_name}
            School: {school}

            Regards,
            University Administration
            """
            
            message = MIMEMultipart()
            message["From"] = self.login
            message["To"] = student_email
            message["Cc"] = ", ".join(filter(None, [advisor_email, programme_director_email, faculty_admin_email]))
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain"))
            
            try:
                self.logger.debug(f"Connecting to SMTP server: {self.smtp_server}:{self.port}")
                with smtplib.SMTP(self.smtp_server, self.port) as server:
                    server.starttls()
                    self.logger.debug("Starting TLS.")
                    server.login(self.login, self.password)
                    self.logger.debug("Logged in to SMTP server.")
                    server.sendmail(self.login, [student_email, advisor_email, programme_director_email, faculty_admin_email], message.as_string())
                    self.logger.info(f"Alert sent to {student_name} and relevant parties.")
            except Exception as e:
                self.logger.error(f"Failed to send email to {student_name}: {e}")