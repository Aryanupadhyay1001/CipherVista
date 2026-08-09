import warnings
import base64
from pathlib import Path
import requests
import streamlit as st
from styles import load_css
from components.footer import render_footer
from components.page_header import render_page_header
from components import (
    render_sidebar,
    render_hero,
    render_kpi_cards,
    render_summary,
    render_investigation,
    render_ai_report,
    render_model_info,
    render_charts
)
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
FAVICON_PATH = ROOT / "assets" / "favicon.ico"

import warnings

warnings.filterwarnings(
    "ignore",
    message="X has feature names.*"
)

warnings.filterwarnings(
    "ignore",
    message="X does not have valid feature names.*"
)



# ----------------- PAGE CONFIG -----------------
st.set_page_config(
    page_title="CipherVista | Dataset Analysis",
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

st.markdown(load_css(), unsafe_allow_html=True)

# ----------------- ASSETS & CONFIG -----------------
ROOT = Path(__file__).resolve().parent.parent.parent
ASSETS = ROOT / "assets"
API_URL = "http://127.0.0.1:8000"

def get_image_base64(image_path):
    if image_path.exists():
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""

logo_base64 = get_image_base64(ASSETS / "favicon.ico")
logo_html_tag = f'<img src="data:image/x-icon;base64,{logo_base64}" style="width: 48px; height: 48px; object-fit: contain; border-radius: 12px;" />' if logo_base64 else '<span style="font-size: 42px;">🛡️</span>'

# ----------------- SESSION & QUERY PARAM SYNC -----------------
if "token" in st.query_params and not st.session_state.get("access_token"):
    st.session_state["access_token"] = st.query_params["token"]

if "access_token" not in st.session_state:
    st.session_state["access_token"] = None

if "analysis" not in st.session_state:
    st.session_state.analysis = None

# ----------------- SESSION STATE CHECK -----------------
if st.session_state["access_token"] is None:
    st.warning("Authentication required. Please log in first.")
    st.switch_page("app.py")

# Render global custom sidebar and set the active tab state
render_sidebar(active_page="dataset_analysis")
render_page_header(
    "AI Threat Analysis Workbench",
    "Multi-layered network traffic investigation powered by machine learning and Gemini AI"
)

# Sidebar Controls
with st.sidebar:
    st.markdown("### 🛡️ SOC Telemetry Nodes")
    if st.button("🚪 Terminate Session", use_container_width=True):
        st.session_state["access_token"] = None
        st.session_state.analysis = None
        st.query_params.clear()
        st.rerun()

# =====================================================
# DATASET UPLOAD & INGESTION WORKBENCH
# =====================================================
if st.session_state.analysis is None:

    hero_html = f'<div style="background: linear-gradient(135deg, #0F172A 0%, #1E1B4B 50%, #0F172A 100%); border: 1px solid #3B82F6; border-radius: 24px; padding: 36px 30px; text-align: center; margin-bottom: 28px; box-shadow: 0 0 35px rgba(37, 99, 235, 0.25);"><div style="display: flex; justify-content: center; align-items: center; gap: 14px; margin-bottom: 12px;">{logo_html_tag}<span style="font-size: 44px; font-weight: 900; color: white; letter-spacing: -1px; text-shadow: 0 2px 12px rgba(0,0,0,0.6);">CipherVista</span><span style="background: #2563EB; color: white; padding: 4px 12px; border-radius: 999px; font-size: 13px; font-weight: 800; border: 1px solid #60A5FA;">v3.0</span></div><div style="font-size: 21px; font-weight: 800; background: linear-gradient(90deg, #60A5FA, #A78BFA, #38BDF8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 14px; text-transform: uppercase; letter-spacing: 1px;">⚡ AI-Powered Threat Intelligence Platform</div><p style="color: #94A3B8; font-size: 15px; max-width: 750px; margin: 0 auto 24px auto; line-height: 1.6; font-weight: 500;">Enterprise Network Threat Detection, Automated SOC Investigation, and Machine Learning Analytics driven by <strong style="color: white;">Random Forest</strong>, <strong style="color: white;">Isolation Forest</strong>, and <strong style="color: white;">Google Gemini AI</strong>.</p></div>'
    st.markdown(hero_html, unsafe_allow_html=True)

    left_col, right_col = st.columns([1.2, 1], gap="large")

    with left_col:
        upload_header = '<div style="background: #0F172A; border: 1px solid #1E293B; border-radius: 18px; padding: 28px; box-shadow: 0 10px 25px rgba(0,0,0,0.3);"><div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;"><span style="font-size: 26px;">📂</span><span style="font-size: 22px; font-weight: 700; color: white;">Upload Dataset</span></div><p style="color: #94A3B8; font-size: 15px; margin: 0 0 20px 0; line-height: 1.5;">Upload your network traffic CSV dataset for multi-layered AI-powered threat analysis.</p><div style="display: flex; gap: 12px; margin-bottom: 20px;"><span style="background: #1E293B; color: #E2E8F0; padding: 6px 12px; border-radius: 8px; font-size: 13px; font-weight: 600; border: 1px solid #334155;">📄 Format: CSV</span><span style="background: #1E293B; color: #E2E8F0; padding: 6px 12px; border-radius: 8px; font-size: 13px; font-weight: 600; border: 1px solid #334155;">📦 Max Size: 200 MB</span></div>'
        st.markdown(upload_header, unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "📂 Choose Dataset",
            type=["csv"],
            label_visibility="collapsed"
        )

        if uploaded_file is not None:
            size = uploaded_file.size / (1024 * 1024)
            st.success("✅ Dataset Ready")

            c1, c2 = st.columns(2)
            with c1:
                st.metric("Filename", uploaded_file.name)
            with c2:
                st.metric("Size", f"{size:.2f} MB")

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        analyze = st.button(
            "🚀 Start AI Threat Analysis",
            use_container_width=True,
            type="primary"
        )
        
        st.markdown("</div>", unsafe_allow_html=True)

    with right_col:
        pipeline_html = '<div style="background: #0F172A; border: 1px solid #1E293B; border-radius: 18px; padding: 28px; height: 100%; box-shadow: 0 10px 25px rgba(0,0,0,0.3);"><div style="display: flex; align-items: center; gap: 12px; margin-bottom: 24px;"><span style="font-size: 26px;">🤖</span><span style="font-size: 22px; font-weight: 700; color: white;">Analysis Pipeline</span></div><div style="display: flex; flex-direction: column; gap: 20px;"><div style="display: flex; align-items: center; gap: 16px;"><div style="background: rgba(37, 99, 235, 0.2); color: #60A5FA; width: 36px; height: 36px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 15px; font-weight: 800; border: 1px solid #2563EB;">1</div><div style="color: #E2E8F0; font-size: 15px; font-weight: 600;">Random Forest Classification</div></div><div style="width: 2px; height: 12px; background: #334155; margin: -16px 0 -16px 17px;"></div><div style="display: flex; align-items: center; gap: 16px;"><div style="background: rgba(139, 92, 246, 0.2); color: #A78BFA; width: 36px; height: 36px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 15px; font-weight: 800; border: 1px solid #8B5CF6;">2</div><div style="color: #E2E8F0; font-size: 15px; font-weight: 600;">Isolation Forest Detection</div></div><div style="width: 2px; height: 12px; background: #334155; margin: -16px 0 -16px 17px;"></div><div style="display: flex; align-items: center; gap: 16px;"><div style="background: rgba(16, 185, 129, 0.2); color: #34D399; width: 36px; height: 36px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 15px; font-weight: 800; border: 1px solid #10B981;">3</div><div style="color: #E2E8F0; font-size: 15px; font-weight: 600;">Gemini AI Investigation</div></div><div style="width: 2px; height: 12px; background: #334155; margin: -16px 0 -16px 17px;"></div><div style="display: flex; align-items: center; gap: 16px;"><div style="background: rgba(245, 158, 11, 0.2); color: #FBBF24; width: 36px; height: 36px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 15px; font-weight: 800; border: 1px solid #F59E0B;">4</div><div style="color: #E2E8F0; font-size: 15px; font-weight: 600;">Executive PDF Generation</div></div></div></div>'
        st.markdown(pipeline_html, unsafe_allow_html=True)

    if uploaded_file is not None and analyze:
        with st.spinner("Running AI Threat Analysis..."):
            try:
                headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}
                response = requests.post(
                    f"{API_URL}/predict-file",
                    headers=headers,
                    files={
                        "file": (
                            uploaded_file.name,
                            uploaded_file,
                            "text/csv"
                        )
                    },
                    timeout=300
                )
            except requests.RequestException as e:
                st.error(f"API Error: {e}")
                st.stop()

        if response.status_code == 200:
            st.session_state.analysis = response.json()
            st.rerun()
        else:
            st.error(response.text)
            st.stop()

