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