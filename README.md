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


and available model names will be suggested.

If tab completion still does not trigger:

- Verify `argcomplete` is installed in the same environment used by `uv run`.
- Use `uv run -- ...` so flags after `--` are parsed by your script, not by `uv`.
- Ensure your shell startup file loads argcomplete completion hooks.
