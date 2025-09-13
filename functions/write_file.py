import os 
from google.genai import types
def write_file(working_directory, file_path, content):
    try:
        working_abs_path = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(working_directory, file_path))

        if not full_path.startswith(working_abs_path):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, "w") as f:
                f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        
    except Exception as e:
        return f"Error: {e}"
    
schema_write_file= types.FunctionDeclaration(
    name="write_file",
    description="Write or overwrite a file with the given content.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path of the file to write."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write into the file."
    ),
        },
         required=["file_path", "content"],
),
)