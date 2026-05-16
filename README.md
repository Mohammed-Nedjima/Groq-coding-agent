# Groq Coding Agent

A CLI-based coding agent powered by the Groq API and LLaMA 3.3 70B.
Given a prompt, the agent autonomously reads, writes, and executes files
in a sandboxed working directory to complete coding tasks.

## How it works

The agent uses LLM tool-calling to interact with the filesystem. It can:

- **Read files** — inspect source code and project structure
- **Write files** — create or overwrite files with generated content
- **Run Python scripts** — execute code and observe the output
- **List directories** — explore the working directory tree

Each tool enforces a sandboxed working directory — the agent cannot
read or write outside its permitted scope.

## Usage

```sh
python main.py "fix the bug in main.py"
python main.py "add error handling to all functions" --verbose
```

`--verbose` disables streaming and shows token usage instead.

## Setup

```sh
pip install -r requirements.txt
cp .env.example .env  # add your GROQ_API_KEY
```

## Project structure
├── main.py                  # CLI entrypoint and agent loop
├── prompts.py               # System prompt
├── functions/
│   ├── get_file_content.py  # Read files (sandboxed)
│   ├── get_files_info.py    # List directory contents
│   ├── write_file.py        # Write files (sandboxed)
│   └── run_python_file.py   # Execute Python scripts
└── tests/                   # Unit tests for each tool

## Stack

- [Groq API](https://groq.com) — ultra-fast LLM inference
- `argparse` — CLI interface
- `yaspin` — terminal spinner for streaming responses
