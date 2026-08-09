import os
from datetime import datetime
import requests
import streamlit as st
from components import render_sidebar
from components.footer import render_footer
from components.page_header import render_page_header
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
FAVICON_PATH = ROOT / "assets" / "favicon.ico"

st.set_page_config(
    page_title="CipherVista | Reports",
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

render_sidebar(active_page="reports")

render_page_header(
    "Security Intelligence Reports",
    "Historical investigations, executive briefings and security analytics"
)

with st.sidebar:
    st.markdown("### 🛡️ SOC Telemetry Nodes")
    if st.button("🚪 Terminate Session", use_container_width=True):
        st.session_state["access_token"] = None
        st.query_params.clear()
        st.rerun()

# Configure page theme styling
st.markdown("""
<style>
    /* Existing Badges */
    .badge-critical { background-color: #7f1d1d; color: #fca5a5; padding: 4px 10px; border-radius: 6px; font-weight: 600; font-size: 12px; }
    .badge-high { background-color: #7c2d12; color: #fdba74; padding: 4px 10px; border-radius: 6px; font-weight: 600; font-size: 12px; }
    .badge-medium { background-color: #713f12; color: #fde047; padding: 4px 10px; border-radius: 6px; font-weight: 600; font-size: 12px; }
    .badge-low { background-color: #14532d; color: #86efac; padding: 4px 10px; border-radius: 6px; font-weight: 600; font-size: 12px; }

    /* Custom Metric Cards matching image_d8147f.jpg */
    .cyber-card {
        background-color: #111827; /* Dark background matching the dashboard */
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid #1f2937;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Left accent borders */
    .border-blue { border-left: 4px solid #3b82f6; }
    .border-red { border-left: 4px solid #ef4444; }
    .border-teal { border-left: 4px solid #14b8a6; }
    .border-green { border-left: 4px solid #22c55e; }

    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }
    
    .card-title {
        color: #f8fafc;
        font-size: 15px;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* LIVE pill badges */
    .live-badge {
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    .badge-blue { background-color: #1e3a8a; color: #93c5fd; }
    .badge-red { background-color: #7f1d1d; color: #fca5a5; }
    .badge-teal { background-color: #134e4a; color: #5eead4; }
    .badge-green { background-color: #14532d; color: #86efac; }

    .card-value {
        font-size: 32px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 2px;
        line-height: 1.2;
    }
    
    .card-subtitle {
        color: #94a3b8;
        font-size: 13px;
        margin-bottom: 16px;
    }
    
    .card-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 11px;
        color: #64748b;
        border-top: 1px solid #1e293b;
        padding-top: 12px;
    }
    
    .status-indicator {
        display: flex;
        align-items: center;
        gap: 6px;
        font-weight: 500;
    }
    .status-blue { color: #3b82f6; }
    .status-red { color: #ef4444; }
    .status-teal { color: #14b8a6; }
    .status-green { color: #22c55e; }
    
    .dot {
        height: 6px;
        width: 6px;
        border-radius: 50%;
        display: inline-block;
    }
    .dot-blue { background-color: #3b82f6; }
    .dot-red { background-color: #ef4444; }
    .dot-teal { background-color: #14b8a6; }
    .dot-green { background-color: #22c55e; }
</style>
""", unsafe_allow_html=True)

def render_reports_page(api_url: str, token: str):
    headers = {"Authorization": f"Bearer {token}"}

    # Top Header section
    col_title, col_btn = st.columns([4, 1])
    with col_title:
        st.markdown("## Reports")
        st.caption("View, manage and analyze your past security assessments")
    
    with col_btn:
        st.write("") # alignment spacing
        if st.button("+ New Analysis", type="primary", use_container_width=True):
            st.session_state.current_page = "Upload & Analyze"
            st.rerun()

    # Fetch reports from FastAPI backend
    try:
        response = requests.get(f"{api_url}/reports", headers=headers)
        if response.status_code == 200:
            reports_data = response.json().get("reports", [])
        else:
            reports_data = []
            st.warning(f"Could not load reports (Server responded with status {response.status_code})")
    except Exception as e:
        st.error(f"Failed to connect to backend server: {e}")
        reports_data = []

    # Calculate summary metrics safely
    total_reports = len(reports_data)
    total_threats = sum([r.get("attacks", 0) for r in reports_data])
    critical_count = sum([1 for r in reports_data if r.get("risk_level") == "Critical"])
    avg_conf = round(sum([r.get("confidence", 0) for r in reports_data]) / total_reports, 1) if total_reports > 0 else 0.0

    # 1. Styled Top Summary Metric Cards Layout
    m1, m2, m3, m4 = st.columns(4)
    
    with m1:
        st.markdown(f"""
        <div class="cyber-card border-blue">
            <div class="card-header">
                <div class="card-title">🌐 Total Reports</div>
                <div class="live-badge badge-blue">LIVE</div>
            </div>
            <div class="card-value">{total_reports:,}</div>
            <div class="card-subtitle">Generated Assessments</div>
            <div class="card-footer">
                <div>Updated just now</div>
                <div class="status-indicator status-blue"><span class="dot dot-blue"></span> Operational</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with m2:
        st.markdown(f"""
        <div class="cyber-card border-red">
            <div class="card-header">
                <div class="card-title">🚨 Total Threats</div>
                <div class="live-badge badge-red">LIVE</div>
            </div>
            <div class="card-value">{total_threats:,}</div>
            <div class="card-subtitle">Historical Detections</div>
            <div class="card-footer">
                <div>Updated just now</div>
                <div class="status-indicator status-red"><span class="dot dot-red"></span> Operational</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with m3:
        st.markdown(f"""
        <div class="cyber-card border-teal">
            <div class="card-header">
                <div class="card-title">🛡️ Avg. Confidence</div>
                <div class="live-badge badge-teal">LIVE</div>
            </div>
            <div class="card-value">{avg_conf}%</div>
            <div class="card-subtitle">Model Accuracy</div>
            <div class="card-footer">
                <div>Updated just now</div>
                <div class="status-indicator status-teal"><span class="dot dot-teal"></span> Operational</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with m4:
        # Change risk card color based on critical count
        border_color = "border-red" if critical_count > 0 else "border-green"
        badge_color = "badge-red" if critical_count > 0 else "badge-green"
        status_color = "status-red" if critical_count > 0 else "status-green"
        dot_color = "dot-red" if critical_count > 0 else "dot-green"
        
        st.markdown(f"""
        <div class="cyber-card {border_color}">
            <div class="card-header">
                <div class="card-title">⚠️ Critical Reports</div>
                <div class="live-badge {badge_color}">LIVE</div>
            </div>
            <div class="card-value">{critical_count:,}</div>
            <div class="card-subtitle">High Priority Action Required</div>
            <div class="card-footer">
                <div>Updated just now</div>
                <div class="status-indicator {status_color}"><span class="dot {dot_color}"></span> Operational</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # 2. Search & Filter Bar
    f_col1, f_col2, f_col3 = st.columns([3, 1, 1])
    with f_col1:
        search_query = st.text_input("Search", placeholder="Search reports by name, dataset...", label_visibility="collapsed")
    with f_col2:
        risk_filter = st.selectbox("Risk Level", ["All Risk Levels", "Critical", "High", "Medium", "Low"], label_visibility="collapsed")
    with f_col3:
        time_filter = st.selectbox("Time Range", ["All Time", "Last 7 Days", "This Month"], label_visibility="collapsed")

    # Filter logic
    filtered_reports = reports_data
    if search_query:
        filtered_reports = [r for r in filtered_reports if search_query.lower() in r.get("report_name", "").lower() or search_query.lower() in r.get("dataset_name", "").lower()]
    if risk_filter != "All Risk Levels":
        filtered_reports = [r for r in filtered_reports if r.get("risk_level") == risk_filter]

    st.markdown("###")

    # 3. Reports Table Headers
    header_cols = st.columns([2.5, 2, 1, 1.2, 1.2, 1.5, 1.2])
    header_titles = ["REPORT DETAILS", "DATASET", "RISK LEVEL", "THREATS", "CONFIDENCE", "CREATED AT", "ACTIONS"]
    for col, h in zip(header_cols, header_titles):
        col.markdown(f"**<span style='color: #94a3b8; font-size: 12px;'>{h}</span>**", unsafe_allow_html=True)

    st.markdown("<hr style='margin: 5px 0px 15px 0px; border-color: #1e293b;'>", unsafe_allow_html=True)

    # 4. Render Report Rows
    if not filtered_reports:
        st.info("No security assessment reports found matching your criteria. Run an analysis first!")
    else:
        for r in filtered_reports:
            r_id = r["report_id"]
            risk = r.get("risk_level", "Low")
            badge_class = f"badge-{risk.lower()}"
            
            row_cols = st.columns([2.5, 2, 1, 1.2, 1.2, 1.5, 1.2])
            
            with row_cols[0]:
                st.markdown(f"🛡️ **{r.get('report_name')}**<br><span style='color: #64748b; font-size: 11px;'>Internal Security Assessment v1.0</span>", unsafe_allow_html=True)
            with row_cols[1]:
                st.markdown(f"📁 {r.get('dataset_name')}<br><span style='color: #64748b; font-size: 11px;'>{r.get('dataset_rows', 0):,} rows</span>", unsafe_allow_html=True)
            with row_cols[2]:
                st.markdown(f"<span class='{badge_class}'>{risk}</span>", unsafe_allow_html=True)
            with row_cols[3]:
                attack_rate = r.get('attack_rate', 0.0)
                st.markdown(f"**{r.get('attacks', 0):,}**<br><span style='color: #ef4444; font-size: 11px;'>{attack_rate}%</span>", unsafe_allow_html=True)
            with row_cols[4]:
                conf = r.get('confidence', 0.0)
                st.markdown(f"**{conf}%**", unsafe_allow_html=True)
            with row_cols[5]:
                created_raw = r.get('created_at')
                if created_raw:
                    try:
                        dt_obj = datetime.fromisoformat(created_raw)
                        formatted_date = dt_obj.strftime("%d %b %Y<br>%I:%M %p")
                    except Exception:
                        formatted_date = created_raw
                else:
                    formatted_date = "N/A"
                st.markdown(f"<span style='font-size: 12px;'>{formatted_date}</span>", unsafe_allow_html=True)
            
            with row_cols[6]:
                b_col1, b_col2, b_col3 = st.columns(3)
                with b_col1:
                    if st.button("👁️", key=f"view_{r_id}", help="View Report Details"):
                        st.session_state.selected_report_id = r_id
                        st.session_state.current_page = "Report Detail View"
                        st.rerun()
                with b_col2:
                    pdf_path = r.get("pdf_path")
                    if pdf_path and os.path.exists(pdf_path):
                        try:
                            with open(pdf_path, "rb") as pdf_file:
                                pdf_bytes = pdf_file.read()
                            st.download_button("📥", data=pdf_bytes, file_name=f"report_{r_id}.pdf", key=f"dl_{r_id}", mime="application/pdf", help="Download PDF")
                        except Exception:
                            st.button("📥", disabled=True, key=f"dl_err_{r_id}", help="Error reading file")
                    else:
                        st.button("📥", disabled=True, key=f"dl_none_{r_id}", help="PDF file not found on server")
                with b_col3:
                    if st.button("🗑️", key=f"del_{r_id}", help="Delete Report"):
                        del_res = requests.delete(f"{api_url}/reports/{r_id}", headers=headers)
                        if del_res.status_code == 200:
                            st.success(f"Deleted #{r_id}")
                            st.rerun()
                        else:
                            st.error("Failed to delete report")

            st.markdown("<hr style='margin: 8px 0px; border-color: #1e293b; opacity: 0.4;'>", unsafe_allow_html=True)

# ----------------- EXECUTION GUARD -----------------
if __name__ == "__main__":
    API_URL = "http://127.0.0.1:8000"
    if not st.session_state.get("access_token"):
        st.warning("Please log in from the main portal first.")
        if st.button("Go to Login"):
            st.switch_page("app.py")
    else:
        render_reports_page(API_URL, st.session_state["access_token"])

render_footer()