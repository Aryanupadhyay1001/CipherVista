from pathlib import Path
import sys
import time
import plotly.express as px
import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from components.footer import render_footer

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
FAVICON_PATH = ROOT / "assets" / "favicon.ico"

# Path setup
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.capture.interface_manager import InterfaceManager
from src.capture.packet_capture import PacketCapture
from src.ai.gemini_client import GeminiClient
from components import render_sidebar
from styles import load_css
from components.page_header import render_page_header

# 1. Page Configuration
st.set_page_config(
    page_title="CipherVista | Live Monitor",
    page_icon=str(FAVICON_PATH),
    layout="wide"
)

# ----------------- SESSION & TOKEN SYNC -----------------
if "token" in st.query_params and not st.session_state.get("access_token"):
    st.session_state["access_token"] = st.query_params["token"]

# Guard check for individual pages
if st.session_state.get("access_token") is None:
    st.warning("Authentication required. Please log in first.")
    st.switch_page("app.py")
    st.stop()

# Render Custom Sidebar Navigation
render_sidebar(active_page="live_monitoring")

render_page_header(
    "Live Security Monitor",
    "Real-time network telemetry and active threat detection"
)

# 3. CSS Styling for Cyber Cards, Buttons, and Custom Tables
custom_css = """
<style>
    /* Cyber Cards */
    .cyber-card {
        background-color: #111827;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid #1f2937;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .border-blue { border-left: 4px solid #3b82f6; }
    .border-red { border-left: 4px solid #ef4444; }
    .border-teal { border-left: 4px solid #14b8a6; }
    .border-green { border-left: 4px solid #22c55e; }
    .border-orange { border-left: 4px solid #f97316; }
    .border-purple { border-left: 4px solid #a855f7; }
    .border-yellow { border-left: 4px solid #eab308; }

    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }
    
    .card-title {
        color: #f8fafc;
        font-size: 14px;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .card-value {
        font-size: 28px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 2px;
        line-height: 1.2;
    }
    
    .card-subtitle {
        color: #94a3b8;
        font-size: 12px;
        margin-top: 4px;
    }

    /* Severity Badges */
    .badge-critical { background-color: #7f1d1d; color: #fca5a5; padding: 4px 10px; border-radius: 6px; font-weight: 600; font-size: 12px; display: inline-block; text-align: center; }
    .badge-high { background-color: #7c2d12; color: #fdba74; padding: 4px 10px; border-radius: 6px; font-weight: 600; font-size: 12px; display: inline-block; text-align: center; }
    .badge-medium { background-color: #713f12; color: #fde047; padding: 4px 10px; border-radius: 6px; font-weight: 600; font-size: 12px; display: inline-block; text-align: center; }
    .badge-low { background-color: #14532d; color: #86efac; padding: 4px 10px; border-radius: 6px; font-weight: 600; font-size: 12px; display: inline-block; text-align: center; }

    /* Custom Button Styling */
    .stButton > button {
        background-color: #1f2937 !important;
        color: #f8fafc !important;
        border: 1px solid #374151 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.2s ease-in-out !important;
    }
    
    .stButton > button:hover {
        background-color: #374151 !important;
        border-color: #4b5563 !important;
        color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
    }

    .stButton > button[kind="primary"] {
        background-color: #3b82f6 !important;
        border-color: #3b82f6 !important;
        color: #ffffff !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background-color: #2563eb !important;
        border-color: #2563eb !important;
    }

    /* Custom Styled HTML Tables */
    .cyber-table-container {
        background-color: #111827;
        border-radius: 12px;
        border: 1px solid #1f2937;
        padding: 16px;
        margin-bottom: 20px;
        overflow-x: auto;
    }
    
    .cyber-table {
        width: 100%;
        border-collapse: collapse;
        text-align: left;
        font-size: 13px;
        color: #f8fafc;
    }
    
    .cyber-table th {
        color: #94a3b8;
        font-weight: 600;
        padding: 12px 16px;
        border-bottom: 1px solid #1f2937;
        text-transform: uppercase;
        font-size: 11px;
        letter-spacing: 0.5px;
    }
    
    .cyber-table td {
        padding: 12px 16px;
        border-bottom: 1px solid #1e293b;
        color: #e2e8f0;
    }
    
    .cyber-table tr:hover {
        background-color: #1f293755;
    }

    /* Progress bar style for confidence scores */
    .confidence-bar-container {
        background-color: #1f2937;
        border-radius: 4px;
        width: 100px;
        height: 8px;
        display: inline-block;
        overflow: hidden;
        margin-right: 8px;
        vertical-align: middle;
    }
    .confidence-bar-fill {
        background-color: #3b82f6;
        height: 100%;
    }

    /* Styled Section Headers */
    .section-header-box {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-top: 35px;
        margin-bottom: 15px;
        border-bottom: 1px solid #1f2937;
        padding-bottom: 8px;
    }
    .section-header-box h3 {
        color: #f8fafc !important;
        margin: 0 !important;
        font-size: 18px !important;
        font-weight: 600 !important;
    }
</style>
"""
st.markdown(load_css(), unsafe_allow_html=True)
st.markdown(custom_css, unsafe_allow_html=True)

