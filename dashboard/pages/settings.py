import os
import streamlit as st
import requests
from components import render_sidebar
from components.footer import render_footer
from components.page_header import render_page_header
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
FAVICON_PATH = ROOT / "assets" / "favicon.ico"

# ----------------- PAGE CONFIG -----------------
st.set_page_config(
    page_title="CipherVista | Settings",
    page_icon=str(FAVICON_PATH),
    layout="wide"
)

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# ----------------- SESSION & TOKEN SYNC -----------------
if "token" in st.query_params and not st.session_state.get("access_token"):
    st.session_state["access_token"] = st.query_params["token"]

# Guard check for individual pages
if st.session_state.get("access_token") is None:
    st.warning("Authentication required. Please log in first.")
    st.switch_page("app.py")
    st.stop()

render_sidebar(active_page="settings")

render_page_header(
    "SOC Configuration",
    "Manage account, security and CipherVista platform preferences"
)

with st.sidebar:
    st.markdown("### 🛡️ SOC Telemetry Nodes")
    if st.button("🚪 Terminate Session", use_container_width=True):
        st.session_state["access_token"] = None
        st.query_params.clear()
        st.rerun()

token = st.session_state["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# ----------------- CUSTOM STYLING -----------------
st.markdown("""
<style>
    .main-header {
        font-size: 28px;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 2px;
    }
    .main-sub {
        color: #94a3b8;
        font-size: 14px;
        margin-bottom: 20px;
    }
    .settings-card {
        background-color: #0f172a;
        border: 1px solid #1e293b;
        padding: 24px;
        border-radius: 12px;
        margin-bottom: 20px;
    }
    .badge-verified {
        background-color: #064e3b;
        color: #34d399;
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 600;
    }
    .badge-pro {
        background-color: #581c87;
        color: #e9d5ff;
        padding: 2px 10px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 600;
    }
    .score-box {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        border: 1px solid #312e81;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- HEADER SECTION -----------------
st.markdown('<div class="main-header">Settings</div>', unsafe_allow_html=True)
st.markdown('<div class="main-sub">Manage your account, security preferences and application settings.</div>', unsafe_allow_html=True)

# ----------------- TABS NAVIGATION -----------------
tabs = st.tabs([
    "👤 Profile & Account", 
    "🔒 Security", 
    "⚙️ Preferences", 
    "🔔 Notifications", 
    "🔗 Integrations", 
    "📊 Data & Privacy", 
    "💳 Billing"
])

# =====================================================
# TAB 1: PROFILE & ACCOUNT
# =====================================================
with tabs[0]:
    col_main, col_side = st.columns([2.2, 1], gap="large")

    with col_main:
        with st.container(border=True):
            col_t, col_b = st.columns([3, 1])
            with col_t:
                st.subheader("Profile Information")
            with col_b:
                if st.button("Edit Profile", use_container_width=True):
                    st.info("Edit profile modal triggered.")

            c1, c2 = st.columns([1, 2.5])
            with c1:
                st.markdown("""
                <div style="background-color: #4f46e5; width: 80px; height: 80px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 28px; font-weight: bold; color: white; margin-top: 10px;">
                    AU
                </div>
                """, unsafe_allow_html=True)
            with c2:
                st.markdown("**Full Name**")
                st.text("Aryan Upadhyay")
                st.markdown("**Email Address**")
                st.markdown("aryan.upadhyay@example.com &nbsp;&nbsp; <span class='badge-verified'>Verified</span>", unsafe_allow_html=True)
                st.markdown("**Role & Member Since**")
                st.text("SOC Analyst | Joined 08 Aug 2026")

        with st.container(border=True):
            st.subheader("Account Settings")
            
            st.selectbox("Language", ["English", "Spanish", "French", "German"], index=0)
            st.selectbox("Time Zone", ["(GMT+05:30) Asia/Kolkata", "(GMT+00:00) UTC", "(GMT-05:00) Eastern Time"], index=0)
            st.selectbox("Date Format", ["DD MMM YYYY (08 Aug 2026)", "YYYY-MM-DD", "MM/DD/YYYY"], index=0)
            
            st.markdown("**Theme**")
            th_col1, th_col2, th_col3 = st.columns(3)
            with th_col1:
                st.button("🌙 Dark", use_container_width=True, type="primary")
            with th_col2:
                st.button("☀️ Light", use_container_width=True)
            with th_col3:
                st.button("💻 Auto", use_container_width=True)

        with st.container(border=True):
            st.subheader("Default Analysis Settings")
            st.selectbox("Default Risk Threshold", ["Medium (50%)", "Low (25%)", "High (75%)", "Critical (90%)"], index=0)
            st.toggle("Auto Save Reports", value=True, help="Automatically save reports after analysis completion.")

    with col_side:
        with st.container(border=True):
            c_av, c_info = st.columns([1, 2])
            with c_av:
                st.markdown("""
                <div style="background-color: #4f46e5; width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 18px; font-weight: bold; color: white;">
                    AU
                </div>
                """, unsafe_allow_html=True)
            with c_info:
                st.markdown("**Aryan Upadhyay**")
                st.caption("SOC Analyst")
            
            st.markdown("<span class='badge-pro'>Pro Plan</span>", unsafe_allow_html=True)
            st.markdown("---")
            
            st.markdown("**Security Score**")
            col_sc, col_txt = st.columns([2, 1])
            with col_sc:
                st.markdown("### 92 <span style='font-size: 14px; color: #94a3b8;'>/100</span>", unsafe_allow_html=True)
            with col_txt:
                st.markdown("<span style='color: #34d399; font-weight: 600; font-size: 14px;'>Excellent</span>", unsafe_allow_html=True)
            
            st.progress(0.92)
            st.caption("Strong security posture")

        with st.container(border=True):
            st.markdown("**Security**")
            st.markdown("🔒 **Password**<br><span style='color: #94a3b8; font-size: 12px;'>Last changed 15 Jul 2026</span>", unsafe_allow_html=True)
            if st.button("Change Password", key="btn_chg_pwd", use_container_width=True):
                st.toast("Password update prompt opened.")
            
            st.markdown("🛡️ **Two-Factor Authentication**<br><span style='color: #34d399; font-size: 12px;'>Enabled</span>", unsafe_allow_html=True)
            st.markdown("🔔 **Login Alerts**<br><span style='color: #34d399; font-size: 12px;'>Enabled for new logins</span>", unsafe_allow_html=True)

        with st.container(border=True):
            st.markdown("**Quick Actions**")
            if st.button("🔑 API Keys & Tokens", use_container_width=True):
                st.switch_page("pages/Settings.py")
            if st.button("💻 Active Sessions", use_container_width=True):
                st.toast("Active sessions manager loaded.")
            if st.button("📥 Download My Data", use_container_width=True):
                st.toast("Account data export initiated.")

        with st.container(border=True):
            col_head, col_link = st.columns([2, 1])
            with col_head:
                st.markdown("**Active Sessions**")
            with col_link:
                st.markdown("<span style='color: #60a5fa; font-size: 12px; cursor: pointer;'>View All</span>", unsafe_allow_html=True)
            
            st.markdown("""
            🖥️ **Current Session** &nbsp; <span style='background-color: #064e3b; color: #34d399; font-size: 10px; padding: 2px 6px; border-radius: 4px;'>Active</span><br>
            <span style='color: #94a3b8; font-size: 12px;'>Windows • Chrome<br>Kolkata, India • 08 Aug 2026, 12:20 PM</span>
            """, unsafe_allow_html=True)

# =====================================================
# TAB 2: SECURITY
# =====================================================
with tabs[1]:
    st.subheader("Security Settings")
    sec_col1, sec_col2 = st.columns(2, gap="large")
    
    with sec_col1:
        with st.container(border=True):
            st.markdown("#### Change Password")
            st.text_input("Current Password", type="password")
            st.text_input("New Password", type="password")
            st.text_input("Confirm New Password", type="password")
            st.button("Update Password", type="primary")
            
    with sec_col2:
        with st.container(border=True):
            st.markdown("#### Multi-Factor Authentication (MFA)")
            st.write("Add an extra layer of security to your account.")
            st.toggle("Enable Authenticator App", value=True)
            st.toggle("Enable SMS/Email Verification", value=False)
            
        with st.container(border=True):
            st.markdown("#### Session Management")
            st.slider("Auto-logout Timeout (Minutes)", min_value=5, max_value=120, value=30, step=5)
            if st.button("Log out of all other sessions"):
                st.success("Successfully logged out of all other active sessions.")

# =====================================================
# TAB 3: PREFERENCES
# =====================================================
with tabs[2]:
    st.subheader("Dashboard Preferences")
    pref_col1, pref_col2 = st.columns(2, gap="large")
    
    with pref_col1:
        with st.container(border=True):
            st.markdown("#### Workspace Layout")
            st.selectbox("Default Landing Page", ["Dashboard", "Live Monitoring", "Threat Intelligence", "Dataset Analysis", "Reports"])
            st.selectbox("Telemetry Data Refresh Rate", ["Real-time", "Every 30 seconds", "Every 1 minute", "Every 5 minutes"])
            
    with pref_col2:
        with st.container(border=True):
            st.markdown("#### Advanced UI Settings")
            st.toggle("Show Mini-Map in Live Monitoring", value=True)
            st.toggle("Enable Compact Table Rows", value=False)
            st.toggle("Enable Sound Alerts for Critical Threats", value=True)

# =====================================================
# TAB 4: NOTIFICATIONS
# =====================================================
with tabs[3]:
    st.subheader("Notification Preferences")
    notif_col1, notif_col2 = st.columns(2, gap="large")
    
    with notif_col1:
        with st.container(border=True):
            st.markdown("#### Email Notifications")
            st.toggle("Critical Security Alerts", value=True)
            st.toggle("Weekly Security Digest", value=True)
            st.toggle("New Login Attempts", value=False)
            st.toggle("System Maintenance Updates", value=True)
            
    with notif_col2:
        with st.container(border=True):
            st.markdown("#### Third-Party Alerts")
            st.text_input("Slack Webhook URL", placeholder="https://hooks.slack.com/services/...")
            st.text_input("Microsoft Teams Webhook URL", placeholder="https://outlook.office.com/webhook/...")
            st.button("Save Webhooks", type="primary")

# =====================================================
# TAB 5: INTEGRATIONS
# =====================================================
with tabs[4]:
    st.subheader("Integrations")
    st.write("Connect external services to enhance CipherVista's telemetry and detection capabilities.")
    
    int_col1, int_col2, int_col3 = st.columns(3)
    
    with int_col1:
        with st.container(border=True):
            st.markdown("### 🧩 Splunk")
            st.write("Forward logs directly to Splunk Enterprise.")
            st.toggle("Enable Splunk Forwarder", value=False, key="splunk")
            
    with int_col2:
        with st.container(border=True):
            st.markdown("### ☁️ AWS CloudTrail")
            st.write("Ingest and analyze AWS environment logs.")
            st.toggle("Enable AWS Sync", value=True, key="aws")
            
    with int_col3:
        with st.container(border=True):
            st.markdown("### 🦠 VirusTotal")
            st.write("Automated IoC enrichment via API.")
            st.toggle("Enable VT API", value=True, key="vt")
            st.text_input("API Key", type="password", value="hidden_key_12345")

# =====================================================
# TAB 6: DATA & PRIVACY
# =====================================================
with tabs[5]:
    st.subheader("Data & Privacy")
    dp_col1, dp_col2 = st.columns(2, gap="large")
    
    with dp_col1:
        with st.container(border=True):
            st.markdown("#### Data Retention Policies")
            st.selectbox("Keep audit logs for:", ["30 Days", "90 Days", "1 Year", "Indefinitely"], index=1)
            st.selectbox("Keep threat intel data for:", ["30 Days", "90 Days", "1 Year", "Indefinitely"], index=2)
            st.button("Save Retention Policies", type="primary")
            
    with dp_col2:
        with st.container(border=True):
            st.markdown("#### Compliance & Export")
            st.write("Download a complete archive of your account data, logs, and configurations.")
            st.button("Request Data Export")
            
        with st.container(border=True):
            st.markdown("<span style='color: #ef4444; font-weight: bold;'>Danger Zone</span>", unsafe_allow_html=True)
            st.write("Permanently delete your account and wipe all associated telemetry data.")
            if st.button("Delete Account"):
                st.error("Action requires admin confirmation.")

# =====================================================
# TAB 7: BILLING
# =====================================================
with tabs[6]:
    st.subheader("Billing & Subscriptions")
    with st.container(border=True):
        st.markdown("### Enterprise Pro Plan")
        st.write("Your next billing date is **01 Sept 2026**.")
        st.progress(0.45)
        st.caption("API Quota Usage: 45,000 / 100,000 requests")
        st.button("Manage Subscription", type="primary")
render_footer()