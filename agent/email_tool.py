from google.adk.tools import BaseTool
import requests
import json
import re

class EmailTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="email_generator",
            description="Generates a complete email based on user input, intent, and tone"
        )

    def run(self, user_input: str, situation: str, goal: str, tone: str):
        prompt = f"""
        You are an AI email assistant. 
        Generate a professional and context-aware email based on the following:

        Situation: {situation}
        Goal: {goal}
        Tone: {tone}
        User Message: {user_input}

        STRICT INSTRUCTIONS:
        1. Return ONLY valid JSON.
        2. Use exactly these keys: "subject", "body", "closing".
        3. Do not include any conversational text, headers, or footers.

        Example Output Format:
        {{
            "subject": "Enter subject here",
            "body": "Enter email body here",
            "closing": "Enter formal closing here"
        }}
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
                timeout=40 # Email generation thoda waqt le sakti hai
            )

            response.raise_for_status()
            raw_result = response.json().get("response", "").strip()

            # Robust JSON extraction
            json_match = re.search(r'\{.*\}', raw_result, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            
            return json.loads(raw_result)

        except Exception as e:
            print(f"Error in EmailTool: {e}")
            return {
                "subject": "Email regarding your request",
                "body": f"Regarding your message: {user_input}",
                "closing": "Best regards"
            }