# Sidebar Termination Button Logic
with st.sidebar:
    st.markdown("### 🛡️ SOC Telemetry Nodes")
    if st.button("🚪 Terminate Session", use_container_width=True):
        st.session_state["access_token"] = None
        st.session_state.analysis = None
        st.query_params.clear()
        st.rerun()

# Helper for styled section headers
def render_section_header(title, icon="📊"):
    st.markdown(f"""
    <div class="section-header-box">
        <span style="font-size: 18px;">{icon}</span>
        <h3>{title}</h3>
    </div>
    """, unsafe_allow_html=True)

# 4. Session State Initialization
if "ai_answer" not in st.session_state:
    st.session_state.ai_answer = ""
if "capture" not in st.session_state:
    st.session_state.capture = PacketCapture()

capture = st.session_state.capture
gemini = GeminiClient()

if capture.running:
    st_autorefresh(interval=1000, key="live_refresh")

# 5. Header Section
st.title("🌐 Live Network Monitoring")
st.markdown("Monitor network traffic in real time using CipherVista's live packet capture engine.")
st.divider()

# 6. Data Fetching & Processing
stats = capture.get_statistics()
packets = capture.get_recent_packets()
raw_alerts = capture.get_alerts()

# Deduplicate alerts based on unique fingerprint (Source IP, Destination IP, Protocol, Threat Type)
unique_alerts_map = {}
for alert in raw_alerts:
    key = (alert.source_ip, alert.destination_ip, alert.protocol, alert.threat_type)
    unique_alerts_map[key] = alert

alerts = list(unique_alerts_map.values())

predictions = capture.get_predictions()
alert_stats = capture.get_alert_statistics()

unique_ips = set()
mitre = set()

for alert in alerts:
    unique_ips.add(alert.source_ip)
    unique_ips.add(alert.destination_ip)
    if alert.mitre != "-":
        mitre.add(alert.mitre)

hosts_monitored = len({p.get("src") for p in packets}.union({p.get("dst") for p in packets})) if packets else 0

if predictions:
    avg_confidence = round(sum(float(p["confidence"]) for p in predictions) / len(predictions), 2)
else:
    avg_confidence = 0

# 7. Controls Section
render_section_header("Network Interface & Controls", "⚙️")
left, right = st.columns([2, 1])

with left:
    interfaces = InterfaceManager.get_interfaces()
    interface = st.selectbox(
        "Select Interface",
        options=interfaces,
        format_func=lambda x: f'{x["name"]} ({x["description"]})'
    )
    
    c1, c2 = st.columns(2)
    with c1:
        start = st.button("🟢 Start Monitoring", use_container_width=True, type="primary")
    with c2:
        stop = st.button("🔴 Stop Monitoring", use_container_width=True)

if start:
    capture.start_capture(interface["name"])
    st.success("Monitoring Started")
if stop:
    capture.stop_capture()
    st.warning("Monitoring Stopped")

with right:
    if capture.get_statistics()["running"]:
        st.success(f"### Status\n🟢 Monitoring\n\n**Interface**\n{capture.get_statistics()['interface']}")
    else:
        st.info("### Status\n🔴 Not Monitoring")

st.divider()

# Helper for custom HTML tables
def render_cyber_table(headers, rows_data):
    header_html = "".join([f"<th>{h}</th>" for h in headers])
    rows_html = ""
    for row in rows_data:
        cells_html = "".join([f"<td>{cell}</td>" for cell in row])
        rows_html += f"<tr>{cells_html}</tr>"
    
    return f"""
    <div class="cyber-table-container">
        <table class="cyber-table">
            <thead><tr>{header_html}</tr></thead>
            <tbody>{rows_html}</tbody>
        </table>
    </div>
    """

