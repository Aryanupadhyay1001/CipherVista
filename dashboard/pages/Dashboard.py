import warnings
import base64
from pathlib import Path
import requests
import streamlit as st
from components.footer import render_footer
from components.page_header import render_page_header
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
FAVICON_PATH = ROOT / "assets" / "favicon.ico"
warnings.filterwarnings("ignore", message="X has feature names*")

# ----------------- PAGE CONFIG -----------------
st.set_page_config(
    page_title="CipherVista | SOC Command Center",
    page_icon=str(FAVICON_PATH),
    layout="wide"
)

from styles import load_css
st.markdown(load_css(), unsafe_allow_html=True)

from components import render_sidebar, hero, attack_pie_chart, traffic_bar_chart
st.markdown(load_css(), unsafe_allow_html=True)
render_sidebar("Dashboard")

# ----------------- PROFESSIONAL SOC STYLING -----------------
st.markdown("""
<style>
    .stApp {
        background-color: #07090e;
        color: #e2e8f0;
    }
    
    .soc-header-card {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 27, 75, 0.8) 100%);
        border: 1px solid #1e293b;
        border-radius: 16px;
        padding: 24px 30px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        margin-bottom: 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    /* Enforce identical dimensions and flex layout for alignment */
    .soc-card {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 27, 75, 0.6) 100%);
        border: 1px solid #1e293b;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
        margin-bottom: 16px;
        height: 250px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .soc-card-body {
        flex-grow: 1;
    }
    
    .soc-metric-header {
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        color: #94a3b8;
        margin-bottom: 6px;
    }
    
    .soc-metric-value {
        font-size: 28px;
        font-weight: 900;
        color: #ffffff;
    }

    .badge-live {
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 4px 12px;
        border-radius: 99px;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 0.5px;
    }

    /* Force Streamlit page_link button styling to match consistency */
    [data-testid="stPageLink"] a {
        background-color: rgba(59, 130, 246, 0.15) !important;
        border: 1px solid rgba(59, 130, 246, 0.4) !important;
        color: #60a5fa !important;
        border-radius: 8px !important;
        width: 100% !important;
        text-align: center !important;
        font-weight: 600 !important;
        transition: all 0.2s ease-in-out;
    }
    [data-testid="stPageLink"] a:hover {
        background-color: rgba(59, 130, 246, 0.3) !important;
        border-color: #3b82f6 !important;
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- ASSETS & IMPORTS -----------------
ROOT = Path(__file__).resolve().parent.parent.parent
ASSETS = ROOT / "assets"

def get_image_base64(image_path):
    if image_path.exists():
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""

logo_base64 = get_image_base64(ASSETS / "favicon.ico")
logo_html_tag = f'<img src="data:image/x-icon;base64,{logo_base64}" style="width: 36px; height: 36px; object-fit: contain; border-radius: 8px;" />' if logo_base64 else '<span style="font-size: 28px;">🛡️</span>'

API_URL = "http://127.0.0.1:8000"

# ----------------- SESSION STATE INIT -----------------
if "access_token" not in st.session_state:
    st.session_state["access_token"] = None

if "user_name" not in st.session_state:
    st.session_state["user_name"] = "Operative"

def fetch_user_profile():
    if st.session_state["access_token"]:
        try:
            headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}
            res = requests.get(f"{API_URL}/auth/me", headers=headers, timeout=5)
            if res.status_code == 200:
                data = res.json()
                st.session_state["user_name"] = data.get("name", "Security Analyst")
        except Exception:
            pass

# =====================================================
# AUTHENTICATION CHECK GATE
# =====================================================
if st.session_state["access_token"] is None:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%); border: 1px solid #3b82f6; border-radius: 20px; padding: 32px; box-shadow: 0 0 30px rgba(59, 130, 246, 0.2);">
            <div style="text-align: center; margin-bottom: 24px;">
                {logo_html_tag}
                <h2 style="color: white; margin-top: 10px;">CipherVista SOC</h2>
                <p style="color: #94a3b8; font-size: 13px;">Restricted Area — Authentication Required</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        login_email = st.text_input("Operative Email", key="login_email")
        login_password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Authenticate & Enter", type="primary", use_container_width=True):
            if login_email and login_password:
                try:
                    response = requests.post(
                        f"{API_URL}/auth/login", 
                        json={"email": login_email, "password": login_password}
                    )
                    if response.status_code == 200:
                        token_data = response.json()
                        st.session_state["access_token"] = token_data["access_token"]
                        fetch_user_profile()
                        st.success("Access Granted. Loading Command Center...")
                        st.rerun()
                    else:
                        st.error("Invalid credentials.")
                except requests.RequestException:
                    st.error("Backend connection failed.")
            else:
                st.warning("Please enter email and password.")
else:
    fetch_user_profile()

render_page_header(
        "SOC Command Center",
        "Real-time security posture and threat operations"
    )
    
    # ----------------- COMMAND CENTER LANDING PAGE -----------------
    
st.markdown(f"""
    <div class="cv-header-card">
        <div style="display: flex; align-items: center; gap: 24px;">
            <div style="background: rgba(255,255,255,0.03); padding: 16px; border-radius: 18px; border: 1px solid rgba(255,255,255,0.05); box-shadow: inset 0 4px 20px rgba(0,0,0,0.2);">
                {logo_html_tag}
            </div>
            <div>
                <div class="cv-welcome-text">Welcome back, <span class="cv-user-name-gradient">{st.session_state.get('user_name', 'Operative')}</span></div>
                <div style="color: #94a3b8; font-size: 14px; font-weight: 500; letter-spacing: 0.5px;">
                    <span style="color: #60a5fa; font-weight: 700;">SOC Tier-2</span> <span style="opacity: 0.4; margin: 0 6px;">|</span> Incident Response & Threat Hunting Console
                </div>
            </div>
        </div>
        <div>
            <span class="cv-badge-live-premium">
                <span style="color: #10b981; font-size: 14px;">●</span> SYSTEM DEFENSE ACTIVE
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)


    # Sidebar controls
