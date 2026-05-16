import os

write_file_schema = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "writes content to a file within the working directory. If the file already exists, it will be overwritten. If the file does not exist, it will be created along with any necessary parent directories.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file to write, relative to the working directory. This is a required parameter."
                },
                "content": {
                    "type": "string",
                    "description": "The content to write to the file. This is a required parameter."
                }
            },
            "required": ["file_path", "content"]
        }
    }
}


def write_file(working_directory, file_path, content):
    absolute_path = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(absolute_path, file_path))
    valid_path = os.path.commonpath(
        [absolute_path, target_file]) == absolute_path
    if not valid_path:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if os.path.exists(target_file) and os.path.isdir(target_file):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    os.makedirs(os.path.dirname(target_file), exist_ok=True)
    with open(target_file, "w") as f:
        f.write(content)
    return f'File "{file_path}" has been written successfully.'
