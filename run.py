from agent.main_agent import EmailDrafterAgent
from memory.session_manager import save_to_session

agent = EmailDrafterAgent()

print("Describe the situation:")
user_input = input("> ")

# Agent email generate kar raha hai
result = agent.run(user_input)

# --- YAHAN CODE UPDATE KIYA HAI ---
# Result ko JSON file mein save karne ke liye function call karein
save_to_session(user_input, result)
# ---------------------------------

print("\n--- GENERATED EMAIL ---\n")
print(f"Subject: {result.get('subject', 'No Subject')}\n")
print(result.get('body', 'No Body Content'))
print("\n" + result.get('closing', 'Best regards,'))

print(f"\n✅ Draft saved to memory/session_store.json")