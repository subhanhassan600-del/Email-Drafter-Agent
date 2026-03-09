from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from App.Agents.email_agent import EmailDrafterAgent
from App.Agents.prompt_agent import PromptImproverAgent
from memory.session_manager import save_to_session
import json

app = FastAPI()

# Initialize Agents
email_agent = EmailDrafterAgent()
prompt_agent = PromptImproverAgent()


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

                result = email_agent.run(user_text)

                response = {
                    "agent": "email",
                    "subject": result.get("subject", "No Subject"),
                    "body": result.get("body", "No Body Generated"),
                    "closing": result.get("closing", "Best regards")
                }

                save_to_session(user_text, response, agent_type="email")

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

                save_to_session(user_text, improved_prompt, agent_type="prompt")

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