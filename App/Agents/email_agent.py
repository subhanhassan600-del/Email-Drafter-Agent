from App.Tools.intent_tool import IntentTool
from App.Tools.tone_tool import ToneTool
from App.Tools.email_tool import EmailTool

class EmailDrafterAgent:
    def __init__(self):
        self.intent_tool = IntentTool()
        self.tone_tool = ToneTool()
        self.email_tool = EmailTool()

    def run(self, user_input: str):
        # 1. Understand what user wants
        intent = self.intent_tool.run(user_input)
        # 2. Understand how user feels
        tone_res = self.tone_tool.run(user_input)
        
        # 3. Generate the final email
        result = self.email_tool.run(
            user_input=user_input,
            situation=intent.get("situation", "general"),
            goal=intent.get("goal", "communication"),
            tone=tone_res.get("tone", "professional")
        )
        return result