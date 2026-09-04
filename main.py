import argparse
import os
import sys
from typing import cast

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

from call_function import available_functions, call_function
from prompts import system_prompt

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")


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

    messages: list[ChatCompletionMessageParam] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    # maximum iterations for token reasons
    for _ in range(20):
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions,
        )

        message = response.choices[0].message
        messages.append(
            cast(ChatCompletionMessageParam, message.model_dump(exclude_none=True))
        )

        if args.verbose:
            if response.usage is not None:
                print(f"Prompt tokens: {response.usage.prompt_tokens}")
                print(f"Response tokens: {response.usage.completion_tokens}")
            else:
                raise RuntimeError("Response usage information is not available")

        if message.tool_calls:
            for tool_call in message.tool_calls:
                if tool_call.type != "function":
                    raise RuntimeError(f"Unsupported tool call type: {tool_call.type}")
                result_message = call_function(tool_call, verbose=args.verbose)
                if not result_message["content"]:
                    raise RuntimeError("Function call returned empty content")
                messages.append(result_message)
                if args.verbose:
                    print(f"-> {result_message['content']}")
        else:
            print(f"Final response:\n{message.content}")
            return

    print(f"Error: Agent exceeded iterations limit without a final response.")
    sys.exit(1)

if __name__ == "__main__":
    main()
