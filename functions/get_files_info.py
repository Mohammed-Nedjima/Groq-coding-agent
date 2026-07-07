import os

get_files_info_schema = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "gets information about files and directories in a directory",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "The directory to list files and directories for, relative to the working directory. Defaults to the working directory itself.",
                },
            }
        }
    }
}


def get_files_info(working_directory, directory="."):
    output = ""
    absolute_path = os.path.abspath(working_directory)
    target_path = os.path.normpath(os.path.join(absolute_path, directory))
    valid_path = os.path.commonpath(
        [absolute_path, target_path]) == absolute_path
    if not valid_path:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.exists(target_path):
        return f'Error: The directory "{directory}" does not exist'
    if not os.path.isdir(target_path):
        return f'Error: The path "{directory}" is not a directory'
    output += f'Success: "{directory}" is within the working directory\n'
    try:
        children_info = []
        for entry in os.listdir(target_path):
            entry_path = os.path.join(target_path, entry)
            child_info = {
                "name": entry,
                "size": os.path.getsize(entry_path),
                "is_directory": os.path.isdir(entry_path)
            }
            children_info.append(child_info)
        for child in children_info:
            output += f"- {child['name']}: file_size={child['size']} bytes, is_dir={child['is_directory']}\n"
    except OSError as exc:
        return f'Error: Could not inspect "{directory}": {exc}'
    return output
