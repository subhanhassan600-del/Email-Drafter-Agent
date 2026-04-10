from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from App.Agents.email_agent import EmailDrafterAgent
from App.Agents.prompt_agent import PromptImproverAgent
from database import DatabaseManager
import json
import re

app = FastAPI()

# Initialize Agents
email_agent = EmailDrafterAgent()
prompt_agent = PromptImproverAgent()
db = DatabaseManager()


@app.get("/")
async def get():
    return FileResponse("index.html")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()

    try:
        while True:

            # Receive message from frontend
            raw_payload = await websocket.receive_text()
            data = json.loads(raw_payload)

            user_text = data.get("text")
            selected_agent = data.get("agent")
            
            # ---------------- EMAIL AGENT ----------------
            if selected_agent == "email":
                # 1. AI se result lein
                result = email_agent.run(user_text)

                # 2. Cleanup & Parsing Logic
                email_subject = "Project Update"
                email_body = str(result)
                email_closing = "Best regards"

                if isinstance(result, dict):
                    # Agar pehle hi dictionary hai toh asani se nikalen
                    email_subject = result.get("subject", email_subject)
                    email_body = result.get("body", str(result))
                    email_closing = result.get("closing", email_closing)
                
                elif isinstance(result, str):
                    # AGAR STRING HAI: Toh Regex se JSON dhoondein
                    try:
                        # { } ke darmiyan wala saara data nikalna
                        match = re.search(r'\{.*\}', result, re.DOTALL)
                        if match:
                            clean_json = json.loads(match.group())
                            email_subject = clean_json.get("subject", email_subject)
                            email_body = clean_json.get("body", clean_json.get("message", result))
                            email_closing = clean_json.get("closing", email_closing)
                        else:
                            # Agar koi bracket nahi mila, toh pura text hi body hai
                            email_body = result
                    except Exception as e:
                        print(f"Regex Parsing Error: {e}")
                        email_body = result

                # 3. Frontend ke liye response tayyar karein
                response = {
                    "agent": "email",
                    "subject": email_subject,
                    "body": email_body,
                    "closing": email_closing
                }

                # 4. Database mein save karein
                db.add_record(
                    prompt=user_text, 
                    intent="Email Drafting", 
                    tone="Professional", 
                    improved=email_body
                )

            # ---------------- PROMPT IMPROVER ----------------
            elif selected_agent == "prompt":

                result = prompt_agent.run(user_text)

                # Convert result safely to string
                if isinstance(result, dict):
                    improved_prompt = result
                else:
                    improved_prompt = str(result)

                response = {
                    "agent": "prompt",
                    "improved_prompt": improved_prompt
                }

                # Agar improved_prompt dictionary hai toh sirf 'prompt' key nikaalein
                if isinstance(improved_prompt, dict):
                    clean_prompt = improved_prompt.get('prompt', str(improved_prompt))
                else:
                    clean_prompt = str(improved_prompt)

                db.add_record(
                    prompt=user_text, 
                    intent="Prompt Improvement", 
                    tone="Optimized", 
                    improved=clean_prompt
                )

            # ---------------- INVALID AGENT ----------------
            else:
                response = {
                    "error": "Invalid Agent Type"
                }

            # Send response to frontend
            await websocket.send_text(json.dumps(response))

    except WebSocketDisconnect:
        print("Client disconnected")

    except Exception as e:
        print(f"Server Error: {e}")

        await websocket.send_text(
            json.dumps({
                "error": str(e)
            })
        )