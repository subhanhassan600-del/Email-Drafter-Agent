from .base_tool import BaseTool

class EmailTool(BaseTool):
    def run(self, user_input, situation, goal, tone):
        prompt = f"Generate email for: {situation}, Goal: {goal}, Tone: {tone}. Input: {user_input}. Return JSON: subject, body, closing."
        return self.call_model(prompt)