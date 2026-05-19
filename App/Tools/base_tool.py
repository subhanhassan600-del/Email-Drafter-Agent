import requests
import json

class BaseTool:
    def __init__(self, model="llama3"):
        self.model = model
        self.url = "http://localhost:11434/api/generate"
        self.timeout = 200

    def call_model(self, prompt, max_tokens=300):
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": max_tokens,
                "temperature": 0.4
            }
        }

        try:
            response = requests.post(self.url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            
            res_json = response.json()
            result = res_json.get("response", "{}")
            
            return result
        except Exception as e:
            print(f"Error in {self.__class__.__name__}: {e}")
            return None