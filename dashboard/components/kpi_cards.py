import streamlit as st


def kpi_card(title, value, subtitle, color, icon):
    # Flattened HTML string to prevent Markdown from rendering it as a code block
    html = f"""<div style="background:linear-gradient(180deg,#111827,#0F172A); border:1px solid rgba(255,255,255,.06); border-left:6px solid {color}; border-radius:20px; padding:22px; min-height:185px; box-shadow:0 12px 30px rgba(0,0,0,.35); transition:.3s;">
<div style="display:flex; justify-content:space-between; align-items:center;">
<div style="font-size:18px; font-weight:700; color:white;">{icon} {title}</div>
<div style="background:{color}; color:white; padding:5px 12px; border-radius:999px; font-size:12px; font-weight:700;">LIVE</div>
</div>
<div style="font-size:42px; font-weight:800; color:white; margin-top:22px; margin-bottom:12px;">{value}</div>
<div style="color:#94A3B8; font-size:16px; margin-bottom:18px;">{subtitle}</div>
<hr style="border:none; border-top:1px solid #243244; margin:16px 0;">
<div style="display:flex; justify-content:space-between; align-items:center; color:#64748B; font-size:13px;">
<span>Updated just now</span>
<span style="color:{color}; font-weight:700;">● Operational</span>
</div>
</div>"""

    st.markdown(html, unsafe_allow_html=True)


def render_kpi_cards(total, attacks, confidence, risk_level):

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        kpi_card(
            "Total Traffic",
            f"{total:,}",
            "Network Flows",
            "#2563EB",
            "🌐"
        )

    with c2:
        kpi_card(
            "Threats",
            f"{attacks:,}",
            "Detected Attacks",
            "#EF4444",
            "🚨"
        )

    with c3:
        kpi_card(
            "Confidence",
            f"{confidence:.2f}%",
            "Model Accuracy",
            "#10B981",
            "🛡️"
        )

    with c4:

        risk = str(risk_level).lower()

        if risk == "critical":
            color = "#DC2626"
        elif risk == "high":
            color = "#EA580C"
        elif risk == "medium":
            color = "#D97706"
        else:
            color = "#16A34A"

        kpi_card(
            "Risk Level",
            str(risk_level).upper(),
            "Overall Assessment",
            color,
            "⚠️"
        )

    st.markdown("<br>", unsafe_allow_html=True)