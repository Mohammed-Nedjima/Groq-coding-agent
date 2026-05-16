from config import MAX_READ_CHARACTERS
from functions.get_file_content import get_file_content


def test_truncates_long_file():
    output = get_file_content("calculator", "lorem.txt")
    truncation_message = (
        f'[...File "lorem.txt" truncated at {MAX_READ_CHARACTERS} characters]'
    )
    assert output.endswith(truncation_message)
    assert len(output) == MAX_READ_CHARACTERS + len(truncation_message)


def test_blocks_absolute_bin_directory():
    output = get_file_content("calculator", "/bin")
    assert (
        output
        == 'Error: Cannot read "/bin" as it is outside the permitted working directory'
    )


def test_blocks_parent_directory():
    output = get_file_content("calculator", "../")
    assert (
        output
        == 'Error: Cannot read "../" as it is outside the permitted working directory'
    )


def test_path_is_not_file():
    output = get_file_content("calculator", ".")
    assert output == 'Error: File not found or is not a regular file: "."'


def test_reads_main_py():
    output = get_file_content("calculator", "main.py")
    print(output)
    assert output


def test_reads_pkg_calculator():
    output = get_file_content("calculator", "pkg/calculator.py")
    print(output)
    assert output


def test_blocks_bin_cat():
    output = get_file_content("calculator", "/bin/cat")
    print(output)
    assert (
        output
        == 'Error: Cannot read "/bin/cat" as it is outside the permitted working directory'
    )


def test_missing_pkg_file():
    output = get_file_content("calculator", "pkg/does_not_exist.py")
    print(output)
    assert (
        output
        == 'Error: File not found or is not a regular file: "pkg/does_not_exist.py"'
    )
