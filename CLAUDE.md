# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the App

```bash
# Start Ollama with the required model first
ollama run llama3

# Install dependencies (if needed)
pip install -r requirements.txt

# Start the FastAPI server
uvicorn main:app --reload
```

The UI is served at `http://localhost:8000/`. There are no automated tests.

## Architecture

This is **AgentHub** — a browser-based platform for creating, running, and managing custom AI agents. Users define agents via a system prompt, then chat with them. All data persists in a local SQLite file (`agent_builder.db`).

**Request flow:**
1. Browser connects over WebSocket (`/ws`)
2. Frontend sends JSON messages with a `type` field
3. `main.py` routes by `type` → calls `DatabaseManager` or `BaseTool`
4. Response JSON is sent back over the same socket

**WebSocket message types** (handled in [main.py](main.py)):
- `create_agent` — creates or updates an agent (presence of `id` field distinguishes update from create)
- `run_agent` — fetches the agent's system prompt from DB, calls the LLM, saves to history
- `get_agent_details` — fetches agent by ID
- `delete_agent` — removes agent and its history

There is also a REST endpoint `GET /get_agents` that returns all agent names (used by the sidebar on page load).

**LLM layer** ([App/Tools/base_tool.py](App/Tools/base_tool.py)):  
`BaseTool` makes HTTP POST requests to a locally-running Ollama instance at `http://localhost:11434/api/generate`. Default model is `llama3`, temperature `0.4`, streaming disabled. To swap models, change the `model` arg in the `BaseTool()` constructor in `main.py`.

**Database** ([database.py](database.py)):  
`DatabaseManager` wraps a single SQLite connection (thread-safe via `check_same_thread=False`). Two tables:
- `agents(id, name UNIQUE, system_prompt)`
- `history(id, agent_name, user_message, ai_response, timestamp)`

Note: `delete_agent` currently takes `name` as the SQL predicate but `main.py` passes `agent_id` — verify this is consistent if touching delete logic.

**Frontend** ([index.html](index.html)):  
Single-file SPA using Tailwind CSS (CDN) and `marked.js` for Markdown rendering. The WebSocket client is inline JS; agent responses are rendered as Markdown in `#resBody`.

## Branch Context

The `ft/agent-builder` branch is a refactor of the original email-drafter project into the generic AgentHub. Several files from the old architecture (`App/Agents/`, `App/Tools/email_tool.py`, etc.) are deleted on this branch. The README still describes the old structure — update it when merging.
