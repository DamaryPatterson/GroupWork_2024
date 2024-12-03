from pyswip import Prolog
import logging

class PrologIntegration:
    def __init__(self, prolog_script):
        self.prolog_script = prolog_script
        self.prolog = Prolog()
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

    def calculate_gpa(self, grade_points, credits):
        """
        Calculate GPA using Prolog
        
        :param grade_points: List of grade points
        :param credits: List of credits
        :return: Calculated GPA
        """
        self.prolog.consult(self.prolog_script)
        
        grade_points_str = ','.join(map(str, grade_points))
        credits_str = ','.join(map(str, credits))
        
        query = f"calculate_gpa([{grade_points_str}], [{credits_str}], GPA)"
        result = list(self.prolog.query(query))
        
        return result[0]['GPA'] if result else None

    def update_default_gpa(self, new_gpa):
        """
        Update the default GPA threshold in the Prolog script
        
        :param new_gpa: New GPA threshold value
        """
        self.prolog.consult(self.prolog_script)
        self.logger.debug(f"Attempting to update default GPA to {new_gpa}")
        
        # Verify the query works
        update_query = f"update_default_gpa({new_gpa})"
        result = list(self.prolog.query(update_query))
        self.logger.debug(f"Update query result: {result}")
        
        # Immediately verify the update
        verify_query = "default_gpa(GPA)"
        verify_result = list(self.prolog.query(verify_query))
        self.logger.debug(f"Verification query result: {verify_result}")

    def get_default_gpa(self):
        """
        Retrieve the current default GPA threshold
        
        :return: Current default GPA threshold
        """
        self.prolog.consult(self.prolog_script)
        result = list(self.prolog.query("default_gpa(GPA)"))
        
        if result:
            return result[0]['GPA']
        return 2.0  # Default GPA if not set
    
    def query(self, query_str):
        """
        Execute a Prolog query
        
        :param query_str: Prolog query string to execute
        :return: List of results
        """
        self.prolog.consult(self.prolog_script)
        return list(self.prolog.query(query_str))

    def letter_to_grade_point(self, letter_grade):
        query = "SELECT GradePoint FROM LetterGrades WHERE LetterGrade = %s"
        result = self.db.execute_query(query, (letter_grade,))
        if result:
            return result[0][0]
        else:
            return None