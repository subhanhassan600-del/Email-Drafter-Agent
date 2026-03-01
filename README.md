# Email Drafter Agent

A simple command‑line agent that drafts professional emails for you based on a natural language description of your situation. It uses a lightweight tool architecture, with separate components for intent extraction, tone analysis, and final email generation.

The agents rely on a locally‑running Ollama `llama3` model (or another compatible LLM) via HTTP requests and the [Google ADK](https://pypi.org/project/google-adk) `BaseTool` as a helper class.

## 🛠️ Project Structure

```
requirements.txt
run.py                # entry point
agent/
    main_agent.py     # orchestrates the tools
    intent_tool.py    # detects situation/goal/emotion
    tone_tool.py      # classifies tone
    email_tool.py     # produces the email JSON
memory/               # session data (optional)
# session_manager.py    # helper for persisting conversations (may not be present)
session_store.json    # storage file where generated emails are saved
```

## 🚀 Getting Started

1. **Clone the repo** and create a virtual environment:

   ```bash
   git clone <repo-url> email-drafter-agent
   cd email-drafter-agent
   python -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run an Ollama model** on your machine (example):

   ```bash
   ollama run llama3
   ```

   Ensure the model is reachable at `http://localhost:11434/api/generate`.

4. **Start the agent**:

   ```bash
   python run.py
   ```

   Enter a description of the situation when prompted and see the generated email.

## ✅ Features

- Intent extraction (situation, emotion, goal)
- Tone analysis (happy, sad, angry, etc.)
- JSON‑formatted email output with subject, body, and closing
- Modular tools for easy customization

## ✍️ Example

```
Describe the situation:
> I need to ask my manager for a day off next week because of a dentist appointment.

--- GENERATED EMAIL ---

Subject: Request for Personal Day

Hello [Manager Name],

I hope you're doing well. I'm writing to request a personal day on [date] next week due to a dentist appointment I have scheduled. I'll ensure all of my tasks are covered and will be available by phone if anything urgent comes up.

Thank you for your understanding.

Best regards,
[Your Name]
```

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
