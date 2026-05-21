from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from app.tools.base_tool import BaseTool
from database import DatabaseManager
import json

# Load .env if present (ignore if python-dotenv not installed)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

app = FastAPI()

db = DatabaseManager()
base_tool = BaseTool()

@app.get("/")
async def get():
    return FileResponse("index.html")

@app.get("/get_agents")
async def get_agents():
    return {"agents": db.fetch_all_agents()}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            raw_payload = await websocket.receive_text()
            data = json.loads(raw_payload)
            request_type = data.get("type")

            # ── 1. CREATE / UPDATE AGENT ──────────────────────────────────
            if request_type == "create_agent":
                agent_id   = data.get("id")
                agent_name = data.get("name")
                system_instructions = data.get("prompt")

                if agent_id:
                    db.update_agent(agent_id, agent_name, system_instructions)
                    response = {"type": "agent_updated", "id": agent_id, "name": agent_name}
                else:
                    new_id = db.save_agent(agent_name, system_instructions)
                    response = {"type": "agent_created", "id": new_id, "name": agent_name}

            # ── 2. RUN AGENT ──────────────────────────────────────────────
            elif request_type == "run_agent":
                agent_id     = data.get("agent_id")
                user_message = data.get("text")

                instructions = db.get_agent_prompt(agent_id)

                if instructions:
                    full_prompt = f"SYSTEM: {instructions}\n\nUSER INPUT: {user_message}"
                    result      = base_tool.call_model(full_prompt)
                    if result is None:
                        response = {"type": "error", "message": "AI model unavailable. Check your provider config."}
                    else:
                        db.add_history(agent_id, user_message, result["text"])
                        response = {
                            "type":     "ai_output",
                            "response": result["text"],
                            "tokens":   result["tokens"],
                        }
                else:
                    response = {"type": "error", "message": "Agent not found"}

            # ── 3. GET AGENT DETAILS ──────────────────────────────────────
            elif request_type == "get_agent_details":
                agent_id   = data.get("agent_id")
                agent_data = db.get_agent_details(agent_id)
                if agent_data:
                    response = {
                        "type": "agent_details",
                        "id":     agent_data["id"],
                        "name":   agent_data["name"],
                        "prompt": agent_data["prompt"],
                    }
                else:
                    response = {"type": "error", "message": "Agent not found"}

            # ── 4. GET HISTORY ────────────────────────────────────────────
            elif request_type == "get_history":
                agent_id = data.get("agent_id")
                messages = db.get_history(agent_id)
                response = {"type": "history_data", "messages": messages}

            # ── 5. DELETE AGENT ───────────────────────────────────────────
            elif request_type == "delete_agent":
                agent_id = data.get("agent_id")
                db.delete_agent(agent_id)
                response = {"type": "agent_deleted", "id": agent_id}

            # ── 6. INVALID ────────────────────────────────────────────────
            else:
                response = {"type": "error", "message": "Invalid request type"}

            await websocket.send_text(json.dumps(response))

    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"Server Error: {e}")
        await websocket.send_text(json.dumps({"type": "error", "message": str(e)}))
