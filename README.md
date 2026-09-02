# AI Agent in Python

This is my implementation of Boot.dev's [Build an AI Agent in Python](https://www.boot.dev/courses/build-ai-agent-python) project. The goal is a small coding agent that can inspect files, edit code, run Python, and use the results to decide what to do next.

The project is still in progress. The current CLI sends prompts to a free model through OpenRouter, with optional token usage output. Sandboxed helpers for listing, reading, and writing files are also included as the building blocks for agent tool calls.

## Usage

Install the dependencies with [uv](https://docs.astral.sh/uv/):

```sh
uv sync
```

Create a `.env` file and add an [OpenRouter](https://openrouter.ai/) API key:

```env
OPENROUTER_API_KEY=your_api_key
```

Run the agent with a prompt:

```sh
uv run main.py "Explain what this project does"
```

Add `--verbose` to also print token usage.
