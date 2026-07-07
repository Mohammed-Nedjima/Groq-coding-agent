# Groq Coding Agent

A CLI coding agent powered by the [Groq API](https://groq.com). Give it a
task and it reads, writes, and runs files in a sandboxed working directory
until the job is done — using tool calls to inspect code, make changes, and
self-correct based on what it sees.

**Tools:** list files, read a file, write a file, run a Python script — all
restricted to a configured working directory.

## Setup

```sh
git clone https://github.com/Mohammed-Nedjima/Groq-coding-agent.git
cd Groq-coding-agent
uv sync                                          # or: pip install groq python-dotenv yaspin argcomplete
echo "GROQ_API_KEY=your-api-key-here" > .env     # get a key at console.groq.com/keys
```

## Usage

```sh
uv run main.py "list the files in the project"
uv run main.py "add error handling to the divide function" --verbose
```

`--verbose` shows token usage and each tool call as it happens.

By default the agent operates on the bundled `calculator/` sample project.
To point it at your own code, change `WORKING_DIRECTORY` in
`call_function.py`.

## Tests

```sh
uv run pytest
```

## Structure

```
main.py             # CLI entrypoint + agent loop
call_function.py     # Dispatches model tool calls to real functions
functions/            # get_file_content, get_files_info, write_file, run_python_file
calculator/           # Sample sandbox project
tests/                # Unit tests
```

## Stack

Groq API · `python-dotenv` · `yaspin` · `argparse`
