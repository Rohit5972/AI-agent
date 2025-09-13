import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    try:
        working_abs_path = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(working_directory, file_path))

        if not full_path.startswith(working_abs_path):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(full_path):
            return f'Error: File "{file_path}" not found.'
        if not full_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        completed_process = subprocess.run(
            ["python3", full_path, *args],
            cwd=working_directory,
            capture_output=True,
            text=True,
            timeout=30
        )

      
        if completed_process.stdout.strip():
            return completed_process.stdout.strip()
        elif completed_process.stderr.strip():
            return completed_process.stderr.strip()
        else:
            return f"Process exited with code {completed_process.returncode}"

    except Exception as e:
        return f"Error: executing Python file: {e}"
    

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute a Python file with optional arguments.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path of the Python file to execute."
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional arguments to pass to the Python file.",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
        required=["file_path"],
    ),
)
