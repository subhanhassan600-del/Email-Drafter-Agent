from .base_tool import BaseTool

class EmailTool(BaseTool):
    def run(self, user_input, situation, goal, tone):
        # Restriction yahan add hogi
        prompt = (
            f"Generate a professional email based on the following:\n"
            f"Situation: {situation}\n"
            f"Goal: {goal}\n"
            f"Tone: {tone}\n"
            f"User Input: {user_input}\n\n"
            f"CRITICAL: Return ONLY a raw JSON object. Do not include introductory text, "
            f"markdown code blocks, or notes. "
            f"Format: {{\"subject\": \"...\", \"body\": \"...\", \"closing\": \"...\"}}"
        )
        return self.call_model(prompt)