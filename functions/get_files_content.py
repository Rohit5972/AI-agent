import os
from functions.config import MAX_CHARS
def get_file_content(working_directory, file_path):
    try:
        full_path = os.path.join(working_directory,file_path)
        abs_working_dir = os.path.abspath(working_directory)  
        abs_full_path = os.path.abspath(full_path)
        if not abs_full_path.startswith(abs_working_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        

        with open(full_path, "r") as f:
            content = f.read(MAX_CHARS + 1) 

        if len(content) > MAX_CHARS:
            return content[:MAX_CHARS] + f'...[File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content
    except Exception as e:
        return f"Error: {str(e)}"