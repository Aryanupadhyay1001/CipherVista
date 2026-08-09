import os
import warnings
from pathlib import Path
import requests
import streamlit as st
from styles import load_css

warnings.filterwarnings("ignore", message="X has feature names*")

# ----------------- ASSETS & CONFIG -----------------
ROOT = Path(__file__).resolve().parent.parent
FAVICON_PATH = ROOT / "assets" / "favicon.ico"
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="CipherVista | SOC Command Center",
    page_icon=str(FAVICON_PATH) if FAVICON_PATH.exists() else "🛡",
    layout="wide"
)

st.markdown(load_css(), unsafe_allow_html=True)

# ----------------- SESSION & TOKEN SYNC -----------------
query_token = st.query_params.get("token")
if query_token:
    if isinstance(query_token, list):
        query_token = query_token[0]
    st.session_state["access_token"] = query_token

if "access_token" not in st.session_state:
    st.session_state["access_token"] = None

if "analysis" not in st.session_state:
    st.session_state.analysis = None

# ----------------- AUTHENTICATION GATE -----------------
if st.session_state["access_token"] is None:
    col1, col2, col3 = st.columns([1, 1.3, 1])
    with col2:
        st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
        st.title("🔐 Welcome to CipherVista")
        st.markdown("Please log in or create an account to access the AI Threat Intelligence Platform.")
        
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            st.subheader("Login")
            login_email = st.text_input("Email", key="login_email")
            login_password = st.text_input("Password", type="password", key="login_password")
            
            if st.button("Login", type="primary", use_container_width=True):
                if login_email and login_password:
                    try:
                        response = requests.post(
                            f"{API_URL}/auth/login", 
                            json={"email": login_email, "password": login_password}
                        )
                        if response.status_code == 200:
                            token_data = response.json()
                            token = token_data["access_token"]
                            
                            st.session_state["access_token"] = token
                            st.query_params["token"] = token
                            
                            st.success("Login successful! Loading Command Center...")
                            st.rerun()
                        else:
                            st.error("Invalid email or password.")
                    except requests.RequestException:
                        st.error("Cannot connect to backend. Make sure FastAPI is running!")
                else:
                    st.warning("Please enter both email and password.")

        with tab2:
            st.subheader("Create an Account")
            reg_name = st.text_input("Full Name", key="reg_name")
            reg_email = st.text_input("Email", key="reg_email")
            reg_password = st.text_input("Password", type="password", key="reg_password")
            reg_confirm = st.text_input("Confirm Password", type="password", key="reg_confirm")
            
            if st.button("Sign Up", type="primary", use_container_width=True):
                if reg_password != reg_confirm:
                    st.error("Passwords do not match!")
                elif reg_name and reg_email and reg_password:
                    try:
                        response = requests.post(
                            f"{API_URL}/auth/register", 
                            json={"name": reg_name, "email": reg_email, "password": reg_password}
                        )
                        if response.status_code == 200:
                            st.success("Account created successfully! You can now log in.")
                        else:
                            st.error(f"Error: {response.json().get('detail', 'Could not create account')}")
                    except requests.RequestException:
                        st.error("Cannot connect to backend. Make sure FastAPI is running!")
                else:
                    st.warning("Please fill out all fields.")
    
    # Halt script execution here so dashboard code below never runs while logged out
    st.stop()

# ----------------- MODERN NAVIGATION (PROTECTED AREA) -----------------
# Only runs when st.session_state["access_token"] is valid
dashboard_page = st.Page("pages/Dashboard.py", title="Dashboard", icon="📊")
live_monitor_page = st.Page("pages/live_monitoring.py", title="Live Monitor", icon="⚡")
threat_intel_page = st.Page("pages/threat_intelligence.py", title="Threat Intelligence", icon="🌐")
dataset_analysis_page = st.Page("pages/dataset_analysis.py", title="Dataset Analysis", icon="📁")
reports_page = st.Page("pages/reports.py", title="Reports", icon="📋")
settings_page = st.Page("pages/settings.py", title="Settings", icon="⚙️")

pg = st.navigation([
    dashboard_page,
    live_monitor_page,
    threat_intel_page,
    dataset_analysis_page,
    reports_page,
    settings_page
])

pg.run()