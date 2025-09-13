import os
import sys
from functions.get_file_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file


from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

from functions.get_file_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file


from google import genai
from google.genai import types


client = genai.Client(api_key=api_key)




def call_function(function_call_part, verbose=False):
    """
    Handles the abstract task of calling one of our four functions.
    """

    function_name = function_call_part.name
    function_args = dict(function_call_part.args)  

  
    function_args["working_directory"] = "./calculator"

   
    available_functions = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

   
    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

   
    if function_name not in available_functions:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

 
    try:
        result = available_functions[function_name](**function_args)
    except Exception as e:
        result = f"Exception while running {function_name}: {str(e)}"


    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": result},
            )
        ],
    )

def main(prompt):

    available_functions = types.Tool(
    function_declarations=[
    schema_get_files_info,schema_get_file_content,schema_run_python_file,schema_write_file,
    ]
)
    system_instructions ="""
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
    for _ in range(20):
        messages = [types.Content(role="user", parts=[types.Part(text=prompt)]),]
        response = client.models.generate_content(
        model='gemini-2.0-flash-001', contents=messages,config=types.GenerateContentConfig(tools=[available_functions],system_instruction=system_instructions),
        )


    
    
        if "--verbose" in sys.argv[1:]:

            print(f"User prompt: {prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        messages.append(response.candidates[0].content)

        if response.candidates[0].content.parts[0].text:
            print("Final response:")
            print(response.candidates[0].content.parts[0].text)
            break

        if response.candidates[0].content.parts[0].function_call:
            function_call_part = response.candidates[0].content.parts[0].function_call
            result_content = call_function(
            function_call_part,
            verbose="--verbose" in sys.argv[1:]
        )
            messages.append(result_content)
            print(result_content.parts[0].function_response.response["result"])
        else:
            print(response.text)

    


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: uv run main.py <your_prompt>")
        sys.exit(1)
    main(sys.argv[1])