# Groq Coding Agent

A CLI-based coding agent powered by the [Groq API](https://groq.com). Give it a
natural-language task and it will autonomously read, write, and execute files
inside a sandboxed working directory until the task is done — inspecting your
code, making changes, running scripts, and self-correcting based on the
output it sees.

## How it works

The agent runs a **tool-calling loop**: it sends your prompt to the model
along with a set of tools, the model decides which tool(s) to call, the
agent executes them locally and feeds the results back, and this repeats
until the model produces a final answer instead of another tool call.

Available tools:

| Tool | What it does |
|---|---|
| `get_files_info` | Lists files and directories in a given path |
| `get_file_content` | Reads a file's contents (truncated at `MAX_READ_CHARACTERS`) |
| `write_file` | Creates or overwrites a file, including parent directories |
| `run_python_file` | Executes a Python script and captures stdout/stderr |

Every tool validates that the target path stays **inside the configured
working directory** — the agent cannot read, write, or execute anything
outside its sandbox, no matter what it's asked to do.

## Requirements

- Python 3.13+
- A [Groq API key](https://console.groq.com/keys) (free tier available)
- [uv](https://docs.astral.sh/uv/) (recommended) or `pip`

## Setup

**1. Clone the repo**

```sh
git clone https://github.com/Mohammed-Nedjima/Groq-coding-agent.git
cd Groq-coding-agent
```

**2. Install dependencies**

With `uv` (recommended — this project ships a `uv.lock`):

```sh
uv sync
```

Without `uv`:

```sh
pip install groq python-dotenv yaspin argcomplete
```

**3. Add your API key**

Create a `.env` file in the project root:

```sh
echo "GROQ_API_KEY=your-api-key-here" > .env
```

Replace `your-api-key-here` with a key from the
[Groq Console](https://console.groq.com/keys). The `.env` file is already
covered by `.gitignore`, so your key won't accidentally get committed.

## Usage

```sh
uv run main.py "list the files in the project"
uv run main.py "add error handling to the divide function" --verbose
```

(Or, without `uv`: `python main.py "..."`.)

`--verbose` prints token usage and each tool call/result as it happens —
useful for debugging what the agent is actually doing.

### The sandbox directory

The agent only operates inside one working directory at a time, set as
`WORKING_DIRECTORY` in `call_function.py`. It currently points at the
bundled `calculator/` sample project, which exists purely as a safe
target for the agent to read/modify/run. To point the agent at your own
project, change `WORKING_DIRECTORY` to that path.

## Project structure

```
├── main.py                       # CLI entrypoint and agent loop
├── call_function.py              # Dispatches model tool calls to real functions
├── config.py                     # Shared constants (e.g. MAX_READ_CHARACTERS)
├── prompts.py                    # System prompt
├── functions/
│   ├── get_file_content.py       # Read files (sandboxed)
│   ├── get_files_info.py         # List directory contents (sandboxed)
│   ├── write_file.py             # Write files (sandboxed)
│   └── run_python_file.py        # Execute Python scripts (sandboxed)
├── calculator/                   # Sample project used as the default sandbox
└── tests/                        # Unit tests for each tool
```

## Running tests

```sh
uv run pytest
```

## Model

The agent uses `openai/gpt-oss-120b` on Groq. If you want to try a
different model, change the `MODEL` constant in `main.py` — any
tool-use-capable model on Groq will work, though reliability varies by
model, and `main.py` includes retry logic for transient malformed
tool-call generations.

## Stack

- [Groq API](https://groq.com) — ultra-fast LLM inference
- `argparse` / `argcomplete` — CLI interface
- `yaspin` — terminal spinner while waiting on model responses
- `python-dotenv` — loads `GROQ_API_KEY` from `.env`
