import base64
from pathlib import Path
import textwrap
import streamlit as st
# components/__init__.py

from .ai_report import render_ai_report
from .charts import render_charts
from .footer import render_footer
from .hero import render_hero
from .investigation import render_investigation
from .kpi_cards import render_kpi_cards
from .model_info import render_model_info
from .summary import render_summary



# ----------------- BASE64 ENCODER -----------------
def get_image_base64(file_path: Path) -> str:
    """Reads local image file and converts to Base64 string."""
    if file_path.exists():
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""


# ----------------- SIDEBAR COMPONENT -----------------
def render_sidebar(active_page: str = "Dashboard"):
    st.markdown("""
        <style>
            [data-testid="stSidebarNav"] {
                display: none !important;
            }

            [data-testid="stSidebar"] {
                background: #020617;
            }

            [data-testid="stPageLink"] a {
                background: transparent !important;
                border: none !important;
                border-radius: 10px !important;
                padding: 10px 12px !important;
                color: #94a3b8 !important;
                text-decoration: none !important;
                transition: all 0.2s ease !important;
            }

            [data-testid="stPageLink"] a:hover {
                background: rgba(59,130,246,0.12) !important;
                color: #ffffff !important;
            }

            [data-testid="stPageLink"] {
                margin-bottom: 3px;
            }
        </style>
    """, unsafe_allow_html=True)

    DASHBOARD_DIR = Path(__file__).resolve().parent.parent
    FAVICON_PATH = DASHBOARD_DIR / "assets" / "favicon.ico"

    if not FAVICON_PATH.exists():
        FAVICON_PATH = DASHBOARD_DIR.parent / "assets" / "favicon.ico"

    logo_b64 = get_image_base64(FAVICON_PATH)

    if logo_b64:
        logo_html = f'<img src="data:image/x-icon;base64,{logo_b64}" width="26" height="26" style="object-fit:contain;border-radius:4px;">'
    else:
        logo_html = '<span style="font-size:22px;">🛡️</span>'

    user_display_name = st.session_state.get("user_name", "Aryan Upadhyay")

    st.sidebar.markdown(f"""
        <div class="cv-brand-header">
            <div class="cv-brand-left">
                <div class="cv-brand-logo">{logo_html}</div>
                <div class="cv-brand-text">
                    <span class="cv-brand-title">CipherVista</span>
                    <span class="cv-brand-subtitle">Enterprise</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown(
        '<div class="cv-section-title-nav"><div class="cv-section-dot"></div> NAVIGATION</div>',
        unsafe_allow_html=True
    )

    st.sidebar.page_link(
        "pages/Dashboard.py",
        label="Dashboard"
    )

    st.sidebar.markdown(
        '<div class="cv-section-title-nav"><div class="cv-section-dot"></div> MONITORING</div>',
        unsafe_allow_html=True
    )

    st.sidebar.page_link(
        "pages/live_monitoring.py",
        label="Live Monitor"
    )

    st.sidebar.page_link(
        "pages/threat_intelligence.py",
        label="Threat Intelligence"
    )

    st.sidebar.page_link(
        "pages/dataset_analysis.py",
        label="Dataset Analysis"
    )

    st.sidebar.markdown(
        '<div class="cv-section-title-nav"><div class="cv-section-dot"></div> ANALYSIS</div>',
        unsafe_allow_html=True
    )

    st.sidebar.page_link(
        "pages/reports.py",
        label="Reports",
    )

    st.sidebar.markdown(
        '<div class="cv-section-title-nav"><div class="cv-section-dot"></div> MANAGEMENT</div>',
        unsafe_allow_html=True
    )

    st.sidebar.page_link(
        "pages/settings.py",
        label="Settings"
    )

    st.sidebar.markdown(f"""
        <div class="cv-profile-card">
            <div class="cv-profile-left">
                <div class="cv-avatar">
                    AU
                    <div class="cv-status-dot"></div>
                </div>
                <div class="cv-profile-info">
                    <span class="cv-profile-name">{user_display_name}</span>
                    <span class="cv-profile-role">SOC Analyst</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

try:
    from .hero import hero
except (ImportError, AttributeError):
    hero = None

try:
    from .charts import render_charts
except (ImportError, AttributeError):
    render_charts = None

attack_pie_chart = None
traffic_bar_chart = None