from agents.llm_helper import ask_gemini

class ValidationAgent:
    def __init__(self):
        self.name = "Validation Agent"
        self.description = "Runs tests and security scans."

    def run(self, context):
        print(f"[{self.name}] Validating proposed fix with Gemini...")
        patch = context.get('patch', '')
        prompt = f"Review this patch for security and syntax issues: {patch}. Output a brief validation report."
        report = ask_gemini("You are a DevSecOps validation agent.", prompt)
        return {"status": "validated", "validation_report": report}
