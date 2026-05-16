from functions.run_python_file import run_python_file


def test_runs_main_usage():
    output = run_python_file("calculator", "main.py")
    print(output)
    assert output.startswith('Python script "main.py" executed successfully')
    assert "Calculator App" in output
    assert 'Usage: python main.py "<expression>"' in output


def test_runs_main_expression():
    output = run_python_file("calculator", "main.py", ["3 + 5"])
    print(output)
    assert output.startswith('Python script "main.py" executed successfully')
    assert '"expression": "3 + 5"' in output
    assert '"result": 8' in output


def test_runs_calculator_tests():
    output = run_python_file("calculator", "tests.py")
    print(output)
    assert output.startswith('Python script "tests.py" executed successfully')
    assert "OK" in output


def test_blocks_parent_directory():
    output = run_python_file("calculator", "../main.py")
    print(output)
    assert (
        output
        == 'Error: Cannot execute "../main.py" as it is outside the permitted working directory'
    )


def test_missing_file():
    output = run_python_file("calculator", "nonexistent.py")
    print(output)
    assert (
        output
        == 'Error: File not found or is not a regular file: "nonexistent.py"'
    )


def test_rejects_non_python_file():
    output = run_python_file("calculator", "lorem.txt")
    print(output)
    assert output == 'Error: "lorem.txt" is not a Python file'
