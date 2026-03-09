from .base_tool import BaseTool
import json

class PromptRefinerTool(BaseTool):
    def refine(self, raw_prompt, intent, tone):
        # --- NEW EXTRACTION LOGIC ---
        # Agar intent aur tone JSON/Dict hain, toh sirf unka text nikaalein
        # Taake AI ko curly braces nazar na aayein
        
        situation_text = intent.get('situation', 'Expert') if isinstance(intent, dict) else intent
        goal_text = intent.get('goal', raw_prompt) if isinstance(intent, dict) else raw_prompt
        tone_text = tone.get('tone', 'neutral') if isinstance(tone, dict) else tone

        # --- UPDATED PROMPT ---
        prompt = f"""
        SYSTEM: YOU ARE A MASTER PROMPT ENGINEER. 

        CRITICAL INSTRUCTIONS:
        1. NO JSON: Do NOT use curly braces {{}} or keys like "improved_prompt".
        2. CLEAN TEXT: Return ONLY the final improved prompt as a readable document.
        3. FORMAT: Use the headers [ROLE], [CONTEXT], [TASK], and [CONSTRAINTS].

        INFORMATION FOR YOU:
        - TOPIC: {situation_text}
        - USER GOAL: {goal_text}
        - REQUIRED TONE: {tone_text}

        USER'S RAW INPUT: "{raw_prompt}"
        
        TASK: Rewrite the RAW INPUT into a professional, highly detailed prompt.

        CLEAN TEXT OUTPUT:
        """
        
        result = self.call_model(prompt)
        return result