# 8. Live Statistics (Custom Styled Cards)
render_section_header("Live Statistics", "📊")
k1, k2, k3, k4, k5 = st.columns(5)

def render_card(title, value, subtitle, border_color):
    return f"""
    <div class="cyber-card {border_color}">
        <div class="card-header"><div class="card-title">{title}</div></div>
        <div class="card-value">{value}</div>
        <div class="card-subtitle">{subtitle}</div>
    </div>
    """

with k1: st.markdown(render_card("📦 Total Packets", stats["total_packets"], "Captured locally", "border-blue"), unsafe_allow_html=True)
with k2: st.markdown(render_card("🔗 TCP", stats["tcp_packets"], "Transmission Control", "border-teal"), unsafe_allow_html=True)
with k3: st.markdown(render_card("📡 UDP", stats["udp_packets"], "User Datagram", "border-green"), unsafe_allow_html=True)
with k4: st.markdown(render_card("⚡ ICMP", stats["icmp_packets"], "Control Message", "border-orange"), unsafe_allow_html=True)
with k5: st.markdown(render_card("⏱️ Pkt/Sec", stats["packets_per_second"], "Current throughput", "border-purple"), unsafe_allow_html=True)

st.divider()

# 9. SOC Overview
render_section_header("SOC Overview", "🛡️")
c1, c2, c3, c4, c5 = st.columns(5)

alert_border = "border-red" if len(alerts) > 0 else "border-green"
with c1: st.markdown(render_card("🚨 Active Alerts", len(alerts), "Current threats", alert_border), unsafe_allow_html=True)
with c2: st.markdown(render_card("🖥 Hosts Monitored", hosts_monitored, "Active endpoints", "border-blue"), unsafe_allow_html=True)
with c3: st.markdown(render_card("🌐 Unique IPs", len(unique_ips), "Distinct sources/dest", "border-teal"), unsafe_allow_html=True)
with c4: st.markdown(render_card("🎯 MITRE Techs", len(mitre), "Observed tactics", "border-orange"), unsafe_allow_html=True)
with c5: st.markdown(render_card("🤖 Confidence", f"{avg_confidence}%", "Model accuracy", "border-purple"), unsafe_allow_html=True)

st.divider()

# 10. Threat Statistics
render_section_header("Threat Statistics", "🚨")
a1, a2, a3, a4 = st.columns(4)

with a1: st.markdown(render_card("Total Threats", alert_stats["total"], "All time", "border-blue"), unsafe_allow_html=True)
with a2: st.markdown(render_card("Critical", alert_stats["critical"], "Immediate Action", "border-red"), unsafe_allow_html=True)
with a3: st.markdown(render_card("High", alert_stats["high"], "Elevated Risk", "border-orange"), unsafe_allow_html=True)
with a4: st.markdown(render_card("Medium", alert_stats["medium"], "Monitor closely", "border-yellow"), unsafe_allow_html=True)

st.divider()

# Protocol mapping dictionary for packet capture & predictions
protocol_map = {6: "TCP", 17: "UDP", 1: "ICMP", 2: "IGMP", 50: "ESP", 51: "AH"}

