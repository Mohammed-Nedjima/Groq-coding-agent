from functions.write_file import write_file


def test_writes_lorem_txt():
    output = write_file("calculator", "lorem.txt",
                        "wait, this isn't lorem ipsum")
    print(output)
    assert output == 'File "lorem.txt" has been written successfully.'


def test_writes_pkg_file():
    output = write_file("calculator", "pkg/morelorem.txt",
                        "lorem ipsum dolor sit amet")
    print(output)
    assert output == 'File "pkg/morelorem.txt" has been written successfully.'


def test_blocks_tmp_path():
    output = write_file("calculator", "/tmp/temp.txt",
                        "this should not be allowed")
    print(output)
    assert (
        output
        == 'Error: Cannot write to "/tmp/temp.txt" as it is outside the permitted working directory'
    )
