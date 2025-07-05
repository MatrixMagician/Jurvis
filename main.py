import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_functions import available_functions, call_function
from config import MAX_ITERS

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

# Main iteration loop
for iteration in range(MAX_ITERS):
    if verbose:
        print(f"\n--- Iteration {iteration + 1} ---")
    
    # Generate content using the Gemini model with system instructions and tools
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        ),
    )
    
    # Track if any function was called in this iteration
    function_called = False
    
    # Step 1: Check the .candidates property and add content to messages
    if response.candidates:
        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)
                
                # Check if this candidate contains function calls
                if candidate.content.parts:
                    for part in candidate.content.parts:
                        if hasattr(part, 'function_call') and part.function_call:
                            function_called = True
                            function_call_part = part.function_call
                            
                            if verbose:
                                print(f"Calling function: {function_call_part.name}")
                            
                            # Step 2: Call the function and append result to messages
                            function_call_result = call_function(function_call_part)
                            
                            # Check if the result has the expected structure
                            if (not hasattr(function_call_result, 'parts') or
                                len(function_call_result.parts) == 0 or
                                not hasattr(function_call_result.parts[0], 'function_response') or
                                not hasattr(function_call_result.parts[0].function_response, 'response')):
                                raise RuntimeError(f"Function call result does not have expected structure: {function_call_result}")
                            
                            # Add the function result to messages
                            messages.append(function_call_result)
                            
                            # Print the result if verbose mode is enabled
                            if verbose:
                                print(f"-> {function_call_result.parts[0].function_response.response}")
    
    # Step 3: Check if we should continue iterating or break
    if not function_called:
        # No function was called, so the agent is done
        # Print the LLM's final response
        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'text') and part.text:
                    print(part.text)
        elif hasattr(response, 'text') and response.text:
            print(response.text)
        break
    
    # If we've reached max iterations, break
    if iteration >= MAX_ITERS - 1:
        if verbose:
            print(f"\nReached maximum iterations ({MAX_ITERS})")
        break

# Print token usage information
if verbose:
    print(f"\nPrompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")