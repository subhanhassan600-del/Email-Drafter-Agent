# Multi-Agent Intelligence System
This project is a Multi-Agent Intelligence System featuring two main agents: an Email Drafter that generates professional emails based on user input, and a Prompt Improver that refines and enhances user prompts for better AI interactions. It is a UI-based application built with FastAPI for the backend, WebSocket for real-time communication, and powered by Google ADK and requests for seamless integration with local LLMs like Ollama.

The agents rely on a locally‑running Ollama `llama3` model (or another compatible LLM) via HTTP requests and the [Google ADK](https://pypi.org/project/google-adk) `BaseTool` as a helper class.

## 🛠️ Project Structure

```
email-drafter-agent/
├── App/
│   ├── Agents/
│   │   ├── email_agent.py      # email drafting agent
│   │   └── prompt_agent.py     # prompt refinement agent
│   └── Tools/
│       ├── base_tool.py        # base tool class
│       ├── email_tool.py       # email generation tool
│       ├── intent_tool.py      # intent extraction tool
│       ├── main_agent.py       # main agent coordinator
│       ├── refiner_tool.py     # prompt refinement tool
│       └── tone_tool.py        # tone analysis tool
├── memory/                     # storage logic
│   ├── __init__.py
│   ├── session_manager.py      # read/write logic for session store
│   └── session_store.json      # data file holding previous emails
├── main.py                     # FastAPI & WebSocket server
├── index.html                  # user interface (frontend)
└── run.py                      # CLI testing (legacy/alternative interface)
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
- Prompt refinement for optimized AI queries
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
f

### Email Drafter Example

The Email Drafter agent generates professional emails based on user input, analyzing intent and tone.

**Input:** "I need to request a day off tomorrow because I'm not feeling well."

**Generated Email Output:**
```json
{
  "subject": "Request for Sick Leave Tomorrow",
  "body": "Dear [Manager's Name],\n\nI am writing to inform you that I am not feeling well and would like to request a day off tomorrow. I apologize for any inconvenience this may cause and will ensure that my responsibilities are covered.\n\nThank you for your understanding.\n\nBest regards,\n[Your Name]",
  "closing": "Best regards,"
}
```

### Prompt Improver Example

The Prompt Improver agent refines raw user prompts into structured, professional prompts for better AI interactions.

**Input:** "write email to boss for leave"

**Refined Output:**
```
[ROLE]
You are a professional email writer.

[CONTEXT]
The user needs to request leave from their boss.

[TASK]
Compose a formal email requesting time off, including reason and dates.

[CONSTRAINTS]
Keep the tone polite and professional; include subject, body, and closing.
```

This refined prompt can then be used to generate higher-quality emails.

## 📁 Session Memory

Generated emails and refined prompts are automatically appended to `memory/session_store.json` so you can review past drafts and improvements. Each entry includes the original user query, a timestamp, the agent type, and the result (email or prompt).

This project includes a `session_manager.py` which handles appending generated content to the JSON store; you can modify it to change how persistence works.

Example stored records:

**Email Drafter Record:**
```json
{
    "timestamp": "2026-03-02 02:31:26",
    "agent_type": "email",
    "user_query": "I met a potential client, Sarah, at the conference yesterday...",
    "result": {
        "subject": "Following Up on Our Conference Discussion",
        "body": "Dear Sarah, I wanted to take a moment to express my gratitude...",
        "closing": "Best regards,"
    }
}
```

**Prompt Improver Record:**
```json
{
    "timestamp": "2026-03-02 02:32:15",
    "agent_type": "prompt",
    "user_query": "write email to boss for leave",
    "result": "[ROLE]\nYou are a professional email writer.\n\n[CONTEXT]\nThe user needs to request leave from their boss.\n\n[TASK]\nCompose a formal email requesting time off, including reason and dates.\n\n[CONSTRAINTS]\nKeep the tone polite and professional; include subject, body, and closing."
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
