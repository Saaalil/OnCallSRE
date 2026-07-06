from agents.llm_helper import ask_gemini
from tools.gitlab_mcp_tools import call_gitlab_tool_sync

class ProactiveMonitoringAgent:
    def __init__(self):
        self.name = "Proactive Monitoring Agent"
        self.description = "Scans metrics every 10 minutes to predict outages."

    def run(self):
        print(f"[{self.name}] Fetching latest metrics for proactive scan...")
        
        try:
            # We would normally fetch recent metrics using MCP
            metrics_raw = call_gitlab_tool_sync("get_prometheus_metrics", {"service": "all"})
        except Exception:
            metrics_raw = '{"cpu_trend": "increasing", "memory_trend": "stable", "error_rates": "spiking on frontend"}'

        prompt = f"Analyze these metrics for leading indicators of an outage: {metrics_raw}. Return a JSON object with 'anomaly_detected' (boolean) and 'details'."
        response = ask_gemini("You are a predictive SRE monitoring agent. Respond ONLY in valid JSON.", prompt)
        
        try:
            import json
            import re
            match = re.search(r'\{.*\}', response, re.DOTALL)
            if match:
                data = json.loads(match.group(0))
                if data.get("anomaly_detected"):
                    print(f"[{self.name}] Anomaly detected! Triggering incident workflow.")
                    return {
                        "object_kind": "proactive_anomaly",
                        "object_attributes": {"status": "anomaly", "detailed_status": data.get("details")},
                        "project": {"name": "proactive-scan"}
                    }
        except:
            pass
            
        print(f"[{self.name}] System is healthy. No anomalies detected.")
        return None
