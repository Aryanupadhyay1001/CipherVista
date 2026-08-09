import streamlit as st


def render_summary(
    stats,
    confidence,
    total,
    attack_breakdown
):
    
    # Start building the HTML string with ZERO leading indentation
    html = f"""<div class="cv-card">
<div class="cv-card-header">
<div>
<div class="cv-card-title">🚨 Executive Summary</div>
<div class="cv-card-subtitle">AI generated overview of the analysed network traffic</div>
</div>
<div class="cv-badge">LIVE</div>
</div>
<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px;">
<div style="background:linear-gradient(180deg,#111827,#0F172A); border:1px solid rgba(255,255,255,.06); border-left:5px solid #EF4444; border-radius:18px; padding:22px; min-height:155px; box-shadow:0 10px 25px rgba(0,0,0,.35);">
<div style="color:#94A3B8; font-size:15px; font-weight:600;">🚨 Attack Rate</div>
<div style="margin-top:18px; color:white; font-size:28px; font-weight:700; line-height:1.3;">{stats['attack_percentage']}%</div>
</div>
<div style="background:linear-gradient(180deg,#111827,#0F172A); border:1px solid rgba(255,255,255,.06); border-left:5px solid #10B981; border-radius:18px; padding:22px; min-height:155px; box-shadow:0 10px 25px rgba(0,0,0,.35);">
<div style="color:#94A3B8; font-size:15px; font-weight:600;">🛡 Benign Traffic</div>
<div style="margin-top:18px; color:white; font-size:28px; font-weight:700; line-height:1.3;">{stats['benign_percentage']}%</div>
</div>
<div style="background:linear-gradient(180deg,#111827,#0F172A); border:1px solid rgba(255,255,255,.06); border-left:5px solid #8B5CF6; border-radius:18px; padding:22px; min-height:155px; box-shadow:0 10px 25px rgba(0,0,0,.35);">
<div style="color:#94A3B8; font-size:15px; font-weight:600;">🎯 Average Confidence</div>
<div style="margin-top:18px; color:white; font-size:28px; font-weight:700; line-height:1.3;">{confidence:.2f}%</div>
</div>
</div>
<div class='cv-divider'></div>
<div class="cv-section-title">🎯 Top Attack Types</div>"""

    # Dynamically append attack breakdowns to the HTML string
    if attack_breakdown:
        for attack, count in sorted(
            attack_breakdown.items(),
            key=lambda x: x[1],
            reverse=True
        ):
            html += f"""
<div class="cv-item" style="margin-bottom:12px;">
<div style="display:flex; justify-content:space-between; align-items:center;">
<span style="color:white; font-weight:600;">{attack}</span>
<span class="cv-badge">{count:,}</span>
</div>
</div>"""
    else:
        # Custom HTML to replace st.info() so we don't break the div structure
        html += """
<div style="background-color: rgba(59, 130, 246, 0.1); border-left: 4px solid #3B82F6; padding: 16px; border-radius: 8px; color: #93C5FD; font-weight: 500;">
ℹ️ No attacks detected.
</div>"""

    # Append the footer of the card
    html += f"""
<div class='cv-divider'></div>
<div class="cv-item">
<div class="cv-label">🌐 Total Network Flows Analysed</div>
<div class="cv-value">{total:,}</div>
</div>
</div>"""

    # Render the complete, unbroken HTML at once
    st.markdown(html, unsafe_allow_html=True)