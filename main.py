from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from App.Agents.email_agent import EmailDrafterAgent
from App.Agents.prompt_agent import PromptImproverAgent
from database import DatabaseManager
import json

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

                # 2. String vs Dictionary Check (Yahan error aa raha tha)
                if isinstance(result, dict):
                    # Agar dictionary hai toh safely keys nikalen
                    email_subject = result.get("subject", "Project Update")
                    email_body = result.get("body", str(result))
                    email_closing = result.get("closing", "Best regards")
                else:
                    # Agar result sirf ek string hai, toh pura result body mein dal den
                    email_subject = "Project Update"
                    email_body = str(result)
                    email_closing = "Best regards"

                # 3. Frontend ke liye response tayyar karein
                response = {
                    "agent": "email",
                    "subject": email_subject,
                    "body": email_body,
                    "closing": email_closing
                }

                # 4. Database mein save karein (Ab crash nahi hoga)
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