import os
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from styles import load_css
from components import render_sidebar
from components.footer import render_footer
from components.page_header import render_page_header
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
FAVICON_PATH = ROOT / "assets" / "favicon.ico"

# ----------------- PAGE CONFIG -----------------
st.set_page_config(
    page_title="CipherVista | Threat Intelligence",
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

render_sidebar(active_page="threat_intelligence")

render_page_header(
    "Threat Intelligence Center",
    "Investigate indicators, adversaries and emerging threats"
)

with st.sidebar:
    st.markdown("### 🛡️ SOC Telemetry Nodes")
    if st.button("🚪 Terminate Session", use_container_width=True):
        st.session_state["access_token"] = None
        st.query_params.clear()
        st.rerun()

# Load universal CSS from styles.py
st.markdown(load_css(), unsafe_allow_html=True)

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# ----------------- AUTH GUARD -----------------
if not st.session_state.get("access_token"):
    st.warning("Please log in from the main portal first.")
    if st.button("Go to Login"):
        st.switch_page("app.py")
    st.stop()

token = st.session_state["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# ----------------- UTILS -----------------
def get_badge_cls(level):
    lvl = str(level).lower()
    if "critical" in lvl: return "cv-badge cv-critical"
    if "high" in lvl: return "cv-badge cv-warning"
    if "medium" in lvl: return "cv-badge cv-warning"
    if "low" in lvl: return "cv-badge cv-live"
    return "cv-badge"

# ----------------- FETCH BACKEND DATA -----------------
try:
    resp = requests.get(f"{API_URL}/threat-intelligence/overview", headers=headers)
    data = resp.json() if resp.status_code == 200 else {}
except Exception:
    data = {}

active_threats = data.get("active_threats", 1248)
new_iocs = data.get("new_iocs", 5732)
threat_actors_count = data.get("threat_actors_count", 312)
global_risk = data.get("global_risk", "High")
malicious_ips = data.get("malicious_ips", [])
recent_iocs = data.get("recent_iocs", [])
sources = data.get("sources", [])

# ----------------- HEADER & TABS -----------------
st.markdown('<div class="cv-section-title">Threat Intelligence</div>', unsafe_allow_html=True)
st.markdown('<div class="cv-card-subtitle" style="margin-bottom: 25px;">Real-time threat intelligence, IOCs, threat actors and global attack landscape.</div>', unsafe_allow_html=True)

tabs = st.tabs([
    "Overview", 
    "Threat Feeds", 
    "IOCs", 
    "Threat Actors", 
    "Malware", 
    "Vulnerabilities", 
    "TTPs", 
    "Reports"
])

# =====================================================
# TAB 0: OVERVIEW
# =====================================================
with tabs[0]:
    # KPI Cards matching Dataset Analysis styling
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    with kpi1:
        st.markdown(f"""
        <div class="cv-card" style="padding:20px; margin-bottom:0px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span class="cv-card-subtitle" style="font-size:14px; font-weight:600;">Active Threats</span>
                <span class="cv-badge cv-critical">LIVE</span>
            </div>
            <div class="cv-value" style="font-size:32px; font-weight:800; margin:10px 0;">{active_threats:,}</div>
            <div class="cv-label" style="font-size:12px; color:#F87171;">↗ 18% from yesterday</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi2:
        st.markdown(f"""
        <div class="cv-card" style="padding:20px; margin-bottom:0px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span class="cv-card-subtitle" style="font-size:14px; font-weight:600;">New IOCs (24h)</span>
                <span class="cv-badge cv-live">LIVE</span>
            </div>
            <div class="cv-value" style="font-size:32px; font-weight:800; margin:10px 0;">{new_iocs:,}</div>
            <div class="cv-label" style="font-size:12px; color:#4ADE80;">↗ 24% from yesterday</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi3:
        st.markdown(f"""
        <div class="cv-card" style="padding:20px; margin-bottom:0px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span class="cv-card-subtitle" style="font-size:14px; font-weight:600;">Threat Actors</span>
                <span class="cv-badge">ACTIVE</span>
            </div>
            <div class="cv-value" style="font-size:32px; font-weight:800; margin:10px 0;">{threat_actors_count}</div>
            <div class="cv-label" style="font-size:12px; color:#60A5FA;">↗ 7% from yesterday</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi4:
        st.markdown(f"""
        <div class="cv-card" style="padding:20px; margin-bottom:0px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span class="cv-card-subtitle" style="font-size:14px; font-weight:600;">Global Risk Level</span>
                <span class="cv-badge cv-warning">ELEVATED</span>
            </div>
            <div class="cv-value" style="font-size:32px; font-weight:800; margin:10px 0; color:#FBBF24;">{global_risk}</div>
            <div class="cv-label" style="font-size:12px; color:#FBBF24;">⚡ High severity threats detected</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='cv-divider' style='margin:25px 0;'></div>", unsafe_allow_html=True)

    col_left, col_right = st.columns([2.2, 1], gap="large")

    with col_left:
        st.markdown('<div class="cv-value" style="margin-bottom: 15px; font-size: 20px;">Global Threat Map</div>', unsafe_allow_html=True)
        with st.container(border=True):
            map_data = malicious_ips if malicious_ips else [
                {"lat": 55.75, "lon": 37.61, "ip": "185.234.218.45", "risk": "Critical"},
                {"lat": 52.36, "lon": 4.90, "ip": "176.31.103.27", "risk": "High"},
                {"lat": 1.35, "lon": 103.81, "ip": "103.87.12.56", "risk": "High"},
                {"lat": 38.89, "lon": -77.03, "ip": "45.77.23.199", "risk": "Medium"},
                {"lat": 51.16, "lon": 10.45, "ip": "94.102.49.12", "risk": "Low"}
            ]
            df_map = pd.DataFrame(map_data)
            if not df_map.empty and "lat" in df_map.columns:
                fig = px.scatter_geo(
                    df_map, lat="lat", lon="lon", hover_name="ip", color="risk",
                    color_discrete_map={"Critical": "#ef4444", "High": "#f59e0b", "Medium": "#fbbf24", "Low": "#10b981"},
                    projection="natural earth"
                )
                fig.update_geos(bgcolor="rgba(0,0,0,0)", landcolor="#1E293B", oceancolor="rgba(0,0,0,0)", showcountries=True, countrycolor="#334155")
                fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=320, legend=dict(orientation="h", yanchor="bottom", y=0.01, xanchor="right", x=0.99, font=dict(color="#94A3B8")))
                st.plotly_chart(fig, use_container_width=True)

        c_ip, c_ioc = st.columns(2)
        with c_ip:
            st.markdown('<div class="cv-value" style="margin-bottom: 10px;">Top Malicious IPs</div>', unsafe_allow_html=True)
            display_ips = malicious_ips[:4] if malicious_ips else [
                {"ip": "185.234.218.45", "country": "Russian Federation", "risk": "Critical"},
                {"ip": "176.31.103.27", "country": "Netherlands", "risk": "High"},
                {"ip": "103.87.12.56", "country": "Singapore", "risk": "High"},
                {"ip": "45.77.23.199", "country": "United States", "risk": "Medium"}
            ]
            for item in display_ips:
                r_cls = get_badge_cls(item.get("risk", "High"))
                st.markdown(f"""
                <div class="cv-item" style="margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div class="cv-value" style="font-size: 15px;">🌐 {item.get('ip')}</div>
                        <div class="cv-label" style="font-size: 12px;">{item.get('country')}</div>
                    </div>
                    <span class='{r_cls}'>{item.get('risk', 'High')}</span>
                </div>
                """, unsafe_allow_html=True)

        with c_ioc:
            st.markdown('<div class="cv-value" style="margin-bottom: 10px;">Recent IOCs</div>', unsafe_allow_html=True)
            display_iocs = recent_iocs[:4] if recent_iocs else [
                {"indicator": "e3f5a7d3b2c1e9f8a6...", "type": "SHA256", "created_at": "2 min ago"},
                {"indicator": "185.234.218.45", "type": "IP Address", "created_at": "2 min ago"},
                {"indicator": "a1b2c3d4e5f6g7h8i9...", "type": "MD5", "created_at": "5 min ago"},
                {"indicator": "hxxp://malicious[.]ru", "type": "URL", "created_at": "7 min ago"}
            ]
            for ioc in display_iocs:
                st.markdown(f"""
                <div class="cv-item" style="margin-bottom: 10px;">
                    <div class="cv-value" style="font-size: 15px; font-family: monospace;">🔗 {ioc.get('indicator')}</div>
                    <div class="cv-label" style="font-size: 12px;">{ioc.get('type')} • {ioc.get('created_at')}</div>
                </div>
                """, unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="cv-value" style="margin-bottom: 15px; font-size: 20px;">Live Threat Feed</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class='cv-item' style='border-left: 4px solid #EF4444; margin-bottom: 12px;'>
            <div class='cv-value' style='font-size: 14px;'>🔴 New Ransomware Campaign</div>
            <div class='cv-label' style='font-size: 12px;'>LockBit 3.0 targeting healthcare sector</div>
            <div class='cv-label' style='font-size: 10px; margin-top: 4px;'>2 min ago</div>
        </div>
        <div class='cv-item' style='border-left: 4px solid #F59E0B; margin-bottom: 12px;'>
            <div class='cv-value' style='font-size: 14px;'>🟠 Malicious IP Communication</div>
            <div class='cv-label' style='font-size: 12px;'>185.234.218.45 flagged for C2 activity</div>
            <div class='cv-label' style='font-size: 10px; margin-top: 4px;'>8 min ago</div>
        </div>
        <div class='cv-item' style='border-left: 4px solid #F59E0B; margin-bottom: 12px;'>
            <div class='cv-value' style='font-size: 14px;'>🟠 Phishing Kit Detected</div>
            <div class='cv-label' style='font-size: 12px;'>New 16Shop phishing kit in the wild</div>
            <div class='cv-label' style='font-size: 10px; margin-top: 4px;'>15 min ago</div>
        </div>
        <div class='cv-item' style='border-left: 4px solid #FBBF24; margin-bottom: 12px;'>
            <div class='cv-value' style='font-size: 14px;'>🟡 Vulnerability Exploitation</div>
            <div class='cv-label' style='font-size: 12px;'>Apache ActiveMQ RCE attempt</div>
            <div class='cv-label' style='font-size: 10px; margin-top: 4px;'>21 min ago</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="cv-value" style="margin-top: 25px; margin-bottom: 15px; font-size: 20px;">Top Threats by Category</div>', unsafe_allow_html=True)
        cat_df = pd.DataFrame({"Category": ["Malware", "Phishing", "C2 Activity", "Exploits", "Other"], "Percentage": [42, 28, 18, 7, 5]})
        fig_pie = px.pie(cat_df, names="Category", values="Percentage", hole=0.7, color_discrete_sequence=["#EF4444", "#F59E0B", "#3B82F6", "#8B5CF6", "#64748B"])
        fig_pie.update_layout(margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=200, showlegend=False)
        st.plotly_chart(fig_pie, use_container_width=True)

# =====================================================
# TAB 1: THREAT FEEDS
# =====================================================
with tabs[1]:
    st.markdown('<div class="cv-value" style="font-size: 22px;">Global RSS & Threat Feeds</div>', unsafe_allow_html=True)
    st.markdown('<div class="cv-card-subtitle" style="margin-bottom: 20px;">Aggregated threat intelligence streams refreshed every 5 minutes.</div>', unsafe_allow_html=True)

    f_col1, f_col2 = st.columns([3, 1])
    with f_col1:
        feed_search = st.text_input("Search Feeds", placeholder="Search by advisory title, CVE, or keyword...")
    with f_col2:
        feed_source_filter = st.selectbox("Source Filter", ["All Sources", "CISA Advisory", "MITRE ATT&CK", "AlienVault OTX", "BleepingComputer", "The Hacker News"])
    
    st.markdown("<div class='cv-divider'></div>", unsafe_allow_html=True)

    feeds_data = [
        {"title": "LockBit 3.0 Ransomware Deployment via Exposed RDP Services", "source": "CISA Advisory", "severity": "Critical", "time": "5 mins ago", "cve": "CVE-2026-4412"},
        {"title": "Zero-Day Remote Code Execution Vulnerability in Enterprise VPN Gateways", "source": "BleepingComputer", "severity": "Critical", "time": "18 mins ago", "cve": "CVE-2026-1092"},
        {"title": "APT28 Phishing Campaign Targeting Defense Contractors in Eastern Europe", "source": "AlienVault OTX", "severity": "High", "time": "42 mins ago", "cve": "T1566.002"},
        {"title": "Apache Tomcat Information Disclosure Vulnerability Notice", "source": "MITRE ATT&CK", "severity": "Medium", "time": "3 hours ago", "cve": "CVE-2026-3821"}
    ]

    for item in feeds_data:
        if feed_search and feed_search.lower() not in item["title"].lower() and feed_search.lower() not in item["cve"].lower():
            continue
        if feed_source_filter != "All Sources" and feed_source_filter != item["source"]:
            continue

        with st.container(border=True):
            c_info, c_badge, c_act = st.columns([4, 1, 1])
            with c_info:
                st.markdown(f"""
                <div class="cv-value" style="font-size: 16px;">📌 {item['title']}</div>
                <div class="cv-label" style="font-size: 13px; margin-top: 4px;">Source: <b style="color:#F8FAFC;">{item['source']}</b> • Indicator: <code style="color:#60A5FA; background:transparent;">{item['cve']}</code> • {item['time']}</div>
                """, unsafe_allow_html=True)
            with c_badge:
                st.markdown(f"<div style='margin-top: 10px;'><span class='{get_badge_cls(item['severity'])}'>{item['severity']}</span></div>", unsafe_allow_html=True)
            with c_act:
                st.markdown("<div style='margin-top: 5px;'></div>", unsafe_allow_html=True)
                if st.button("View IOCs", key=f"feed_{item['cve']}"):
                    st.toast(f"Loading intelligence bundle for {item['cve']}")

# =====================================================
# TAB 2: IOCS
# =====================================================
with tabs[2]:
    st.markdown('<div class="cv-value" style="font-size: 22px;">Indicators of Compromise Repository</div>', unsafe_allow_html=True)
    st.markdown('<div class="cv-card-subtitle" style="margin-bottom: 20px;">Extracted and verified IOCs from automated dataset audits and public security feeds.</div>', unsafe_allow_html=True)

    i_col1, i_col2 = st.columns([3, 1])
    with i_col1:
        ioc_search = st.text_input("Search Indicator", placeholder="Search by IP address, domain, MD5, SHA256...")
    with i_col2:
        ioc_type_filter = st.selectbox("IOC Type", ["All Types", "IP Address", "SHA256 Hash", "MD5 Hash", "URL", "Domain"])

    st.markdown("<div class='cv-divider'></div>", unsafe_allow_html=True)

    iocs_table = [
        {"indicator": "185.234.218.45", "type": "IP Address", "confidence": "99.4%", "risk": "Critical", "report": "Network Threat Audit"},
        {"indicator": "e3f5a7d3b2c1e9f8a6d4bc81029384f1", "type": "SHA256 Hash", "confidence": "98.1%", "risk": "Critical", "report": "Malware Sample #44"},
        {"indicator": "hxxp://phishing-login-portal[.]com/auth", "type": "URL", "confidence": "91.8%", "risk": "High", "report": "Phishing Kit Analysis"},
        {"indicator": "176.31.103.27", "type": "IP Address", "confidence": "88.2%", "risk": "Medium", "report": "Web Server Recon"}
    ]

    for idx, row in enumerate(iocs_table):
        if ioc_search and ioc_search.lower() not in row["indicator"].lower(): continue
        if ioc_type_filter != "All Types" and ioc_type_filter not in row["type"]: continue

        with st.container(border=True):
            r_cols = st.columns([3, 1.5, 1, 1, 1.5, 1])
            with r_cols[0]: st.markdown(f"<div class='cv-value' style='font-family: monospace; font-size: 14px;'>{row['indicator'][:25]}...</div>", unsafe_allow_html=True)
            with r_cols[1]: st.markdown(f"<div class='cv-label' style='margin-top: 6px;'>{row['type']}</div>", unsafe_allow_html=True)
            with r_cols[2]: st.markdown(f"<div class='cv-value' style='font-size: 14px;'>{row['confidence']}</div>", unsafe_allow_html=True)
            with r_cols[3]: st.markdown(f"<div style='margin-top: 4px;'><span class='{get_badge_cls(row['risk'])}'>{row['risk']}</span></div>", unsafe_allow_html=True)
            with r_cols[4]: st.markdown(f"<div class='cv-label' style='margin-top: 6px;'>{row['report']}</div>", unsafe_allow_html=True)
            with r_cols[5]:
                if st.button("Export", key=f"ioc_{idx}"): st.toast(f"Exported: {row['indicator'][:10]}")

# =====================================================
# TAB 3: THREAT ACTORS
# =====================================================
with tabs[3]:
    st.markdown('<div class="cv-value" style="font-size: 22px;">Known Advanced Persistent Threats (APT) & Gangs</div>', unsafe_allow_html=True)
    st.markdown('<div class="cv-card-subtitle" style="margin-bottom: 20px;">Catalog of global threat actor profiles mapped against active campaigns.</div>', unsafe_allow_html=True)

    actors = [
        {"name": "APT28 (Fancy Bear)", "origin": "Russian Federation", "target": "Defense, Government, Aerospace", "malware": "XAgent, Sofacy"},
        {"name": "Lazarus Group", "origin": "North Korea", "target": "Financial Institutions, Cryptocurrency", "malware": "AppleJeus, Manuscrypt"},
        {"name": "LockBit Syndicate", "origin": "Global Cyber Syndicate", "target": "Healthcare, Manufacturing, Retail", "malware": "LockBit 3.0 Ransomware"}
    ]

    for actor in actors:
        with st.container(border=True):
            ac1, ac2, ac3 = st.columns([2.5, 2.5, 1])
            with ac1:
                st.markdown(f"""
                <div class="cv-value" style="font-size: 16px;">🕵️‍♂️ {actor['name']}</div>
                <div class="cv-label" style="margin-top: 4px;">Origin: <b style="color:#F8FAFC;">{actor['origin']}</b></div>
                """, unsafe_allow_html=True)
            with ac2:
                st.markdown(f"""
                <div class="cv-value" style="font-size: 14px;">🎯 Targets: {actor['target']}</div>
                <div class="cv-label" style="color: #60A5FA; margin-top: 4px;">Malware: {actor['malware']}</div>
                """, unsafe_allow_html=True)
            with ac3:
                st.markdown("<div style='margin-top: 8px;'></div>", unsafe_allow_html=True)
                if st.button("Profile", key=f"act_{actor['name'][:5]}"): st.toast("Loaded profile")

# =====================================================
# TAB 4: MALWARE
# =====================================================
with tabs[4]:
    st.markdown('<div class="cv-value" style="font-size: 22px;">Malware Intelligence & Signature Database</div>', unsafe_allow_html=True)
    st.markdown('<div class="cv-card-subtitle" style="margin-bottom: 20px;">Analyzed malware samples, behavior characteristics, and AV detection rates.</div>', unsafe_allow_html=True)

    m_col1, m_col2 = st.columns([3, 1])
    with m_col1:
        malware_search = st.text_input("Search Malware", placeholder="Search family name, category, or signature...")
    with m_col2:
        malware_cat = st.selectbox("Malware Type", ["All Types", "Ransomware", "Trojan / Dropper", "Information Stealer", "Command & Control", "Spyware"])

    st.markdown("<div class='cv-divider'></div>", unsafe_allow_html=True)

    malware_list = [
        {"family": "LockBit 3.0", "type": "Ransomware", "hash_type": "SHA256", "hash": "e3f5a7d3b2c1e9f8a6d4bc81029384f1a2b3c4d5", "risk": "Critical", "detections": "58/65 Engines", "behavior": "Encrypts NTFS drives, disables VSS volume shadow copies."},
        {"family": "Emotet Dropper", "type": "Trojan / Dropper", "hash_type": "MD5", "hash": "a1b2c3d4e5f6g7h8i9j0123456789abc", "risk": "Critical", "detections": "62/65 Engines", "behavior": "Polymorphic DLL dropper injected via malicious Office macros."},
        {"family": "RedLine Stealer", "type": "Information Stealer", "hash_type": "SHA256", "hash": "7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a", "risk": "High", "detections": "45/65 Engines", "behavior": "Harvests browser credentials, crypto wallets, and system tokens."},
        {"family": "Cobalt Strike Beacon", "type": "Command & Control", "hash_type": "SHA1", "hash": "d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3", "risk": "Critical", "detections": "60/65 Engines", "behavior": "Memory resident C2 beacon facilitating lateral movement."},
        {"family": "Agent Tesla", "type": "Spyware", "hash_type": "MD5", "risk": "Medium", "hash": "9f8e7d6c5b4a3f2e1d0c9b8a7f6e5d4c", "detections": "38/65 Engines", "behavior": "Keylogger and screen capture module exfiltrating over SMTP/FTP."}
    ]

    for m_idx, m in enumerate(malware_list):
        if malware_search and malware_search.lower() not in m["family"].lower() and malware_search.lower() not in m["behavior"].lower():
            continue
        if malware_cat != "All Types" and malware_cat not in m["type"]:
            continue

        with st.container(border=True):
            mc1, mc2, mc3, mc4 = st.columns([2.5, 1.5, 1.5, 1])
            with mc1:
                st.markdown(f"""
                <div class="cv-value" style="font-size: 16px;">🦠 {m['family']}</div>
                <div class="cv-label" style="margin-top: 2px;">Category: <b style="color:#F8FAFC;">{m['type']}</b></div>
                <div class="cv-label" style="font-size:11px; margin-top:4px;">{m['behavior']}</div>
                """, unsafe_allow_html=True)
            with mc2:
                st.markdown(f"""
                <div class="cv-label">Signature Hash ({m['hash_type']})</div>
                <div class="cv-value" style="font-size: 12px; font-family: monospace; color:#60A5FA;">{m['hash'][:18]}...</div>
                """, unsafe_allow_html=True)
            with mc3:
                st.markdown(f"""
                <div class="cv-label">AV Detection Ratio</div>
                <div class="cv-value" style="font-size: 14px;">{m['detections']}</div>
                """, unsafe_allow_html=True)
            with mc4:
                st.markdown(f"""
                <div style="margin-top: 4px;"><span class="{get_badge_cls(m['risk'])}">{m['risk']}</span></div>
                """, unsafe_allow_html=True)

# =====================================================
# TAB 5: VULNERABILITIES
# =====================================================
with tabs[5]:
    st.markdown('<div class="cv-value" style="font-size: 22px;">Vulnerabilities & CVE Feed (NVD Integrated)</div>', unsafe_allow_html=True)
    st.markdown('<div class="cv-card-subtitle" style="margin-bottom: 20px;">Live National Vulnerability Database (NVD) stream with CVSS score ratings.</div>', unsafe_allow_html=True)

    v_col1, v_col2 = st.columns([3, 1])
    with v_col1:
        cve_search = st.text_input("Search CVE / Product", placeholder="Search by CVE ID, product name, or keyword...")
    with v_col2:
        cvss_filter = st.selectbox("CVSS Severity", ["All Severities", "Critical (9.0 - 10.0)", "High (7.0 - 8.9)", "Medium (4.0 - 6.9)"])

    st.markdown("<div class='cv-divider'></div>", unsafe_allow_html=True)

    cves = [
        {"cve": "CVE-2026-1234", "cvss": "9.8 Critical", "desc": "Unauthenticated Remote Code Execution (RCE) in enterprise logging core.", "product": "Apache Log4j < 2.19", "date": "10 mins ago"},
        {"cve": "CVE-2026-5510", "cvss": "8.8 High", "desc": "Privilege escalation vulnerability in Windows Kernel driver API handling.", "product": "MS Windows Server 2025", "date": "1 hour ago"},
        {"cve": "CVE-2026-0982", "cvss": "7.5 High", "desc": "SQL Injection vulnerability in CMS core database sanitization routines.", "product": "WordPress Core < 6.7", "date": "3 hours ago"},
        {"cve": "CVE-2026-3321", "cvss": "6.5 Medium", "desc": "Cross-Site Scripting (XSS) in admin dashboard component libraries.", "product": "ReactJS Admin Core", "date": "5 hours ago"}
    ]

    for cve_item in cves:
        cve_id = cve_item["cve"]
        score_val = cve_item["cvss"]

        if cve_search and cve_search.lower() not in cve_id.lower() and cve_search.lower() not in cve_item["product"].lower() and cve_search.lower() not in cve_item["desc"].lower():
            continue
        if cvss_filter != "All Severities" and cvss_filter.split(" ")[0] not in score_val:
            continue

        with st.container(border=True):
            cc1, cc2, cc3 = st.columns([3, 1.5, 1])
            with cc1:
                st.markdown(f"""
                <div class="cv-value" style="font-size: 16px;">🔓 {cve_id}</div>
                <div class="cv-label" style="font-size: 13px; margin-top: 2px;">{cve_item['desc']}</div>
                <div class="cv-label" style="font-size: 11px; color:#64748B; margin-top: 4px;">Affected: <b style="color:#94A3B8;">{cve_item['product']}</b> • Detected {cve_item['date']}</div>
                """, unsafe_allow_html=True)
            with cc2:
                st.markdown(f"""
                <div class="cv-label">CVSS Severity Rating</div>
                <div style="margin-top:4px;"><span class="{get_badge_cls(score_val)}">{score_val}</span></div>
                """, unsafe_allow_html=True)
            with cc3:
                st.markdown("<div style='margin-top: 8px;'></div>", unsafe_allow_html=True)
                if st.button("NVD Lookup", key=f"cve_btn_{cve_id}"):
                    st.toast(f"Connecting to NVD database API for {cve_id}...")

# =====================================================
# TAB 6: TTPS (MITRE ATT&CK MAPPING)
# =====================================================
with tabs[6]:
    st.markdown('<div class="cv-value" style="font-size: 22px;">MITRE ATT&CK Framework TTP Mapping</div>', unsafe_allow_html=True)
    st.markdown('<div class="cv-card-subtitle" style="margin-bottom: 20px;">Standardized adversary Tactics, Techniques, and Procedures mapped against active network observations.</div>', unsafe_allow_html=True)

    ttps = [
        {"tech": "T1110", "name": "Brute Force", "tactic": "Credential Access", "desc": "Adversaries attempt login credentials against SSH, RDP, or web authentication portals using automated dictionaries.", "detection": "Monitor for high volume failed authentication events across short windows."},
        {"tech": "T1190", "name": "Exploit Public-Facing Application", "tactic": "Initial Access", "desc": "Adversaries leverage software vulnerabilities in internet-facing web services or APIs to gain code execution.", "detection": "Inspect web application firewall (WAF) logs for abnormal HTTP payload patterns."},
        {"tech": "T1059", "name": "Command and Scripting Interpreter", "tactic": "Execution", "desc": "Execution of malicious commands via PowerShell, Bash, or Python scripts to automate post-compromise activity.", "detection": "Enable process command line logging (Sysmon Event ID 1) and script block logging."},
        {"tech": "T1486", "name": "Data Encrypted for Impact", "tactic": "Impact", "desc": "Ransomware encryption of local file systems and network shares to extort organizations.", "detection": "Monitor file system changes for rapid rename operations and shadow copy deletion commands."},
        {"tech": "T1078", "name": "Valid Accounts", "tactic": "Persistence", "desc": "Adversaries obtain and use credentials of existing enterprise accounts to maintain undetected access.", "detection": "Correlate user login locations against impossible travel metrics and unusual time windows."},
        {"tech": "T1046", "name": "Network Service Discovery", "tactic": "Discovery", "desc": "Adversaries scan network IP ranges to identify listening services and operational ports.", "detection": "Flag internal host port sweeps and TCP SYN packets sent across sequential subnet IPs."}
    ]

    ttp_grid1, ttp_grid2 = st.columns(2)
    for idx, ttp in enumerate(ttps):
        target_col = ttp_grid1 if idx % 2 == 0 else ttp_grid2
        with target_col:
            with st.container(border=True):
                st.markdown(f"""
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span class="cv-value" style="font-size: 20px; font-family: monospace; color:#3B82F6;">{ttp['tech']}</span>
                    <span class="cv-badge">{ttp['tactic']}</span>
                </div>
                <div class="cv-value" style="font-size: 16px; margin-top: 8px;">{ttp['name']}</div>
                <div class="cv-label" style="font-size: 12px; margin-top: 4px;">{ttp['desc']}</div>
                <div class="cv-divider" style="margin: 10px 0;"></div>
                <div class="cv-label" style="font-size: 11px; color:#4ADE80;">🔍 <b>Detection Strategy:</b> {ttp['detection']}</div>
                """, unsafe_allow_html=True)

# =====================================================
# TAB 7: REPORTS
# =====================================================
with tabs[7]:
    st.markdown('<div class="cv-value" style="font-size: 22px;">Historical Assessment Reports</div>', unsafe_allow_html=True)
    st.markdown('<div class="cv-card-subtitle" style="margin-bottom: 20px;">Access full audit reports and generated executive PDF summaries.</div>', unsafe_allow_html=True)

    try:
        rep_resp = requests.get(f"{API_URL}/reports", headers=headers)
        reports_list = rep_resp.json().get("reports", []) if rep_resp.status_code == 200 else []
    except Exception:
        reports_list = []

    if not reports_list:
        st.markdown('<div class="cv-ai">No security assessment reports found in database. Run a dataset analysis first!</div>', unsafe_allow_html=True)
    else:
        for r in reports_list:
            with st.container(border=True):
                rc1, rc2, rc3 = st.columns([3, 1, 1])
                with rc1:
                    st.markdown(f"""
                    <div class="cv-value" style="font-size: 16px;">🛡️ {r.get('report_name')}</div>
                    <div class="cv-label" style="margin-top: 4px;">Dataset: {r.get('dataset_name')} • Threats: {r.get('attacks', 0):,}</div>
                    """, unsafe_allow_html=True)
                with rc2:
                    risk = r.get('risk_level', 'Low')
                    st.markdown(f"<div style='margin-top: 10px;'><span class='{get_badge_cls(risk)}'>{risk}</span></div>", unsafe_allow_html=True)
                with rc3:
                    st.markdown("<div style='margin-top: 5px;'></div>", unsafe_allow_html=True)
                    if st.button("Details", key=f"ti_{r.get('report_id')}"):
                        st.session_state.selected_report_id = r.get('report_id')
                        st.session_state.current_page = "Report Detail View"
                        st.switch_page("pages/Reports.py")
render_footer()