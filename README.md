# PlanetTerp Agent

AI assistant for UMD students using PlanetTerp and Reddit.

## Setup

1. Install dependencies:
   ```bash
   uv sync
   ```
2. Configure `.env`:
   ```env
   OPENAI_API_KEY=your_key
   ```

## Usage

Start the chat:
```bash
uv run src/chat.py
```

### Commands
- `save`: Exports session to `conversations/`.
- `exit`: Ends session.
- `--debug`: Flag to show tool calls.

## Features

- Grade aggregation.
- Reddit sentiment synthesis.
- Professor disambiguation via course context.
- Conversation exports.

## Examples 

Check out some examples of how to use this tool in [conversations](./conversations/).