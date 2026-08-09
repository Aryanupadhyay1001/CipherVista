from textwrap import dedent

def load_css():
    return dedent("""
    <style>

/* =====================================================
   UNIVERSAL CARD
===================================================== */

.cv-card{
    background:linear-gradient(180deg,#111827,#0F172A);
    border:1px solid rgba(59,130,246,.18);
    border-radius:20px;
    padding:24px;
    margin-bottom:22px;
    box-shadow:0 10px 30px rgba(0,0,0,.35);
    transition:.25s ease;
}

.cv-card:hover{
    transform:translateY(-4px);
    border-color:#3B82F6;
    box-shadow:0 16px 40px rgba(37,99,235,.22);
}

.cv-card-header{
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin-bottom:18px;
}

.cv-card-title{
    font-size:24px;
    font-weight:700;
    color:#F8FAFC;
}

.cv-card-subtitle{
    color:#94A3B8;
    font-size:15px;
}

/* =====================================================
   SECTION TITLE
===================================================== */

.cv-section-title{
    font-size:28px;
    font-weight:700;
    margin-bottom:18px;
    color:white;
}

/* =====================================================
   BADGES
===================================================== */

.cv-badge{
    background:#1E40AF;
    color:white;
    padding:6px 14px;
    border-radius:999px;
    font-size:13px;
    font-weight:700;
}

.cv-live{
    background:#14532D;
    color:#4ADE80;
}

.cv-critical{
    background:#7F1D1D;
    color:#F87171;
}

.cv-warning{
    background:#78350F;
    color:#FBBF24;
}

/* =====================================================
   PREMIUM HEADER (Glassmorphism + Glow)
===================================================== */

.cv-header-card {
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.7) 0%, rgba(30, 27, 75, 0.5) 100%);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-top: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 24px;
    padding: 32px 40px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1);
    margin-bottom: 32px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.cv-header-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.cv-welcome-text {
    font-size: 28px;
    font-weight: 400;
    color: #f8fafc;
    margin-bottom: 6px;
    letter-spacing: -0.5px;
}

.cv-user-name-gradient {
    font-weight: 800;
    background: linear-gradient(to right, #60a5fa, #c084fc, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

@keyframes cv-pulse-glow {
    0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); }
    70% { box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }
    100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}

.cv-badge-live-premium {
    background: rgba(16, 185, 129, 0.1);
    color: #34d399;
    border: 1px solid rgba(16, 185, 129, 0.3);
    padding: 8px 18px;
    border-radius: 99px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    animation: cv-pulse-glow 2s infinite;
}

/* =====================================================
   DIVIDER
===================================================== */

.cv-divider{
    height:1px;
    background:#243244;
    margin:18px 0;
}

/* =====================================================
   TABLE CARD
===================================================== */

.cv-table{
    border-radius:16px;
    overflow:hidden;
    border:1px solid #243244;
}

/* =====================================================
   CHART CARD
===================================================== */

.cv-chart{
    background:#111827;
    border-radius:18px;
    padding:20px;
    border:1px solid #243244;
}

/* =====================================================
   INFO GRID
===================================================== */

.cv-grid{
    display:grid;
    grid-template-columns:repeat(2,1fr);
    gap:18px;
}

.cv-item{
    background:#0F172A;
    border:1px solid #243244;
    border-radius:14px;
    padding:16px;
}

.cv-label{
    color:#94A3B8;
    font-size:14px;
}

.cv-value{
    color:white;
    font-size:18px;
    font-weight:600;
    margin-top:6px;
}

/* =====================================================
   AI RESPONSE
===================================================== */

.cv-ai{
    background:linear-gradient(180deg,#0F172A,#111827);
    border-left:4px solid #2563EB;
    border-radius:18px;
    padding:24px;
    margin-top:20px;
}

/* =====================================================
   BUTTON POLISH
===================================================== */

.stButton>button{
    border-radius:14px !important;
    transition:.25s !important;
}

.stButton>button:hover{
    transform:translateY(-3px);
}

/* =====================================================
   METRICS
===================================================== */

div[data-testid="metric-container"]{
    border-radius:18px !important;
    padding:18px !important;
}

/* =====================================================
   FILE UPLOADER
===================================================== */

section[data-testid="stFileUploaderDropzone"]{
    min-height:190px !important;
    border-radius:20px !important;
}

/* =====================================================
   FOOTER
===================================================== */

.cv-footer{
    text-align:center;
    color:#64748B;
    padding:18px;
}

/* =====================================================
   ENTERPRISE SIDEBAR NAVIGATION (CUSTOM)
===================================================== */

/* 1. Hide default Streamlit navigation and reset sidebar */
[data-testid="stSidebarNav"] {
    display: none !important;
}

[data-testid="stSidebar"] {
    background-color: #030712 !important;
    border-right: 1px solid rgba(255, 255, 255, 0.05);
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
    padding: 0 !important;
}

/* 2. Main Container */
.cv-sidebar-container {
    display: flex;
    flex-direction: column;
    padding: 24px 16px;
}

/* 3. Header Styling */
.cv-brand-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 28px;
}

.cv-brand-left {
    display: flex;
    align-items: center;
    gap: 12px;
}

.cv-brand-logo {
    background: linear-gradient(135deg, #6D28D9, #3B82F6);
    width: 38px;
    height: 38px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 0 15px rgba(109, 40, 217, 0.4);
}

.cv-brand-title {
    font-size: 20px;
    font-weight: 700;
    color: white;
    line-height: 1.1;
}

.cv-brand-subtitle {
    font-size: 12px;
    color: #8B5CF6;
    font-weight: 500;
}

/* 4. Active Dashboard Button */
.cv-nav-active {
    background: linear-gradient(90deg, rgba(109, 40, 217, 0.25) 0%, transparent 100%);
    border: 1px solid #7C3AED;
    border-radius: 12px;
    padding: 10px 14px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
    text-decoration: none;
}

.cv-nav-active-left {
    display: flex;
    align-items: center;
    gap: 10px;
    color: white;
    font-size: 15px;
    font-weight: 500;
}

.cv-badge-number {
    background: rgba(109, 40, 217, 0.4);
    color: white;
    padding: 2px 8px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 600;
}

/* 5. Navigation Sections */
.cv-nav-section {
    margin-bottom: 20px;
}

.cv-section-title-nav {
    font-size: 11px;
    color: #64748B;
    letter-spacing: 1.5px;
    font-weight: 600;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 8px;
    text-transform: uppercase;
}

.cv-section-dot {
    width: 6px;
    height: 6px;
    background-color: #7C3AED;
    border-radius: 50%;
}

/* 6. Navigation Items */
.cv-nav-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px 10px;
    color: #94A3B8;
    text-decoration: none;
    border-radius: 8px;
    margin-bottom: 2px;
    transition: all 0.2s ease;
    font-size: 14px;
}

.cv-nav-item-left {
    display: flex;
    align-items: center;
    gap: 10px;
}

.cv-nav-item:hover {
    color: white;
    background: rgba(255, 255, 255, 0.05);
}

.cv-badge-ai {
    background: rgba(109, 40, 217, 0.15);
    color: #A78BFA;
    border: 1px solid rgba(109, 40, 217, 0.3);
    padding: 2px 6px;
    border-radius: 6px;
    font-size: 10px;
    font-weight: 600;
}

/* 7. Footer Profile Card */
.cv-profile-card {
    margin-top: 20px;
    background: linear-gradient(180deg, rgba(255,255,255,0.03), transparent);
    border: 1px solid rgba(109, 40, 217, 0.3);
    border-radius: 14px;
    padding: 12px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.cv-profile-left {
    display: flex;
    align-items: center;
    gap: 10px;
}

.cv-avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: #1E1B4B;
    border: 1px solid #4C1D95;
    color: #A78BFA;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 13px;
    position: relative;
}

.cv-status-dot {
    position: absolute;
    bottom: -1px;
    right: -1px;
    width: 8px;
    height: 8px;
    background: #10B981;
    border: 2px solid #030712;
    border-radius: 50%;
}

.cv-profile-info {
    display: flex;
    flex-direction: column;
}

.cv-profile-name {
    color: white;
    font-size: 13px;
    font-weight: 600;
}

.cv-profile-role {
    color: #64748B;
    font-size: 11px;
}

</style>
""")