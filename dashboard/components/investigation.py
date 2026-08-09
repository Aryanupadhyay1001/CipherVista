import os
import pandas as pd
import streamlit as st


def render_investigation(data, confidence, pdf_path):

    threats = pd.DataFrame(data["threats"])

    critical_count = len(
        threats[threats["Severity"] == "Critical"]
    )

    high_count = len(
        threats[threats["Severity"] == "High"]
    )

    safe_count = len(
        threats[threats["Severity"] == "Safe"]
    )

    # =====================================================
    # 1. Threat Statistics Cards
    # =====================================================

    stats_html = f"""<div class="cv-card">
<div class="cv-card-header">
<div>
<div class="cv-card-title">📊 Threat Statistics</div>
<div class="cv-card-subtitle">Severity breakdown and confidence metrics of analyzed network flows</div>
</div>
<div class="cv-badge">LIVE</div>
</div>
<div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 18px;">
<div style="background:linear-gradient(180deg,#111827,#0F172A); border:1px solid rgba(255,255,255,.06); border-left:5px solid #DC2626; border-radius:18px; padding:22px; min-height:155px; box-shadow:0 10px 25px rgba(0,0,0,.35);">
<div style="color:#94A3B8; font-size:15px; font-weight:600;">🚨 Critical</div>
<div style="margin-top:18px; color:white; font-size:28px; font-weight:700; line-height:1.3;">{critical_count:,}</div>
</div>
<div style="background:linear-gradient(180deg,#111827,#0F172A); border:1px solid rgba(255,255,255,.06); border-left:5px solid #EA580C; border-radius:18px; padding:22px; min-height:155px; box-shadow:0 10px 25px rgba(0,0,0,.35);">
<div style="color:#94A3B8; font-size:15px; font-weight:600;">⚠️ High</div>
<div style="margin-top:18px; color:white; font-size:28px; font-weight:700; line-height:1.3;">{high_count:,}</div>
</div>
<div style="background:linear-gradient(180deg,#111827,#0F172A); border:1px solid rgba(255,255,255,.06); border-left:5px solid #10B981; border-radius:18px; padding:22px; min-height:155px; box-shadow:0 10px 25px rgba(0,0,0,.35);">
<div style="color:#94A3B8; font-size:15px; font-weight:600;">🟢 Safe</div>
<div style="margin-top:18px; color:white; font-size:28px; font-weight:700; line-height:1.3;">{safe_count:,}</div>
</div>
<div style="background:linear-gradient(180deg,#111827,#0F172A); border:1px solid rgba(255,255,255,.06); border-left:5px solid #8B5CF6; border-radius:18px; padding:22px; min-height:155px; box-shadow:0 10px 25px rgba(0,0,0,.35);">
<div style="color:#94A3B8; font-size:15px; font-weight:600;">🎯 Avg Confidence</div>
<div style="margin-top:18px; color:white; font-size:28px; font-weight:700; line-height:1.3;">{confidence:.2f}%</div>
</div>
</div>
</div>"""

    st.markdown(stats_html, unsafe_allow_html=True)

    # =====================================================
    # 2. Threat Investigation Header & Filters
    # =====================================================

    inv_header = """<div class="cv-card-header" style="margin-top:10px;">
<div>
<div class="cv-card-title">🔍 Threat Investigation</div>
<div class="cv-card-subtitle">Search, filter, and inspect detected network threat anomalies</div>
</div>
<div class="cv-badge">INTERACTIVE</div>
</div>"""

    st.markdown(inv_header, unsafe_allow_html=True)

    search = st.text_input(
        "🔎 Search Threats",
        placeholder="Search attack name or severity..."
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        prediction_filter = st.selectbox(
            "Prediction",
            ["All"] + sorted(threats["prediction"].unique().tolist())
        )

    with c2:
        severity_filter = st.selectbox(
            "Severity",
            ["All", "Critical", "High", "Safe"]
        )

    with c3:
        confidence_filter = st.slider(
            "Minimum Confidence",
            0,
            100,
            90
        )

    with c4:
        sort_by = st.selectbox(
            "Sort By",
            ["Confidence", "Severity", "Anomaly Score"]
        )

    # Apply Filters
    filtered = threats.copy()

    if prediction_filter != "All":
        filtered = filtered[filtered["prediction"] == prediction_filter]

    if severity_filter != "All":
        filtered = filtered[filtered["Severity"] == severity_filter]

    if search:
        filtered = filtered[
            filtered["prediction"].str.contains(search, case=False, na=False)
            | filtered["Severity"].str.contains(search, case=False, na=False)
        ]

    filtered = filtered[filtered["confidence"] >= confidence_filter]

    # Apply Sorting
    if sort_by == "Confidence":
        filtered = filtered.sort_values("confidence", ascending=False)

    elif sort_by == "Severity":
        order = {"Critical": 3, "High": 2, "Safe": 1}
        filtered["SeverityOrder"] = filtered["Severity"].map(order)
        filtered = filtered.sort_values("SeverityOrder", ascending=False)
        filtered = filtered.drop(columns=["SeverityOrder"])

    elif sort_by == "Anomaly Score":
        filtered = filtered.sort_values("anomaly_score", ascending=False)

    # Custom styling for table severity pills
    def style_severity(val):
        if val == "Critical":
            return "background-color: #7F1D1D; color: #F87171; font-weight: bold; text-align: center; border-radius: 6px;"
        elif val == "High":
            return "background-color: #78350F; color: #FBBF24; font-weight: bold; text-align: center; border-radius: 6px;"
        elif val == "Safe":
            return "background-color: #14532D; color: #4ADE80; font-weight: bold; text-align: center; border-radius: 6px;"
        return ""

    styled_df = filtered.style.map(style_severity, subset=["Severity"])

    # Render Styled Interactive Dataframe
    st.dataframe(
        styled_df,
        use_container_width=True,
        hide_index=True,
        height=450,
        column_config={
            "prediction": st.column_config.TextColumn("Attack Prediction"),
            "Severity": st.column_config.TextColumn("Severity"),
            "confidence": st.column_config.ProgressColumn(
                "Confidence Score",
                format="%.2f%%",
                min_value=0,
                max_value=100
            ),
            "anomaly_score": st.column_config.NumberColumn("Anomaly Score", format="%.4f"),
            "anomaly": st.column_config.TextColumn("Anomaly Status")
        }
    )

    # Download Buttons
    c1, c2 = st.columns(2)

    with c1:
        st.download_button(
            "📥 Download Investigation CSV",
            filtered.to_csv(index=False),
            "ciphervista_investigation.csv",
            "text/csv",
            use_container_width=True
        )

    with c2:
        if pdf_path and os.path.exists(pdf_path):
            with open(pdf_path, "rb") as pdf:
                st.download_button(
                    "📥 Download AI Report",
                    pdf,
                    file_name="CipherVista_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
        else:
            st.warning("PDF report was not generated.")

    st.markdown("<div class='cv-divider'></div>", unsafe_allow_html=True)

    # =====================================================
    # 3. Highest Confidence Attacks Table
    # =====================================================

    top_header = """<div class="cv-card-header" style="margin-top:10px;">
<div>
<div class="cv-card-title">🔥 Highest Confidence Attacks</div>
<div class="cv-card-subtitle">Top threat detections ranked by model certainty</div>
</div>
<div class="cv-badge cv-critical">HIGH RISK</div>
</div>"""

    st.markdown(top_header, unsafe_allow_html=True)

    top_attacks = pd.DataFrame(data["top_attacks"])

    if top_attacks.empty:
        st.info("No attack records found.")
        return

    display = top_attacks.sort_values("confidence", ascending=False)[
        ["prediction", "Severity", "confidence", "anomaly", "anomaly_score"]
    ]

    styled_top = display.style.map(style_severity, subset=["Severity"])

    st.dataframe(
        styled_top,
        use_container_width=True,
        hide_index=True,
        height=280,
        column_config={
            "prediction": st.column_config.TextColumn("Attack Prediction"),
            "Severity": st.column_config.TextColumn("Severity"),
            "confidence": st.column_config.ProgressColumn(
                "Confidence Score",
                format="%.2f%%",
                min_value=0,
                max_value=100
            ),
            "anomaly_score": st.column_config.NumberColumn("Anomaly Score", format="%.4f"),
            "anomaly": st.column_config.TextColumn("Anomaly Status")
        }
    )