with st.sidebar:
        st.markdown("### 🛡️ SOC Telemetry Nodes")
        st.markdown(f"**Logged In:** {st.session_state['user_name']}")
        st.markdown("---")
        st.markdown("#### Engine Status")
        st.caption("• Random Forest Classifier: `ONLINE`")
        st.caption("• Isolation Forest Outlier: `ACTIVE`")
        st.caption("• Gemini 2.5 Security Agent: `CONNECTED`")
        st.markdown("---")
        if st.button("🚪 Terminate Session", use_container_width=True):
            st.session_state["access_token"] = None
            st.session_state.analysis = None
            st.rerun()

    # Top KPI Metrics Row (4 Columns for professional density)
k1, k2, k3, k4 = st.columns(4)
with k1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 27, 75, 0.6) 100%); border: 1px solid #1e293b; border-radius: 14px; padding: 18px;">
            <div class="soc-metric-header">Threat Detections</div>
            <div class="soc-metric-value" style="color: #60a5fa;">1,428</div>
            <div style="color: #34d399; font-size: 11px; margin-top: 4px;">↑ 4.2% from baseline</div>
        </div>
        """, unsafe_allow_html=True)
with k2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 27, 75, 0.6) 100%); border: 1px solid #1e293b; border-radius: 14px; padding: 18px;">
            <div class="soc-metric-header">Anomaly Index</div>
            <div class="soc-metric-value" style="color: #f87171;">CRITICAL</div>
            <div style="color: #f87171; font-size: 11px; margin-top: 4px;">Entropy Threshold Exceeded</div>
        </div>
        """, unsafe_allow_html=True)
