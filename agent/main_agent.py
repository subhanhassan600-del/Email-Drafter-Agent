from agent.intent_tool import IntentTool
from agent.tone_tool import ToneTool
from agent.email_tool import EmailTool

class EmailDrafterAgent:
    def __init__(self):
        self.intent_tool = IntentTool()
        self.tone_tool = ToneTool()
        self.email_tool = EmailTool()

    def run(self, user_input: str):
        # 1️⃣ Get intent
        intent = self.intent_tool.run(user_input)

        # 2️⃣ Get tone from full user input
        tone_result = self.tone_tool.run(user_input)

        # 3️⃣ Generate email
        email = self.email_tool.run(
            user_input=user_input,  # pass full message!
            tone=tone_result.get("tone", "neutral"),
            goal=intent.get("goal", "clarification"),
            situation=intent.get("situation", "unknown")
        )

        return email