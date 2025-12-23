# planet-terp-agent

an ai assistant for university of maryland students powered by planetterp.

this tool is especially useful when you're choosing classes and feeling confused about which professors to take or want to compare class grade data. it can analyze professor reviews, look up course details, and check historical grade distributions to help you make informed decisions.

## setup

1. install dependencies:
   ```bash
   uv sync
   ```
2. set your environment variables in `.env`:
   ```bash
   OPENAI_API_KEY=your_key_here
   ```

## usage

run the interactive chat assistant:
```bash
uv run src/chat.py`
```

this will open a persistent chat session where you can ask multiple questions. context is maintained throughout the session.

## project structure

- `src/agent.py`: agent configuration and initialization.
- `src/tools.py`: planetterp api tools including grades, search, and reviews.
- `src/chat.py`: cli entry point with prompt and debug support.
- `initpy.sh`: helper script to initialize new python projects.