# =====================================================
# RESULTS DASHBOARD VIEW
# =====================================================
else:
    data = st.session_state.analysis

    col1, col2 = st.columns([5,1])

    with col1:
        st.success("✅ Analysis Completed Successfully")

    with col2:
        if st.button(
            "🔄 New Analysis",
            key="new_analysis",
            use_container_width=True
        ):
            st.session_state.analysis = None
            st.rerun()

    pdf_path = data.get("pdf_path", "")
    summary = data.get("summary", {})
    stats = data.get("statistics", {})
    risk = data.get("risk", {})

    attack_breakdown = data.get("attack_breakdown", {})
    ai_report = data.get("ai_report", "")

    total = summary.get("total_records", 0)
    attacks = summary.get("attacks", 0)
    confidence = stats.get("average_confidence", 0)
    risk_level = risk.get("level", "Unknown")

    tab_dashboard, tab_report = st.tabs(
        [
            "📊 Dashboard",
            "🤖 AI Security Report"
        ]
    )

    with tab_dashboard:
        render_kpi_cards(total, attacks, confidence, risk_level)
        render_charts(attack_breakdown)
        render_model_info()
        st.divider()
        render_summary(stats, confidence, total, attack_breakdown)
        render_investigation(data, confidence, pdf_path)

    with tab_report:
        render_ai_report(ai_report)
render_footer()