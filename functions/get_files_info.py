import os


def get_files_info(working_directory, directory="."):
    output = ""
    absolute_path = os.path.abspath(working_directory)
    target_directory = os.path.normpath(os.path.join(absolute_path, directory))
    valid_path = os.path.commonpath(
        [absolute_path, target_directory]) == absolute_path
    if not valid_path:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.exists(target_directory):
        return f'Error: The directory "{directory}" does not exist'
    if not os.path.isdir(target_directory):
        return f'Error: The path "{directory}" is not a directory'
    children_info = []
    for entry in os.listdir(target_directory):
        entry_path = os.path.join(target_directory, entry)
        child_info = {
            "name": entry,
            "size": os.path.getsize(entry_path),
            "is_directory": os.path.isdir(entry_path)
        }
        children_info.append(child_info)
    for child in children_info:
        output += f"- {child['name']}: file_size={child['size']} bytes, is_dir={child['is_directory']}\n"
    return output
