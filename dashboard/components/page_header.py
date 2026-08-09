import streamlit as st
from pathlib import Path
import base64
from io import BytesIO
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent.parent
LOGO_PATH = ROOT / "assets" / "favicon.ico"

def get_logo_base64():
    if LOGO_PATH.exists():
        image = Image.open(LOGO_PATH).convert("RGBA")
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode()
    return ""

def render_page_header(title, subtitle):
    html_code = f"""<div style="position:relative; overflow:hidden; background: radial-gradient(circle at 85% 20%, rgba(79,70,229,0.18), transparent 28%), radial-gradient(circle at 15% 100%, rgba(37,99,235,0.12), transparent 30%), linear-gradient(135deg,#0B1020 0%,#10172B 55%,#0C1222 100%); border:1px solid rgba(99,102,241,0.32); border-radius:22px; padding:24px 28px 20px 28px; margin-bottom:26px; box-shadow: 0 18px 45px rgba(0,0,0,0.28), inset 0 1px 0 rgba(255,255,255,0.04);">
<div style="position:absolute; top:-80px; right:-70px; width:220px; height:220px; border-radius:50%; background:rgba(99,102,241,0.07); filter:blur(5px);"></div>
<div style="position:relative; display:flex; justify-content:space-between; align-items:center; gap:30px;">
<div style="display:flex; align-items:center; gap:18px; min-width:0;">
<div style="
    width:64px;
    height:64px;
    min-width:64px;
    border-radius:18px;
    display:flex;
    align-items:center;
    justify-content:center;
    background:linear-gradient(145deg,#172554,#111827);
    border:1px solid rgba(96,165,250,0.38);
    box-shadow:
        0 0 24px rgba(37,99,235,0.18),
        inset 0 1px 0 rgba(255,255,255,0.06);
    overflow:hidden;
">
    <img
        src="data:image/x-icon;base64,{get_logo_base64()}"
        style="
            width:48px;
            height:48px;
            object-fit:contain;
        "
    >
</div>
<div style="min-width:0;">
<div style="display:flex; align-items:center; gap:10px; margin-bottom:5px;">
<span style="color:#93C5FD; font-size:11px; font-weight:800; letter-spacing:2px; text-transform:uppercase;">CIPHERVISTA</span>
<span style="color:#64748B; font-size:11px;">/</span>
<span style="color:#A78BFA; font-size:11px; font-weight:700; letter-spacing:1.5px;">SOC COMMAND CENTER</span>
</div>
<h1 style="margin:0; color:#F8FAFC; font-size:30px; line-height:1.15; font-weight:800; letter-spacing:-0.7px;">{title}</h1>
<p style="margin:7px 0 0 0; color:#94A3B8; font-size:14px; line-height:1.5;">{subtitle}</p>
</div>
</div>
<div style="display:flex; flex-direction:column; align-items:flex-end; gap:10px; min-width:205px;">
<div style="display:flex; align-items:center; gap:9px; background:rgba(16,185,129,0.08); border:1px solid rgba(16,185,129,0.28); padding:8px 14px; border-radius:999px;">
<span style="width:8px; height:8px; border-radius:50%; background:#10B981; box-shadow:0 0 10px rgba(16,185,129,0.8);"></span>
<span style="color:#34D399; font-size:11px; font-weight:800; letter-spacing:1.2px;">SYSTEM OPERATIONAL</span>
</div>
<div style="display:flex; align-items:center; gap:8px; color:#94A3B8; font-size:12px;">
<span style="color:#60A5FA;">●</span> AI Threat Engine <span style="color:#10B981;font-weight:700;">ONLINE</span>
</div>
</div>
</div>
<div style="position:relative; height:1px; margin:20px 0 15px 0; background:linear-gradient(90deg, rgba(96,165,250,0.22), rgba(139,92,246,0.16), transparent);"></div>
<div style="position:relative; display:flex; align-items:center; justify-content:space-between; gap:15px; flex-wrap:wrap;">
<div style="display:flex; align-items:center; gap:8px;">
<span style="color:#CBD5E1; font-size:12px; font-weight:600;">Analyst Console</span>
<span style="color:#475569;">•</span>
<span style="color:#60A5FA; font-size:12px; font-weight:700;">Tier 2 SOC</span>
</div>
<div style="display:flex; align-items:center; gap:22px;">
<div style="display:flex; align-items:center; gap:7px; color:#94A3B8; font-size:11px;">
<span style="color:#A78BFA;">◆</span> Gemini AI <span style="color:#34D399;font-weight:700;">READY</span>
</div>
<div style="display:flex; align-items:center; gap:7px; color:#94A3B8; font-size:11px;">
<span style="color:#60A5FA;">◆</span> ML Detection <span style="color:#34D399;font-weight:700;">ACTIVE</span>
</div>
<div style="background:linear-gradient(135deg,#2563EB,#4F46E5); color:white; padding:6px 11px; border-radius:8px; font-size:10px; font-weight:800; letter-spacing:1px; box-shadow:0 5px 16px rgba(37,99,235,0.22);">v3.0</div>
</div>
</div>
</div>"""

    st.markdown(html_code, unsafe_allow_html=True)