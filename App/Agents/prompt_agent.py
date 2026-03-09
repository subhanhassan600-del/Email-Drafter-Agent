from App.Tools.refiner_tool import PromptRefinerTool
from App.Tools.intent_tool import IntentTool
from App.Tools.tone_tool import ToneTool

class PromptImproverAgent:
    def __init__(self):
        self.intent_tool = IntentTool()
        self.tone_tool = ToneTool()
        self.refiner = PromptRefinerTool()

    def run(self, user_input):
        intent = self.intent_tool.run(user_input)
        tone = self.tone_tool.run(user_input)
        
        return self.refiner.refine(
            raw_prompt=user_input, 
            intent=intent.get("situation"), 
            tone=tone.get("tone")
        )