# 11. Threat Analytics (Charts & Alert Table)
if alerts:
    df = pd.DataFrame([
        {
            "Time": alert.time,
            "Threat": alert.threat_type,
            "Severity": alert.severity,
            "Protocol": alert.protocol,
            "Source": alert.source_ip
        }
        for alert in alerts
    ])
    df["Time"] = pd.to_datetime(df["Time"], format="%H:%M:%S")
    timeline = df.groupby(df["Time"].dt.strftime("%H:%M:%S")).size().reset_index(name="Alerts")

    render_section_header("Threat Analytics", "📊")
    ch1, ch2 = st.columns(2)

    with ch1:
        threat_counts = df["Threat"].value_counts().reset_index()
        threat_counts.columns = ["Threat", "Count"]
        fig = px.bar(threat_counts, x="Threat", y="Count", title="Threat Distribution")
        st.plotly_chart(fig, use_container_width=True)

    with ch2:
        severity_counts = df["Severity"].value_counts().reset_index()
        severity_counts.columns = ["Severity", "Count"]
        fig = px.pie(severity_counts, names="Severity", values="Count", title="Severity Distribution", hole=0.45)
        st.plotly_chart(fig, use_container_width=True)

    ch3, ch4 = st.columns(2)
    with ch3:
        protocol_counts = df["Protocol"].value_counts().reset_index()
        protocol_counts.columns = ["Protocol", "Count"]
        fig = px.pie(protocol_counts, names="Protocol", values="Count", title="Protocol Distribution")
        st.plotly_chart(fig, use_container_width=True)

    with ch4:
        attacker_counts = df["Source"].value_counts().head(5).reset_index()
        attacker_counts.columns = ["Source", "Alerts"]
        fig = px.bar(attacker_counts, x="Source", y="Alerts", title="Top Attack Sources")
        st.plotly_chart(fig, use_container_width=True)

    render_section_header("Threat Timeline", "📈")
    fig = px.line(timeline, x="Time", y="Alerts", markers=True, title="Threat Activity Over Time")
    fig.update_traces(line_shape="spline", line=dict(color="crimson", width=3), marker=dict(size=8, color="crimson"))
    fig.update_layout(height=350, xaxis_title="Time", yaxis_title="Number of Alerts")
    fig.update_xaxes(nticks=12)
    st.plotly_chart(fig, use_container_width=True)

    render_section_header("Live Threat Alerts", "🚨")
    alert_rows = []
    for alert in reversed(alerts):
        sev_lower = alert.severity.lower()
        if sev_lower not in ["critical", "high", "medium", "low"]:
            sev_lower = "low"
        
        severity_badge = f'<span class="badge-{sev_lower}">{alert.severity}</span>'
        detection_badge = f'<span>{alert.detection}</span>'
        mitre_display = "—" if alert.mitre == "-" else f"🎯 {alert.mitre}"

        alert_rows.append([
            alert.time,
            alert.source_ip,
            alert.destination_ip,
            alert.protocol,
            alert.threat_type,
            severity_badge,
            f"{alert.confidence}%",
            detection_badge,
            mitre_display
        ])

    alert_headers = ["Time", "Source", "Destination", "Protocol", "Threat", "Severity", "Confidence", "Detection", "MITRE"]
    st.markdown(render_cyber_table(alert_headers, alert_rows), unsafe_allow_html=True)
else:
    render_section_header("Live Threat Alerts", "🚨")
    st.success("No threats detected.")

st.divider()

# 12. Live Packet Capture Table
render_section_header("Live Packet Capture", "📦")
if packets:
    packet_rows = []
    for p in packets[::-1]:
        proto_val = p.get("protocol") if p.get("protocol") is not None else p.get("proto", "—")
        if isinstance(proto_val, int):
            proto_str = protocol_map.get(proto_val, str(proto_val))
        else:
            proto_str = str(proto_val).upper() if proto_val else "—"

        packet_rows.append([
            p.get("time", "—"),
            p.get("src", "—"),
            p.get("dst", "—"),
            proto_str,
            p.get("length", "—")
        ])
    packet_headers = ["Time", "Source", "Destination", "Protocol", "Length"]
    st.markdown(render_cyber_table(packet_headers, packet_rows), unsafe_allow_html=True)
else:
    st.info("No packets captured yet.")

st.divider()

# 13. AI Incident Analysis & Copilot
render_section_header("AI Incident Analysis", "🤖")
analyses = capture.get_ai_analyses()

# Intelligent Fallback so AI Incident Analysis & Copilot buttons are always available and robust
if not analyses and alerts:
    latest_alert = alerts[-1]
    analyses = [{
        "threat": latest_alert.threat_type,
        "summary": f"Detected {latest_alert.threat_type} traffic from {latest_alert.source_ip} to {latest_alert.destination_ip} using {latest_alert.protocol}.",
        "impact": "Potential network disruption, unauthorized access, or resource exhaustion.",
        "risk": latest_alert.severity,
        "mitre": latest_alert.mitre if latest_alert.mitre != "-" else "T1498 (Network Denial of Service)",
        "recommendations": [
            f"Isolate source IP {latest_alert.source_ip} if malicious activity persists.",
            "Inspect firewall logs and traffic patterns for anomalies.",
            "Ensure rate limiting and intrusion detection rules are active."
        ]
    }]
elif not analyses and predictions:
    latest_pred = predictions[-1]
    analyses = [{
        "threat": latest_pred.get("prediction", "Unknown Threat"),
        "summary": f"ML model detected anomalous traffic from {latest_pred.get('source')} to {latest_pred.get('destination')}.",
        "impact": "Unusual network behavior flagged by machine learning anomaly detection.",
        "risk": "High" if float(latest_pred.get("confidence", 0)) > 80 else "Medium",
        "mitre": "T1046 (Network Service Discovery)",
        "recommendations": [
            f"Review connection logs for {latest_pred.get('source')}.",
            "Verify if this traffic is part of authorized network scanning or routine communication."
        ]
    }]
