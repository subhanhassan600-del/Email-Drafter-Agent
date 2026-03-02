from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from agent.main_agent import EmailDrafterAgent
from memory.session_manager import save_to_session
import json

app = FastAPI()
agent = EmailDrafterAgent()

# Frontend ko serve karne ke liye
@app.get("/")
async def get():
    return FileResponse("index.html")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # 1. Receive User Input
            user_input = await websocket.receive_text()
            
            # 2. Process through AI Agent
            # (Ensure agent.run returns the final dict)
            result = agent.run(user_input)
            
            # 3. Save to Local Memory (JSON)
            save_to_session(user_input, result)
            
            # 4. Send back to UI
            await websocket.send_text(json.dumps(result))
            
    except WebSocketDisconnect:
        print("Client disconnected")