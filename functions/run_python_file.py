import os
import subprocess

run_python_file_schema = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "executes a Python file within the working directory and captures its output. The function ensures that the file is a Python script and is located within the permitted working directory. It also allows passing optional command-line arguments to the script.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the Python file to execute, relative to the working directory. This is a required parameter."
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Optional command-line arguments to pass to the Python script."
                }
            },
            "required": ["file_path"]
        }
    }
}


def run_python_file(working_directory, file_path, args=None):
    absolute_path = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(absolute_path, file_path))
    valid_path = os.path.commonpath(
        [absolute_path, target_file]) == absolute_path
    if not valid_path:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(target_file) or not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    if not target_file.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'
    command = ["python3", target_file]
    if args:
        command.extend(args)
    try:
        completed_process = subprocess.run(
            args=command, capture_output=True, text=True, check=True, timeout=30, cwd=absolute_path)
    except subprocess.CalledProcessError as e:
        return f'Error: Python script "{file_path}" exited with non-zero status {e.returncode}\nStdout: {e.stdout}\nStderr: {e.stderr}'
    except subprocess.TimeoutExpired:
        return f'Error: Python script "{file_path}" timed out after 30 seconds'
    if not completed_process.stdout and not completed_process.stderr:
        return f'Python script "{file_path}" executed successfully with no output'
    return f'Python script "{file_path}" executed successfully\nStdout: {completed_process.stdout}\nStderr: {completed_process.stderr}'