elif not analyses:
    analyses = [{
        "threat": "General Network Monitoring & Threat Detection",
        "summary": "Monitoring active network interfaces and packet streams for potential security events.",
        "impact": "Low immediate impact; routine monitoring state.",
        "risk": "Low",
        "mitre": "—",
        "recommendations": [
            "Continue passive monitoring.",
            "Start packet capture to analyze live traffic feeds."
        ]
    }]

if analyses:
    analysis = analyses[0]
    st.error(f"### Threat\n{analysis['threat']}")
    st.write("### Summary\n", analysis["summary"])
    st.info(f"**Impact:** {analysis['impact']}")
    st.code(f"MITRE ATT&CK: {analysis['mitre']}")
    st.warning(f"**Risk:** {analysis['risk']}")
    
    st.write("### Recommended Actions")
    for item in analysis["recommendations"]:
        st.markdown(f"- {item}")

st.markdown("---")

render_section_header("AI Incident Copilot", "🤖")
if analyses:
    analysis = analyses[0]
    co1, co2, co3, co4, co5, co6 = st.columns(6)
    with co1: why = st.button("⚠ Why Dangerous?")
    with co2: contain = st.button("🛡 Containment")
    with co3: mitre_btn = st.button("🎯 MITRE")
    with co4: report = st.button("📄 Report")
    with co5: summary_btn = st.button("📝 Summary")
    with co6: confidence = st.button("📊 Confidence")

    question = st.chat_input("Ask the SOC Copilot about this incident...")

    if why: question = "Why is this incident dangerous?"
    elif contain: question = "How should I contain this incident?"
    elif mitre_btn: question = "Explain the MITRE ATT&CK technique involved."
    elif report: question = "Generate a professional SOC incident report."
    elif summary_btn: question = "Summarize this incident."
    elif confidence: question = "Explain the confidence score."

    if question:
        prompt = f"""
        You are a Senior SOC Analyst.
        Incident Details
        Threat: {analysis['threat']}
        Summary: {analysis['summary']}
        Impact: {analysis['impact']}
        Risk: {analysis['risk']}
        MITRE: {analysis['mitre']}
        Recommendations:
        {chr(10).join(analysis['recommendations'])}
        
        Question: {question}
        Answer professionally as a SOC analyst.
        """
        response = gemini.generate(prompt)
        if response:
            st.session_state.ai_answer = response
        else:
            st.error("Unable to contact Gemini.")

if st.session_state.ai_answer:
    st.markdown("---")
    st.subheader("🤖 AI Response")
    st.chat_message("assistant").write(st.session_state.ai_answer)

if analyses:
    analysis = analyses[0]
    with st.expander("📋 Incident Details"):
        st.write("**Threat:**", analysis["threat"])
        st.write("**MITRE:**", analysis["mitre"])
        st.write("**Risk:**", analysis["risk"])
        st.write("**Impact:**", analysis["impact"])
        st.write("**Recommendations:**")
        for rec in analysis["recommendations"]:
            st.write("-", rec)

st.divider()

# 14. ML Predictions
render_section_header("Live ML Predictions", "🤖")
if predictions:
    pred_rows = []
    
    for prediction in reversed(predictions):
        conf_val = round(float(prediction["confidence"]), 2)
        bar_html = f"""
        <div class="confidence-bar-container">
            <div class="confidence-bar-fill" style="width: {conf_val}%;"></div>
        </div>
        {conf_val}%
        """
        
        anomaly_status = "Yes" if bool(prediction["anomaly"]) else "No"
        proto_val = prediction.get("protocol")
        proto_str = protocol_map.get(proto_val, str(proto_val)) if proto_val is not None else "—"
        
        pred_rows.append([
            prediction.get("time", "—"),
            prediction.get("source", "—"),
            prediction.get("destination", "—"),
            proto_str,
            prediction.get("prediction", "—"),
            bar_html,
            anomaly_status,
            round(float(prediction.get("anomaly_score", 0.0)), 4)
        ])
        
    pred_headers = ["Time", "Source", "Destination", "Protocol", "Attack Prediction", "Confidence Score", "Anomaly Status", "Anomaly Score"]
    st.markdown(render_cyber_table(pred_headers, pred_rows), unsafe_allow_html=True)
else:
    st.info("No ML predictions yet.")

render_footer()