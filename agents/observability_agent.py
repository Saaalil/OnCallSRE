from tools.gitlab_mcp_tools import call_gitlab_tool_sync
from agents.llm_helper import ask_gemini
import json

class ObservabilityAgent:
    def __init__(self):
        self.name = "Observability Agent"
        self.description = "Collects logs, traces, and metrics."

    def run(self, context):
        service = context.get('affected_service', 'unknown')
        print(f"[{self.name}] Collecting metrics for {service}...")
        
        # Here we would normally use the MCP tool. For the demo, if the tool isn't fully 
        # configured on the GitLab side, we fallback gracefully.
        try:
            # We attempt to call a metrics tool on the MCP server if available
            metrics_raw = call_gitlab_tool_sync("get_prometheus_metrics", {"service": service})
        except Exception as e:
            # Placeholder for Prometheus / Grafana metrics for the hackathon demo
            metrics_raw = json.dumps({
                "source": "Prometheus/Grafana",
                "status": "success",
                "data": {
                    "resultType": "matrix",
                    "result": [
                        {
                            "metric": {"__name__": "process_cpu_seconds_total", "job": service},
                            "values": [[1700000000, "0.12"], [1700000060, "0.98"], [1700000120, "0.99"]]
                        },
                        {
                            "metric": {"__name__": "go_memstats_alloc_bytes", "job": service},
                            "values": [[1700000000, "150000000"], [1700000060, "850000000"], [1700000120, "1200000000"]]
                        }
                    ],
                    "alerts": [
                        {"alertname": "HighCPUUsage", "severity": "critical", "state": "firing"},
                        {"alertname": "MemoryLeakDetected", "severity": "critical", "state": "firing"}
                    ]
                }
            })
            
        prompt = f"Summarize these raw metrics into a diagnostic package for service {service}: {metrics_raw}"
        diagnostic = ask_gemini("You are an SRE Observability expert.", prompt)
        
        return {"status": "collected", "diagnostic_summary": diagnostic}
