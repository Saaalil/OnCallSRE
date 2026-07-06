import os
from flask import Flask, request, jsonify, render_template
from agents.root_agent import RootAgent
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler

load_dotenv()

app = Flask(__name__, template_folder="templates", static_folder="static")
orchestrator = RootAgent()

def proactive_scan_job():
    print("[Proactive Scan] Running scheduled scan...")
    try:
        from agents.monitoring_agent import ProactiveMonitoringAgent
        agent = ProactiveMonitoringAgent()
        anomaly_payload = agent.run()
        if anomaly_payload:
            orchestrator.handle_incident(anomaly_payload)
    except Exception as e:
        print(f"Proactive scan error: {e}")

# Start the 10-minute background scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(func=proactive_scan_job, trigger="interval", minutes=10)
scheduler.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webhook/gitlab', methods=['POST'])
def gitlab_webhook():
    """
    Receives webhooks from GitLab (e.g. Pipeline Failed)
    and triggers the Always-On-CallSRE agent workflow.
    """
    payload = request.json
    print("Received GitLab Webhook. Triggering Agents...")
    
    # Run the orchestrator synchronously for this demo
    try:
        result_context = orchestrator.handle_incident(payload)
        return jsonify({"status": "success", "result": result_context}), 200
    except Exception as e:
        print(f"Error processing incident: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/proactive-check', methods=['POST'])
def run_proactive_check():
    """Manual trigger for the proactive scan (for hackathon demo)."""
    try:
        from agents.monitoring_agent import ProactiveMonitoringAgent
        agent = ProactiveMonitoringAgent()
        anomaly_payload = agent.run()
        
        if anomaly_payload:
            result_context = orchestrator.handle_incident(anomaly_payload)
            return jsonify({"status": "success", "anomaly_found": True, "result": result_context}), 200
        else:
            return jsonify({"status": "success", "anomaly_found": False}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "Always-On-CallSRE"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
