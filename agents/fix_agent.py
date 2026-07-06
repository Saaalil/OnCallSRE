from agents.llm_helper import ask_gemini

class FixAgent:
    def __init__(self):
        self.name = "Fix Generation Agent"
        self.description = "Generates patches and configuration fixes."

    def run(self, context):
        print(f"[{self.name}] Generating code fix using Gemini...")
        hypothesis = context.get('hypothesis', 'Unknown error')
        prompt = f"Generate a git diff patch to fix this root cause: {hypothesis}. Respond with ONLY the diff."
        patch = ask_gemini("You are an expert software engineer fixing a bug.", prompt)
        return {"status": "fix_generated", "patch": patch}
