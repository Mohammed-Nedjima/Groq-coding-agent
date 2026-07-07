import os
from config import MAX_READ_CHARACTERS


get_file_content_schema = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "reads the content of a file within the working directory, with a maximum character limit to prevent excessive output",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file to read, relative to the working directory. This is a required parameter."
                }
            },
            "required": ["file_path"]
        }
    }
}


def get_file_content(working_directory, file_path):
    absolute_path = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(absolute_path, file_path))
    valid_path = os.path.commonpath(
        [absolute_path, target_file]) == absolute_path
    if not valid_path:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(target_file) or not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    with open(target_file, "r") as f:
        content = f.read(MAX_READ_CHARACTERS + 1)
        if len(content) > MAX_READ_CHARACTERS:
            content = content[:MAX_READ_CHARACTERS]
            content += f'[...File "{file_path}" truncated at {MAX_READ_CHARACTERS} characters]'

    return content
