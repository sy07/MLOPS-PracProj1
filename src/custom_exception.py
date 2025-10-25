import traceback
import sys

class CustomException(Exception):
    def __init__(self, error_message, error_detail:sys):
        super().__init__(error_message)
        self.error_message = self.get_detailed_error_message(error_message, error_detail)

    @staticmethod
    def get_detailed_error_message(error_message, error_detail:sys):
        exc_type, exc_value, exc_tb = error_detail.exc_info()
        if exc_tb is not None:
            file_name = exc_tb.tb_frame.f_code.co_filename
            line_number = exc_tb.tb_lineno
            return f"Error occurred in {file_name}, line {line_number}: {error_message}"
        else:
            # fallback if no traceback is available
            return f"Error: {error_message}"


        return f"Error Occured in {file_name}, line {line_number} : {error_message}"
    

    def __str__(self):
        return self.error_message
