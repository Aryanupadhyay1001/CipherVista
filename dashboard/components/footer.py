import streamlit as st


def render_footer():

    html = """<div class="cv-card" style="margin-top: 80px; padding: 28px;">
<div style="display: grid; grid-template-columns: 1.2fr 1fr; gap: 32px; align-items: start;">

<!-- Left Section: App Info & Tech Stack -->
<div>
<div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
<span style="font-size: 28px;">🛡️</span>
<span style="font-size: 26px; font-weight: 800; color: white;">CipherVista</span>
<span style="background: #2563EB; color: white; padding: 4px 12px; border-radius: 999px; font-size: 12px; font-weight: 700;">v3.0</span>
</div>

<p style="color: #94A3B8; font-size: 15px; margin-top: 0; margin-bottom: 20px;">
Enterprise AI Threat Intelligence Platform
</p>

<div style="color: #F8FAFC; font-weight: 700; font-size: 15px; margin-bottom: 12px;">🛠️ Technology Stack</div>

<div style="display: flex; flex-wrap: wrap; gap: 8px;">
<span style="background: #1E293B; border: 1px solid #334155; color: #E2E8F0; padding: 6px 12px; border-radius: 10px; font-size: 13px; font-weight: 600;">🐍 Python</span>
<span style="background: #1E293B; border: 1px solid #334155; color: #E2E8F0; padding: 6px 12px; border-radius: 10px; font-size: 13px; font-weight: 600;">⚡ FastAPI</span>
<span style="background: #1E293B; border: 1px solid #334155; color: #E2E8F0; padding: 6px 12px; border-radius: 10px; font-size: 13px; font-weight: 600;">🎈 Streamlit</span>
<span style="background: #1E293B; border: 1px solid #334155; color: #E2E8F0; padding: 6px 12px; border-radius: 10px; font-size: 13px; font-weight: 600;">🌲 Random Forest</span>
<span style="background: #1E293B; border: 1px solid #334155; color: #E2E8F0; padding: 6px 12px; border-radius: 10px; font-size: 13px; font-weight: 600;">🌳 Isolation Forest</span>
<span style="background: #1E293B; border: 1px solid #334155; color: #E2E8F0; padding: 6px 12px; border-radius: 10px; font-size: 13px; font-weight: 600;">🤖 Google Gemini AI</span>
</div>
</div>

<!-- Right Section: Developer Contacts -->
<div>
<div style="color: #F8FAFC; font-weight: 700; font-size: 18px; margin-bottom: 4px;">👨‍💻 Developer</div>
<div style="color: #3B82F6; font-size: 20px; font-weight: 700; margin-bottom: 16px;">Aryan Upadhyay</div>

<div style="display: flex; flex-direction: column; gap: 10px;">
<a href="https://mail.google.com/mail/u/0/?compose=GTvVlcSHwQcxvSsDgWVWHSksFwbfwwbtccdVfdXbdtcFSdMfTPJDVKMxsmSHNzgnCZRGwnCZDSvrM#inbox?compose=DmwnWrRlQQLQGLqCbRQMjtRrJsCxjTKmMGLCMdgtpbjZSKvbjQmhtZtdxgtFVTpLtLctrzrsNZzL" target="_blank" style="text-decoration: none; color: #94A3B8; font-size: 14px; display: flex; align-items: center; gap: 8px;">
<span>📧</span> <span style="color: #94A3B8;">aryanupadhyay@gmail.com</span>
</a>
<a href="https://github.com/Aryanupadhyay1001" target="_blank" style="text-decoration: none; color: #60A5FA; font-size: 14px; display: flex; align-items: center; gap: 8px;">
<span>🐙</span> <span>GitHub Profile</span>
</a>
<a href="https://www.linkedin.com/in/aryan-upadhyay-b26a282a4/" target="_blank" style="text-decoration: none; color: #60A5FA; font-size: 14px; display: flex; align-items: center; gap: 8px;">
<span>💼</span> <span>LinkedIn Profile</span>
</a>
<div style="color: #64748B; font-size: 13px; font-style: italic; margin-top: 2px;">
🌐 Portfolio (Under Development)
</div>
</div>
</div>

</div>

<div class="cv-divider" style="margin: 20px 0 16px 0;"></div>

<div style="text-align: center; color: #64748B; font-size: 13px; font-weight: 500;">
© 2026 Aryan Upadhyay • All Rights Reserved
</div>
</div>"""

    st.markdown(html, unsafe_allow_html=True)