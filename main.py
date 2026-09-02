import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import system_prompt
from functions.get_files_info import schema_get_files_info
import json

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."

def main():
    print("Hello from ai-agent-python!")
    if api_key is None:
        raise RuntimeError("OPENROUTER_API_KEY environment variable is not set")
    
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    available_functions = [
        schema_get_files_info,
    ]

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions
    )

    message = response.choices[0].message
    if message.tool_calls:
        for tool_call in message.tool_calls:
            function_args = json.loads(tool_call.function.arguments or "{}")
            print(f"Calling function: {tool_call.function.name}({function_args})")
    else:
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            if response.usage is not None:
                print(f"Prompt tokens: {response.usage.prompt_tokens}")
                print(f"Response tokens: {response.usage.completion_tokens}")
            else:
                raise RuntimeError("Response usage information is not available")
        
        print(f"Response: {response.choices[0].message.content}")



if __name__ == "__main__":
    main()
