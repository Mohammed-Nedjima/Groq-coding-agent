import re

from functions.get_files_info import get_files_info


def parse_output(output):
    entries = {}
    pattern = re.compile(
        r"^- (.*): file_size=(\d+) bytes, is_dir=(True|False)$")
    for line in output.strip().splitlines():
        if line.startswith("Success: "):
            continue
        match = pattern.match(line)
        if not match:
            raise AssertionError(f"Unexpected output line: {line}")
        name, size, is_dir = match.groups()
        entries[name] = {
            "size": int(size),
            "is_dir": is_dir == "True",
        }
    return entries


def test_lists_current_directory():
    output = get_files_info("calculator", ".")
    assert output.startswith('Success: "." is within the working directory')

    entries = parse_output(output)
    assert "main.py" in entries
    assert entries["main.py"]["is_dir"] is False


def test_blocks_absolute_bin_directory():
    output = get_files_info("calculator", "/bin")
    assert (
        output
        == 'Error: Cannot list "/bin" as it is outside the permitted working directory'
    )


def test_blocks_parent_directory():
    output = get_files_info("calculator", "../")
    assert (
        output
        == 'Error: Cannot list "../" as it is outside the permitted working directory'
    )


def test_path_is_file():
    output = get_files_info("calculator", "main.py")
    assert output == 'Error: The path "main.py" is not a directory'
