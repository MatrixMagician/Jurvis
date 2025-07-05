import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Check if prompt argument is provided
if len(sys.argv) < 2:
    print("Error: Please provide a prompt as a command line argument.")
    print("Usage: uv run main.py \"Your prompt here\"")
    sys.exit(1)

# Get the prompt from command line arguments
user_prompt = sys.argv[1]

# Check for verbose flag
verbose = False
if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
    verbose = True

# Load environment variables from .env file
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

# Create a new instance of a Gemini client
client = genai.Client(api_key=api_key)

# Print user prompt if verbose mode is enabled
if verbose:
    print(f"User prompt: {user_prompt}")

# Create a new list of types.Content
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

# Generate content using the Gemini model but with messages
response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
)

# Print the model's response
print(response.text)

# Print token usage information
if verbose:
    print(f"\nPrompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
