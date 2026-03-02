from google.adk.tools import BaseTool
import requests
import json
import re

class ToneTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="tone_analyzer",
            description="Analyzes the tone of a message using Ollama"
        )

    def run(self, user_input: str):
        prompt = f"""
        Analyze the tone of the following message.
        Return the tone in one of these categories: 
        happy, sad, angry, neutral, excited, frustrated, polite, formal, informal.
        
        Return ONLY valid JSON like this:
        {{"tone": ""}}

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
                    "format": "json"
                },
                timeout=120
            )
            
            response.raise_for_status()
            raw_result = response.json().get("response", "").strip()

            # Robust JSON extraction
            json_match = re.search(r'\{.*\}', raw_result, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            
            return json.loads(raw_result)
        except Exception as e:
            print(f"Error in ToneTool: {e}")
            return {"tone": "neutral"}