import os
import sys
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")


from google import genai
from google.genai import types


client = genai.Client(api_key=api_key)

def main(prompt):
    messages = [types.Content(role="user", parts=[types.Part(text=prompt)]),]
    response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents=messages,
)

    if "--verbose" in sys.argv[1:]:

        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    else:
        print(response.text)



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: uv run main.py <your_prompt>")
        sys.exit(1)
    main(sys.argv[1])