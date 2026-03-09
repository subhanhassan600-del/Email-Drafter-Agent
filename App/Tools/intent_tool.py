# from .base_tool import BaseTool

# class IntentTool(BaseTool):
#     def __init__(self):
#         # Ab humein yahan kisi extra setup ki zaroorat nahi
#         # Kyunki BaseTool model aur url ko handle kar raha hai
#         super().__init__()

#     def run(self, user_input: str):
#         prompt = f"""
#         SYSTEM: YOU ARE A SEMANTIC ANALYZER.
        
#         INSTRUCTIONS:
#         1. ANALYZE THE INTENT: Even if the grammar is broken (e.g., "Give a me", "I want a write"), identify the core meaning.
#         2. CATEGORIZE: 
#         - Situation: One word (e.g., Fitness, Coding, Work, Personal).
#         - Emotion: One word (Default to 'Neutral' if unclear).
#         - Goal: Short phrase of what the user needs.
#         3. NO NULLS: If you cannot find a value, use "General" for situation and "Neutral" for emotion. NEVER return 'None'.

#         Return ONLY a JSON object with these exact keys:
#         "situation", "emotion", "goal"

#         Message:
#         "{user_input}"
#     """
#         # Hum BaseTool ka call_model use kar rahe hain jo khud JSON parse karega
#         result = self.call_model(prompt)
        
#         # Backup agar model fail ho jaye
#         if result is None:
#             return {
#                 "situation": "unknown",
#                 "emotion": "neutral",
#                 "goal": "communication"
#             }
#         return result
    

from .base_tool import BaseTool
import json

class IntentTool(BaseTool):
    def run(self, user_input: str):
        prompt = f"""
        SYSTEM: YOU ARE A SEMANTIC ANALYZER.
        INSTRUCTIONS:
        1. IGNORE GRAMMAR: Focus on core meaning (e.g., "workout", "email", "code").
        2. NO NULLS: Use "General" and "Neutral" as defaults.
        3. FORMAT: Return ONLY JSON with keys: "situation", "emotion", "goal"
        
        Message: "{user_input}"
        """
        
        result = self.call_model(prompt)
        
        # Fallback Data
        default_data = {
            "situation": "General",
            "emotion": "Neutral",
            "goal": user_input[:50]
        }

        if not result:
            return default_data
            
        # Agar result dictionary nahi hai, toh dictionary banayein
        if not isinstance(result, dict):
            return default_data
            
        return result