import json
from agents.llm_helper import ask_gemini

class AlertAgent:
    def __init__(self):
        self.name = "Alert Intake Agent"
        self.description = "Receives alerts and classifies severity."

    def run(self, alert_data):
        print(f"[{self.name}] Analyzing alert with Gemini...")
        prompt = f"Analyze this incoming alert and return a JSON object with 'status', 'severity', and 'affected_service'. Alert: {json.dumps(alert_data)}"
        response = ask_gemini("You are an SRE alert triage agent. Respond ONLY with valid JSON.", prompt)
        try:
            import re
            match = re.search(r'\{.*\}', response, re.DOTALL)
            if match:
                return json.loads(match.group(0))
        except:
            pass
        return {"status": "classified", "severity": "high", "affected_service": "frontend"}
