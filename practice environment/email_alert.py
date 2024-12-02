import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging

class GPAAlertSystem:
    def __init__(self, smtp_config):
        """
        Initialize email alert system with SMTP configuration
        
        :param smtp_config: Dictionary containing SMTP server details
        """
        self.smtp_config = smtp_config
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def send_gpa_alert_emails(self, db, prolog, default_gpa):
        """
        Send GPA alert emails for students below default threshold
        
        :param db: Database connection object
        :param prolog: Prolog integration object
        :param default_gpa: Default GPA threshold
        """
        # Find students below or equal to default GPA
        query = """
        SELECT 
            s.StudentID, 
            s.StudentName, 
            s.StudentEmail,
            s.ProgrammeID,
            p.ProgrammeName,
            s.School,
            ROUND(AVG(g.GradePoints), 2) AS CumulativeGPA
        FROM 
            Students s
        JOIN 
            Grades g ON s.StudentID = g.StudentID
        JOIN
            Programmes p ON s.ProgrammeID = p.ProgrammeID
        GROUP BY 
            s.StudentID, s.StudentName, s.StudentEmail, s.ProgrammeID, p.ProgrammeName, s.School
        HAVING 
            CumulativeGPA <= %s
        """
        
        at_risk_students = db.execute_query(query, (default_gpa,))
        
        if not at_risk_students:
            self.logger.info("No students below GPA threshold.")
            return
        
        for student in at_risk_students:
            student_id, student_name, student_email, programme_id, programme_name, school, cumulative_gpa = student
            
            # Find student's advisor
            advisor_query = """
            SELECT LecturerEmail 
            FROM Lecturers l
            JOIN StudentAdvisors sa ON l.LecturerID = sa.AdvisorID
            WHERE sa.StudentID = %s
            """
            advisor_result = db.execute_query(advisor_query, (student_id,))
            
            # Find programme director email
            director_query = """
            SELECT ProgrammeDirectorEmail 
            FROM ProgrammeDirectors 
            WHERE ProgrammeID = %s
            """
            director_result = db.execute_query(director_query, (programme_id,))
            
            # Find faculty administrator email
            admin_query = """
            SELECT AdminEmail 
            FROM Admins 
            LIMIT 1
            """
            admin_result = db.execute_query(admin_query)
            
            # Compile email recipients
            recipients = [
                student_email,
                advisor_result[0][0] if advisor_result else None,
                director_result[0][0] if director_result else None,
                admin_result[0][0] if admin_result else None
            ]
            recipients = [r for r in recipients if r]  # Remove None values
            
            # Compose and send alert email
            subject = f"Academic Performance Alert - Student ID {student_id}"
            body = f"""
            Dear {student_name},

            This is an academic performance alert from the University of Technology.

            Your current cumulative GPA of {cumulative_gpa} is below the university's academic performance threshold of {default_gpa}.

            Programme Details:
            - Programme: {programme_name}
            - School: {school}

            We recommend you:
            1. Meet with your academic advisor
            2. Develop an academic improvement plan
            3. Utilize university support services

            Best regards,
            University Academic Support Team
            """
            
            self.send_email(recipients, subject, body)
            
            self.logger.info(f"Sent GPA alert for Student {student_id}")

    def send_email(self, recipients, subject, body):
        """
        Send email to multiple recipients
        
        :param recipients: List of email addresses
        :param subject: Email subject
        :param body: Email body
        """
        try:
            # Create message container
            msg = MIMEMultipart()
            msg['From'] = self.smtp_config['sender_email']
            msg['To'] = ', '.join(recipients)
            msg['Subject'] = subject

            # Attach body to email
            msg.attach(MIMEText(body, 'plain'))

            # Establish SMTP connection
            with smtplib.SMTP(
                self.smtp_config['smtp_server'], 
                self.smtp_config['smtp_port']
            ) as server:
                server.starttls()
                server.login(
                    self.smtp_config['sender_email'], 
                    self.smtp_config['sender_password']
                )
                server.sendmail(
                    self.smtp_config['sender_email'], 
                    recipients, 
                    msg.as_string()
                )
            
            self.logger.info(f"Email sent successfully to {len(recipients)} recipients")
        
        except Exception as e:
            self.logger.error(f"Email sending failed: {e}")

def initialize_gpa_alert_system(db, prolog):
    """
    Helper function to set up and trigger GPA alerts
    
    :param db: Database connection object
    :param prolog: Prolog integration object
    """
    # SMTP configuration (replace with actual values)
    smtp_config = {
        'smtp_server': 'smtp.example.com',
        'smtp_port': 587,
        'sender_email': 'alerts@university.edu',
        'sender_password': 'your_secure_password'
    }
    
    # Get current default GPA threshold
    default_gpa = prolog.get_default_gpa()
    
    # Create and run alert system
    alert_system = GPAAlertSystem(smtp_config)
    alert_system.send_gpa_alert_emails(db, prolog, default_gpa)

# Example integration in main.py
# In main function or after grade submissions:
# initialize_gpa_alert_system(db, prolog)