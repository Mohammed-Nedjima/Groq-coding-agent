# PYTHON_ARGCOMPLETE_OK
import argparse
import os
from dotenv import load_dotenv
from groq import Groq
from yaspin import yaspin
# import argcomplete
# from argcomplete.completers import ChoicesCompleter


# AVAILABLE_MODELS = [
#     "llama-3.3-70b-versatile",
#     "llama-3.1-8b-instant",
#     "mixtral-8x7b-32768",
# ]

def print_chat_completion(user_prompt, chat_completion, stream, verbose=False):
    if stream:
        for chunk in chat_completion:
            if chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="", flush=True)
        print()
        return

    content = chat_completion.choices[0].message.content
    if content:
        print(f"User prompt: {user_prompt}")
        # print(f"Model response: {content}")
        print("Prompt tokens:", chat_completion.usage.prompt_tokens)
        print("Response tokens:", chat_completion.usage.completion_tokens)

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    # model_argument = parser.add_argument(
    #     "-m",
    #     "--model",
    #     choices=AVAILABLE_MODELS,
    #     default="llama-3.3-70b-versatile",
    #     help="Model name to use.",
    # )
    # model_argument.completer = ChoicesCompleter(AVAILABLE_MODELS)
    # argcomplete.autocomplete(parser)
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
    
    stream = not args.verbose
    with yaspin(text="Waiting for model response...", spinner="dots") as spinner:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": args.user_prompt,
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=1,
            max_completion_tokens=1024,
            top_p=1,
            stream=stream,
            stop=None
        )
    print_chat_completion(args.user_prompt, chat_completion, stream=stream, verbose=args.verbose)
if __name__ == "__main__":
    main()
