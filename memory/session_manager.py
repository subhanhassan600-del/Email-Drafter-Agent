import json
import os
from datetime import datetime

def save_to_session(user_input, agent_result, agent_type="email"):
    """
    Saves the interaction to a JSON file. 
    Handles both Email and Prompt Improver results.
    """
    file_path = "memory/session_store.json"
    
    # 1. Folder check/create
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # 2. Load existing data
    sessions = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try:
                sessions = json.load(f)
            except json.JSONDecodeError:
                sessions = []

    # 3. Create a flexible record
    # Humne keys ko generic rakha hai taake har agent fit ho jaye
    new_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "agent_type": agent_type,
        "user_query": user_input,
        "result": agent_result  # Yeh poora dictionary save karega (Email ho ya Prompt)
    }
    
    sessions.append(new_entry)

    # 4. Save back to file
    with open(file_path, 'w') as f:
        json.dump(sessions, f, indent=4)