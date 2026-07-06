document.addEventListener("DOMContentLoaded", () => {
    const triggerBtn = document.getElementById("trigger-btn");
    const proactiveBtn = document.getElementById("proactive-btn");
    const spinner = triggerBtn.querySelector(".spinner");
    const proSpinner = document.getElementById("proactive-spinner");
    const statusText = document.getElementById("status-text");
    const grid = document.getElementById("dashboard-grid");
    const termOutput = document.getElementById("term-output");

    // Dynamic mock logs for standard reactive workflow
    const reactiveLogs = [
        { text: "[Always-On-CallSRE Orchestrator] Starting incident response workflow...", delay: 200, type: 'info' },
        { text: "Webhook verified. Payload loaded.", delay: 400, type: 'info' },
        { text: "[Alert Intake Agent] Analyzing alert with Gemini...", delay: 1000, type: 'info' },
        { text: "Severity mapped: High. Service: critical-frontend-service.", delay: 1500, type: 'warning' },
        { text: "[Observability Agent] Calling MCP Server for metrics...", delay: 2000, type: 'info' },
        { text: "[GitLabMCPClient] Mocking call to 'get_prometheus_metrics' for demo purposes...", delay: 2100, type: 'warning' },
        { text: "Fallback triggered. Loading Prometheus payload...", delay: 2500, type: 'info' },
        { text: "Extracted 2 active alerts and 2 metric matrices.", delay: 3000, type: 'success' },
        { text: "[Root Cause Agent] Analyzing context to determine required subagents...", delay: 4000, type: 'info' },
        { text: "[Root Cause Agent] Complexity high. Spinning up specialized subagents...", delay: 4500, type: 'warning' },
        { text: "[Code Analysis Subagent] Scanning git history and logs for code faults...", delay: 5000, type: 'info' },
        { text: "[Infrastructure Subagent] Scanning metrics for resource exhaustion...", delay: 5500, type: 'info' },
        { text: "[Root Cause Agent] Synthesizing subagent reports into final hypothesis...", delay: 6500, type: 'success' },
        { text: "[Fix Generation Agent] Generating code patch using Gemini...", delay: 7500, type: 'info' },
        { text: "Patch completed and formatted.", delay: 8500, type: 'success' },
        { text: "[Validation Agent] Running simulated devsecops checks...", delay: 9000, type: 'info' },
        { text: "[Deployment Agent] Creating Merge Request via MCP...", delay: 9500, type: 'info' },
        { text: "[GitLabMCPClient] Mocking call to 'create_merge_request'...", delay: 9600, type: 'warning' },
        { text: "[Postmortem Agent] Writing markdown incident report...", delay: 10000, type: 'info' },
        { text: "[Always-On-CallSRE Orchestrator] Workflow completed successfully.", delay: 10500, type: 'success' }
    ];

    // Dynamic mock logs for proactive workflow
    const proactiveLogs = [
        { text: "[Proactive Monitoring Agent] Fetching latest metrics for proactive scan...", delay: 200, type: 'info' },
        { text: "[GitLabMCPClient] Fetching metrics from MCP...", delay: 800, type: 'info' },
        { text: "[Proactive Monitoring Agent] Gemini analyzing metrics for leading indicators...", delay: 1500, type: 'warning' },
        { text: "[Proactive Monitoring Agent] Anomaly detected! Triggering incident workflow.", delay: 3000, type: 'red' }
    ].concat(reactiveLogs.map(l => ({...l, delay: l.delay + 3000})));

    let logTimeouts = [];

    function clearTerminal() {
        termOutput.innerHTML = "";
        logTimeouts.forEach(clearTimeout);
        logTimeouts = [];
    }

    function addLog(text, type) {
        const line = document.createElement("div");
        line.className = `term-line ${type}`;
        line.innerText = `> ${text}`;
        termOutput.appendChild(line);
        termOutput.scrollTop = termOutput.scrollHeight;
    }

    async function runWorkflow(endpoint, payload, logsArray, btn, currentSpinner) {
        // Reset UI
        triggerBtn.disabled = true;
        proactiveBtn.disabled = true;
        currentSpinner.classList.remove("hidden");
        statusText.classList.remove("hidden");
        statusText.innerText = "Agents are working...";
        statusText.style.color = "var(--primary)";
        grid.classList.remove("hidden");
        
        // Clear old content
        document.querySelectorAll('.card-content').forEach(el => {
            el.innerHTML = "Waiting...";
            el.classList.remove('typing-done');
        });

        clearTerminal();
        addLog("Initializing request...", "info");

        // Schedule mock terminal logs
        logsArray.forEach(log => {
            const t = setTimeout(() => addLog(log.text, log.type), log.delay);
            logTimeouts.push(t);
        });

        try {
            const response = await fetch(endpoint, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: payload ? JSON.stringify(payload) : null
            });

            const data = await response.json();
            
            if (data.status === "success") {
                if(data.anomaly_found === false) {
                    addLog("Proactive scan completed. System is healthy.", "success");
                    statusText.innerText = "System Healthy. No anomalies.";
                    statusText.style.color = "#10b981";
                } else {
                    const res = data.result;
                    
                    statusText.innerText = "Workflow Completed Successfully!";
                    statusText.style.animation = "none";
                    statusText.style.color = "#10b981";

                    // Populate Static Fields immediately
                    document.getElementById('alert-content').innerHTML = `<strong>Severity:</strong> ${res.severity || 'High'}<br><strong>Service:</strong> ${res.affected_service || 'unknown'}`;
                    document.getElementById('obs-content').innerHTML = `<em>${res.diagnostic_summary}</em>`;
                    
                    let mrLink = res.mr_url && res.mr_url.startsWith('http') ? `<a href="${res.mr_url}" target="_blank" style="color:var(--primary)">View Merge Request ↗</a>` : res.mr_url;
                    document.getElementById('dep-content').innerHTML = mrLink || "URL generated.";
                    
                    // Typing Effect for Gemini generated fields
                    typeText('rca-content', res.hypothesis || "No RCA generated.", 15);
                    typeText('fix-content', res.patch || "No patch generated.", 5);
                    typeText('val-content', res.validation_report || "Validation completed.", 20);
                    typeText('post-content', res.postmortem_report || "Report generated.", 5);
                    
                    addLog("Data successfully rendered to dashboard UI.", "success");
                }
            } else {
                statusText.innerText = "Error: " + data.message;
                addLog("ERROR: API returned a failure status.", "red");
            }
        } catch (err) {
            console.error(err);
            statusText.innerText = "Connection failed.";
            addLog("CRITICAL ERROR: Failed to reach backend.", "red");
        } finally {
            triggerBtn.disabled = false;
            proactiveBtn.disabled = false;
            currentSpinner.classList.add("hidden");
        }
    }

    triggerBtn.addEventListener("click", () => {
        const mockPayload = {
            object_kind: "pipeline",
            object_attributes: { id: 12345, status: "failed", detailed_status: "failed on tests" },
            project: { name: "critical-frontend-service" }
        };
        runWorkflow("/webhook/gitlab", mockPayload, reactiveLogs, triggerBtn, spinner);
    });

    proactiveBtn.addEventListener("click", () => {
        runWorkflow("/api/proactive-check", null, proactiveLogs, proactiveBtn, proSpinner);
    });

    function typeText(elementId, text, speed) {
        const el = document.getElementById(elementId);
        el.innerHTML = "";
        let i = 0;
        
        function typeWriter() {
            if (i < text.length) {
                let char = text.charAt(i);
                if(char === '<') char = '&lt;';
                if(char === '>') char = '&gt;';
                
                el.innerHTML += char;
                i++;
                setTimeout(typeWriter, speed);
            } else {
                el.classList.add('typing-done');
            }
        }
        
        typeWriter();
    }
});
