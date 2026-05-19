# AgentHub

A browser-based platform for creating, running, and managing custom AI agents. Define an agent with a system prompt, then chat with it — all in a clean web UI powered by a locally-running LLM.

## Project Structure

```
email-drafter-agent/
├── App/
│   └── Tools/
│       └── base_tool.py    # HTTP wrapper for Ollama LLM calls
├── database.py             # SQLite DatabaseManager (agents + history)
├── main.py                 # FastAPI server & WebSocket handler
├── index.html              # Single-file SPA (Tailwind CSS + marked.js)
├── agent_builder.db        # SQLite database (auto-created on first run)
└── requirements.txt
```

## Getting Started

**Prerequisites:** [Ollama](https://ollama.com) must be installed and running locally.

1. Clone the repo and create a virtual environment:

   ```bash
   git clone <repo-url> email-drafter-agent
   cd email-drafter-agent
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Pull and run the LLM model:

   ```bash
   ollama run llama3
   ```

   Ollama must be reachable at `http://localhost:11434/api/generate`.

4. Start the server:

   ```bash
   uvicorn main:app --reload
   ```

   Open `http://localhost:8000/` in your browser.

## Features

- Create custom agents with any system prompt
- Edit and delete existing agents
- Chat with any agent in real time over WebSocket
- Conversation history persisted per agent in SQLite
- Markdown rendering of AI responses
- Responsive sidebar listing all your agents

## How It Works

**Request flow:**
1. Browser connects over WebSocket (`/ws`)
2. Frontend sends JSON with a `type` field
3. `main.py` routes by type → calls `DatabaseManager` or `BaseTool`
4. Response JSON is sent back over the same socket

**WebSocket message types:**

| Type | Description |
|---|---|
| `create_agent` | Create a new agent (no `id`) or update an existing one (with `id`) |
| `run_agent` | Send a user message to an agent; gets AI response back |
| `get_agent_details` | Fetch an agent's name and system prompt by ID |
| `delete_agent` | Remove an agent and its full conversation history |

There is also a REST endpoint `GET /get_agents` that returns all agents (used by the sidebar on page load).

**LLM layer** (`App/Tools/base_tool.py`):  
`BaseTool` sends HTTP POST requests to a locally-running Ollama instance. Default model is `llama3`, temperature `0.4`, streaming disabled. To swap models, change the `model` arg in the `BaseTool()` constructor in `main.py`.

**Database** (`database.py`):  
`DatabaseManager` wraps a single SQLite connection. Two tables:
- `agents(id, name, system_prompt)`
- `history(id, agent_name, user_message, ai_response, timestamp)`

## Dependencies

| Package | Version | Purpose |
|---|---|---|
| `fastapi` | 0.133.1 | Web framework & REST API |
| `uvicorn` | 0.41.0 | ASGI server |
| `websockets` | 15.0.1 | WebSocket support |
| `requests` | 2.32.5 | HTTP calls to Ollama |
| `google-adk` | 1.25.1 | Agent Development Kit |

## Customization

- **Swap the LLM model:** Change `BaseTool(model="llama3")` in `main.py` to any model available in your Ollama installation (e.g. `mistral`, `gemma3`).
- **Adjust temperature / token limit:** Edit the `options` dict in `base_tool.py` or the `max_tokens` arg passed from `main.py`.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b ft/your-feature`)
3. Commit your changes
4. Open a pull request

## License

MIT License — see `LICENSE` for details.
