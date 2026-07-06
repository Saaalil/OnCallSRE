from agents.alert_agent import AlertAgent
from agents.observability_agent import ObservabilityAgent
from agents.rca_agent import RCAAgent
from agents.fix_agent import FixAgent
from agents.validation_agent import ValidationAgent
from agents.deployment_agent import DeploymentAgent
from agents.postmortem_agent import PostmortemAgent

class RootAgent:
    def __init__(self):
        self.name = "Always-On-CallSRE Orchestrator"
        self.description = "Orchestrates the multi-agent incident response workflow."
        
        # Initialize sub-agents
        self.alert_agent = AlertAgent()
        self.observability_agent = ObservabilityAgent()
        self.rca_agent = RCAAgent()
        self.fix_agent = FixAgent()
        self.validation_agent = ValidationAgent()
        self.deployment_agent = DeploymentAgent()
        self.postmortem_agent = PostmortemAgent()

    def handle_incident(self, alert_payload: dict):
        print(f"[{self.name}] Starting incident response workflow...")
        
        # Step 1: Alert Intake
        context = self.alert_agent.run(alert_payload)
        
        # Step 2: Observability
        obs_result = self.observability_agent.run(context)
        context.update(obs_result)
        
        # Step 3: Root Cause Analysis
        rca_result = self.rca_agent.run(context)
        context.update(rca_result)
        
        # Step 4: Fix Generation
        fix_result = self.fix_agent.run(context)
        context.update(fix_result)
        
        # Step 5: Validation
        val_result = self.validation_agent.run(context)
        context.update(val_result)
        
        # Step 6: Deployment
        deploy_result = self.deployment_agent.run(context)
        context.update(deploy_result)
        
        # Step 7: Postmortem
        postmortem_result = self.postmortem_agent.run(context)
        context.update(postmortem_result)
        
        print(f"[{self.name}] Incident response workflow completed.")
        return context
