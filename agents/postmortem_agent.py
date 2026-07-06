from agents.llm_helper import ask_gemini
import json

class PostmortemAgent:
    def __init__(self):
        self.name = "Postmortem Agent"
        self.description = "Generates incident timeline and RCA report."

    def run(self, context):
        print(f"[{self.name}] Generating postmortem report with Gemini...")
        prompt = f"Write a professional SRE Incident Postmortem using this data: {json.dumps(context)}. Use markdown."
        report = ask_gemini("You are a Lead SRE writing an incident postmortem.", prompt)
        return {"status": "completed", "postmortem_report": report}
