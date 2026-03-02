# Email Drafter Agent

A web‑powered AI assistant that drafts professional emails for you based on a natural language description of your situation. While a minimal CLI entry point exists, the primary interaction is through a browser‑based dashboard. The system uses a lightweight tool architecture with separate components for intent extraction, tone analysis, and final email generation.

The agents rely on a locally‑running Ollama `llama3` model (or another compatible LLM) via HTTP requests and the [Google ADK](https://pypi.org/project/google-adk) `BaseTool` as a helper class.

## 🛠️ Project Structure

```
email-drafter-agent/
├── agent/                  # AI logic
│   ├── __init__.py         # makes the folder a Python package
│   ├── main_agent.py       # coordinator logic
│   ├── intent_tool.py      # tool 1: extract situation/goal/emotion
│   ├── tone_tool.py        # tool 2: classify tone
│   └── email_tool.py       # tool 3: generate email JSON
├── memory/                 # storage logic
│   ├── __init__.py
│   ├── session_manager.py  # read/write logic for session store
│   └── session_store.json  # data file holding previous emails
├── main.py                 # FastAPI & WebSocket server
├── index.html              # user interface (frontend)
└── run.py                  # CLI testing (legacy/alternative interface)
```

## 🚀 Getting Started

1. **Clone the repo** and create a virtual environment:

   ```bash
   git clone <repo-url> email-drafter-agent
   cd email-drafter-agent
   python -m venv venv
   source venv/bin/activate
   ```

2. **Install the Python dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run an Ollama model** on your machine (example):

   ```bash
   ollama run llama3
   ```

   Ensure the model is reachable at `http://localhost:11434/api/generate`.

4. **Start the web server**:

   ```bash
   uvicorn main:app --reload
   ```

   Visit `http://localhost:8000/` in your browser to access the UI and generate emails interactively.

> (A CLI mode is still available via `python run.py` for quick testing, but the web interface is the preferred workflow.)

## ✅ Features

- Browser dashboard with textarea input and live results
- Intent extraction (situation, emotion, goal)
- Tone analysis (happy, sad, angry, etc.)
- JSON‑formatted email output with subject, body, and closing
- Session storage of past drafts
- Modular tools for easy customization

## ✍️ Example

### Web UI Workflow

1. Start the server (`uvicorn main:app --reload`) and open `http://localhost:8000/`.
2. Type your situation in the textarea and click **Generate Professional Email**.
3. The generated subject, body, and closing will appear instantly on the page; use the “Copy All” button to grab the full message.

> Emails are also saved automatically to `memory/session_store.json` for later review.

*(A CLI test mode is still possible with `python run.py`, but the browser dashboard is the main experience.)

## 📁 Session Memory

Generated emails are automatically appended to `memory/session_store.json` so you can review past drafts. Each entry includes the original user query, a timestamp, and the `subject`/`body`/`closing` of the generated message.

This project includes a `session_manager.py` which handles appending generated emails to the JSON store; you can modify it to change how persistence works.

Example stored record:

```json
{
    "timestamp": "2026-03-02 02:31:26",
    "user_query": "I met a potential client, Sarah, at the conference yesterday...",
    "generated_email": {
        "subject": "Following Up on Our Conference Discussion",
        "body": "Dear Sarah, I wanted to take a moment to express my gratitude...",
        "closing": "Best regards,"
    }
}
```

## 🧩 Customization

- Swap out the LLM endpoint or model in each tool by modifying the `requests.post` URL/parameters.
- Add new tones/goals/situations as needed in the prompt templates.

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes and add tests if applicable
4. Submit a pull request

## 📜 License

MIT License – see `LICENSE` for details.

> This project is a small demo and not intended for production use.