with k3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 27, 75, 0.6) 100%); border: 1px solid #1e293b; border-radius: 14px; padding: 18px;">
            <div class="soc-metric-header">SIEM Event Ingestion</div>
            <div class="soc-metric-value" style="color: #34d399;">84.5k/s</div>
            <div style="color: #34d399; font-size: 11px; margin-top: 4px;">Zero Packet Loss</div>
        </div>
        """, unsafe_allow_html=True)
with k4:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 27, 75, 0.6) 100%); border: 1px solid #1e293b; border-radius: 14px; padding: 18px;">
            <div class="soc-metric-header">Gemini AI Latency</div>
            <div class="soc-metric-value" style="color: #a78bfa;">240ms</div>
            <div style="color: #94a3b8; font-size: 11px; margin-top: 4px;">Cluster Synchronized</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
st.markdown("### 🧭 Command Center Operation Hub")
st.markdown("<p style='color: #94a3b8; font-size: 13px; margin-bottom: 20px;'>Select a secure subsystem to manage telemetry, incident triage, and defense settings.</p>", unsafe_allow_html=True)

    # Uniform Navigation Cards Grid (Row 1)
r1_c1, r1_c2, r1_c3 = st.columns(3, gap="medium")

with r1_c1:
        st.markdown("""
        <div class="soc-card">
            <div class="soc-card-body">
                <h4 style="color: #60a5fa; margin-top:0; font-size: 16px;">📊 Dataset Analysis</h4>
                <p style="color: #94a3b8; font-size: 12px; line-height: 1.5;">Upload NetFlow traffic captures, execute multi-model inference pipelines, and inspect automated AI briefs.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.page_link("pages/dataset_analysis.py", label="Open Dataset Analysis", icon="📈")

with r1_c2:
        st.markdown("""
        <div class="soc-card">
            <div class="soc-card-body">
                <h4 style="color: #34d399; margin-top:0; font-size: 16px;">⚡ Live Monitoring</h4>
                <p style="color: #94a3b8; font-size: 12px; line-height: 1.5;">Monitor real-time packet telemetry streams, active socket connections, and instant threat alarms.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.page_link("pages/live_monitoring.py", label="Open Live Monitoring", icon="⚡")

with r1_c3:
        st.markdown("""
        <div class="soc-card">
            <div class="soc-card-body">
                <h4 style="color: #a78bfa; margin-top:0; font-size: 16px;">📄 Reports & Dossiers</h4>
                <p style="color: #94a3b8; font-size: 12px; line-height: 1.5;">Access generated executive PDF defense briefings and historical security audit compliance logs.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.page_link("pages/reports.py", label="Open Reports Center", icon="📄")

st.markdown("<div style='height: 5px;'></div>", unsafe_allow_html=True)

    # Uniform Navigation Cards Grid (Row 2)
r2_c1, r2_c2, r2_c3 = st.columns(3, gap="medium")

with r2_c1:
        st.markdown("""
        <div class="soc-card">
            <div class="soc-card-body">
                <h4 style="color: #fbbf24; margin-top:0; font-size: 16px;">🛡️ Threat Intelligence</h4>
                <p style="color: #94a3b8; font-size: 12px; line-height: 1.5;">Query global indicators of compromise (IoCs), signature databases, and advanced actor telemetry.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.page_link("pages/threat_intelligence.py", label="Open Threat Intel", icon="🛡️")

with r2_c2:
        st.markdown("""
        <div class="soc-card">
            <div class="soc-card-body">
                <h4 style="color: #38bdf8; margin-top:0; font-size: 16px;">⚙️ Engine Settings</h4>
                <p style="color: #94a3b8; font-size: 12px; line-height: 1.5;">Configure classifier sensitivity thresholds, API connection parameters, and security notification hooks.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.page_link("pages/settings.py", label="Open Settings", icon="⚙️")

with r2_c3:
        st.markdown("""
        <div class="soc-card">
            <div class="soc-card-body">
                <h4 style="color: #f43f5e; margin-top:0; font-size: 16px;">🔒 Session Security</h4>
                <p style="color: #94a3b8; font-size: 12px; line-height: 1.5;">Review active JWT session tokens, system audit trails, and operative access clearances.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚪 Terminate Session Now", use_container_width=True, type="secondary"):
            st.session_state["access_token"] = None
            st.session_state.analysis = None
            st.rerun()
render_footer()