# import requests
# import json

# class BaseTool:
#     def __init__(self, model="llama3"):
#         self.model = model
#         self.url = "http://localhost:11434/api/generate"
#         self.timeout = 120  # 2 minutes timeout for slow systems

#     def call_model(self, prompt, is_json=True):
#         """Common method to talk to Ollama"""
#         payload = {
#             "model": self.model,
#             "prompt": prompt,
#             "stream": False
#         }
#         if is_json:
#             payload["format"] = "json"

#         try:
#             response = requests.post(self.url, json=payload, timeout=self.timeout)
#             response.raise_for_status()
#             print(f"Raw response from model: {response.text}")
#             result = response.json().get("response", "{}")
#             return json.loads(result) if is_json else result
#         except Exception as e:
#             print(f"Error in {self.__class__.__name__}: {e}")
#             return None



import requests
import json

class BaseTool:
    def __init__(self, model="llama3"):
        self.model = model
        self.url = "http://localhost:11434/api/generate"
        self.timeout = 200

    def call_model(self, prompt):
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
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