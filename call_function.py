import json
import os
from typing import TypedDict, Dict, Any
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.write_file import write_file
from functions.run_python_file import run_python_file

WORKING_DIRECTORY = "calculator"

available_functions = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "write_file": write_file,
    "run_python_file": run_python_file
}


def execute_function_call(tool_call: dict, verbose=False):
    function_name = getattr(tool_call.function, "name", None)
    function_to_call = available_functions.get(function_name)
    if not function_name:
        result = "Error: Model returned a tool call with no function name."
    elif not function_to_call:
        result = f"Error: Function '{function_name}' is not available."
    else:
        try:
            function_args = json.loads(tool_call.function.arguments)
        except json.JSONDecodeError as e:
            result = f"Error: Failed to parse function arguments for '{function_name}': {str(e)}"
        else:
            try:
                result = function_to_call(WORKING_DIRECTORY, **function_args)
            except Exception as e:
                result = f"Error: An exception occurred while executing '{function_name}': {str(e)}"
    if verbose:
        print(
            f"Function call: {function_name} with arguments: {function_args}")
        print(f"Result: {result}")
    # function_args = json.loads(tool_call.function.arguments)

    return {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": str(result)
    }
