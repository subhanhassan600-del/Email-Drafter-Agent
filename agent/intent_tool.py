from google.adk.tools import BaseTool
import requests
import json
import re

class IntentTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="intent_extractor",
            description="Extracts situation, emotion, and goal using Ollama"
        )

    def run(self, user_input: str):
        prompt = f"""
        Extract the following from the message:
        - situation (short category)
        - emotion (one word)
        - goal (what user wants)

        Return ONLY valid JSON.
        Message:
        {user_input}
        """

        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama3",
                    "prompt": prompt,
                    "stream": False,
                    "format": "json"   # Ollama ab sirf JSON dega
                },
                timeout=120
            )
            
            response.raise_for_status()
            raw_result = response.json().get("response", "").strip()
            
            # Debugging: check karne ke liye ke Ollama ne kya bheja
            # print(f"Ollama Raw Response: {raw_result}")

            # Regex for safety
            json_match = re.search(r'\{.*\}', raw_result, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            
            return json.loads(raw_result)
            
        except Exception as e:
            print(f"Error in IntentTool: {e}")
            return {
                "situation": "unknown",
                "emotion": "neutral",
                "goal": "clarification"
            }