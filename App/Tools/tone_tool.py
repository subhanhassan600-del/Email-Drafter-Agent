from .base_tool import BaseTool
import json

class ToneTool(BaseTool):
    def run(self, user_input: str):
        prompt = f"""
        SYSTEM: YOU ARE A LINGUISTIC TONE ANALYZER.
        INSTRUCTIONS:
        1. ANALYZE TONE: Identify the tone even if the grammar is broken (e.g., "Give a me").
        2. CHOOSE ONE: happy, sad, angry, neutral, excited, frustrated, polite, formal, informal.
        3. DEFAULT: If unclear, return "neutral".
        4. FORMAT: Return ONLY a JSON object: {{"tone": "chosen_tone"}}
        
        Message: "{user_input}"
        """
        
        # call_model se response lein
        result = self.call_model(prompt)
        
        # AGAR result string hai (JSON parse nahi hua), toh manually fix karein
        if isinstance(result, str):
            try:
                return json.loads(result)
            except:
                return {"tone": "neutral"}
                
        # AGAR result None hai
        if not result:
            return {"tone": "neutral"}
            
        return result