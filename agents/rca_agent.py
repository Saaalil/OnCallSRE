from agents.llm_helper import ask_gemini
import json

class RCAAgent:
    def __init__(self):
        self.name = "Root Cause Agent"
        self.description = "Analyzes failures and correlates events."

    def run(self, context):
        print(f"[{self.name}] Analyzing context to determine required subagents...")
        
        # Step 1: Manager Agent decides if it's complex
        # For the hackathon demo, we will force it to spin up subagents to show off the capability
        print(f"[{self.name}] Complexity high. Spinning up specialized subagents...")
        
        # Subagent 1: Code Analysis
        print("[Code Analysis Subagent] Scanning git history and logs for code faults...")
        prompt_code = f"Focus ONLY on code-related faults in this context: {json.dumps(context)}"
        code_findings = ask_gemini("You are a Code Analysis Subagent. Keep it brief.", prompt_code)
        
        # Subagent 2: Infrastructure Diagnostics
        print("[Infrastructure Subagent] Scanning metrics for resource exhaustion...")
        prompt_infra = f"Focus ONLY on infrastructure resource exhaustion in this context: {json.dumps(context)}"
        infra_findings = ask_gemini("You are an Infrastructure Diagnostics Subagent. Keep it brief.", prompt_infra)
        
        # Step 2: Manager synthesizes subagent reports
        print(f"[{self.name}] Synthesizing subagent reports into final hypothesis...")
        synthesis_prompt = f"Synthesize these two subagent reports into a final root cause hypothesis:\nCode Findings: {code_findings}\nInfra Findings: {infra_findings}"
        hypothesis = ask_gemini("You are the Principal SRE synthesizing subagent data.", synthesis_prompt)
        
        return {"status": "analyzed", "hypothesis": hypothesis}
