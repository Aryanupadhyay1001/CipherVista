import streamlit as st


def render_model_info():
    html = """<div class="cv-card">
<div class="cv-card-header">
<div>
<div class="cv-card-title">📋 Model Information</div>
<div class="cv-card-subtitle">Machine learning models powering CipherVista</div>
</div>
<div class="cv-badge">ACTIVE</div>
</div>
<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px;">
<div style="background:linear-gradient(180deg,#111827,#0F172A); border:1px solid rgba(255,255,255,.06); border-left:5px solid #2563EB; border-radius:18px; padding:22px; min-height:155px; box-shadow:0 10px 25px rgba(0,0,0,.35);">
<div style="color:#94A3B8; font-size:15px; font-weight:600;">🧠 Classifier</div>
<div style="margin-top:18px; color:white; font-size:28px; font-weight:700; line-height:1.3;">Random Forest</div>
</div>
<div style="background:linear-gradient(180deg,#111827,#0F172A); border:1px solid rgba(255,255,255,.06); border-left:5px solid #10B981; border-radius:18px; padding:22px; min-height:155px; box-shadow:0 10px 25px rgba(0,0,0,.35);">
<div style="color:#94A3B8; font-size:15px; font-weight:600;">🔍 Anomaly Detector</div>
<div style="margin-top:18px; color:white; font-size:28px; font-weight:700; line-height:1.3;">Isolation Forest</div>
</div>
<div style="background:linear-gradient(180deg,#111827,#0F172A); border:1px solid rgba(255,255,255,.06); border-left:5px solid #F59E0B; border-radius:18px; padding:22px; min-height:155px; box-shadow:0 10px 25px rgba(0,0,0,.35);">
<div style="color:#94A3B8; font-size:15px; font-weight:600;">📂 Training Dataset</div>
<div style="margin-top:18px; color:white; font-size:28px; font-weight:700; line-height:1.3;">CICIDS2017</div>
</div>
</div>
</div>"""

    st.markdown(html, unsafe_allow_html=True)