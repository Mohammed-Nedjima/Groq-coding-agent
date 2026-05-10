# coding-agent

## Usage

Run with a prompt:

```bash
uv run -- main.py "Explain quicksort"
```

Select a model with `--model` (`-m`):

```bash
uv run -- main.py "Hello" --model llama-3.1-8b-instant
```

The model name goes directly after the flag, like `--model llama-3.1-8b-instant`.
The curly braces you may see in `--help` output are just argparse's way of showing the allowed choices.

If you pass a model that is not in the allowed set, `argparse` returns an error.

## TAB Completion for Models

This app supports shell completion through `argcomplete`.

1. One-time activation for your current shell:

```bash
eval "$(register-python-argcomplete main.py)"
```

2. Or enable globally:

```bash
activate-global-python-argcomplete --user
```

After activation, type:

```bash
uv run -- main.py "test" --model <TAB>
```

and available model names will be suggested.

If tab completion still does not trigger:

- Verify `argcomplete` is installed in the same environment used by `uv run`.
- Use `uv run -- ...` so flags after `--` are parsed by your script, not by `uv`.
- Ensure your shell startup file loads argcomplete completion hooks.
