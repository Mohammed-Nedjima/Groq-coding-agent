# PYTHON_ARGCOMPLETE_OK
import argparse
import os
from dotenv import load_dotenv
from groq import APIConnectionError, APIError, BadRequestError, Groq
from httpcore import stream
from yaspin import yaspin
from call_function import execute_function_call
from functions.get_file_content import get_file_content, get_file_content_schema
from functions.get_files_info import get_files_info, get_files_info_schema
from functions.write_file import write_file, write_file_schema
from functions.run_python_file import run_python_file, run_python_file_schema
from prompts import system_prompt

MODEL = "openai/gpt-oss-120b"
MAX_ITERATIONS = 10
TOOL_CALL_RETRY_ATTEMPTS = 3
TOOLS = [
    get_file_content_schema,
    get_files_info_schema,
    write_file_schema,
    run_python_file_schema,
]


# def print_chat_completion(user_prompt, chat_completion, verbose=False):
#     # if stream:
#     #     for chunk in chat_completion:
#     #         if chunk.choices[0].delta.content:
#     #             print(chunk.choices[0].delta.content, end="", flush=True)
#     #     print()
#     #     return

#     content = chat_completion.choices[0].message.content
#     if content:
#         if verbose:
#             print(f"User prompt: {user_prompt}")
#             print("Prompt tokens:", chat_completion.usage.prompt_tokens)
#             print("Response tokens:", chat_completion.usage.completion_tokens)
#         print(f"Model response: {content}")


def run_agent(client, user_prompt, verbose=False):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    for iteration in range(MAX_ITERATIONS):
        response = None
        last_error = None
        for attempt in range(TOOL_CALL_RETRY_ATTEMPTS):
            try:
                with yaspin(text="Waiting for model response...", spinner="dots"):
                    response = client.chat.completions.create(
                        messages=messages,
                        model=MODEL,
                        temperature=0.3,
                        max_completion_tokens=1024,
                        top_p=1,
                        stop=None,
                        tools=TOOLS,
                    )
                break
            except APIConnectionError as e:
                last_error = f"Error: Could not reach Groq's API (network issue): {e}"
            except BadRequestError as e:
                last_error = e
                if verbose:
                    print(
                        f" (tool call generation malformed, retry {attempt + 1}/{TOOL_CALL_RETRY_ATTEMPTS})")
                    continue
            except APIError as e:
                return f"Error: Groq API request failed: {e}"
        if response is None:
            return f"Error: Groq API request failed: {last_error}"

        response_message = response.choices[0].message

        if verbose:
            print(f"Iteration {iteration + 1}")
            print("Prompt tokens:", response.usage.prompt_tokens)
            print("Response tokens:", response.usage.completion_tokens)

        # Model is done no more tool calls.
        if not response_message.tool_calls:
            return response_message.content

        messages.append(response_message)

        for tool_call in response_message.tool_calls:
            tool_result_message = execute_function_call(
                tool_call, verbose=verbose)
            messages.append(tool_result_message)

    return "Max iterations reached without a final answer."


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables.")

    client = Groq()
    try:
        final_answer = run_agent(
            client, args.user_prompt, verbose=args.verbose)
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")
        return

    print(f"Model response answer: {final_answer}")


if __name__ == "__main__":
    main()
