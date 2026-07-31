def load_css():
    return """
    <style>

    /* ---------- App ---------- */

    .stApp{
        background:#0B1220;
        color:white;
    }

    .block-container{
        padding-top:2rem;
        padding-bottom:2rem;
        max-width:1400px;
    }

    section[data-testid="stSidebar"]{
        background:#101827;
    }

    h1,h2,h3,h4,h5,h6,label,p{
        color:white !important;
    }

    hr{
        border-color:#1F2937;
    }

    /* ---------- Hero ---------- */

    .hero{
        background:linear-gradient(135deg,#1D4ED8,#0F172A);
        padding:35px;
        border-radius:20px;
        box-shadow:0 12px 30px rgba(0,0,0,.45);
        margin-bottom:25px;
    }

    .hero h1{
        font-size:48px;
        margin-bottom:10px;
    }

    .hero p{
        color:#CBD5E1 !important;
        font-size:18px;
    }

    /* ---------- Metrics ---------- */

    div[data-testid="metric-container"]{
        background:#111827;
        border:1px solid #1F2937;
        border-radius:18px;
        padding:18px;
        box-shadow:0 8px 20px rgba(0,0,0,.35);
        transition:.25s;
    }

    div[data-testid="metric-container"]:hover{
        transform:translateY(-4px);
        border-color:#2563EB;
    }

    /* ---------- Alerts ---------- */

    div[data-testid="stAlert"]{
        border-radius:15px;
    }

    /* ---------- Plotly ---------- */

    .stPlotlyChart{
        background:#111827;
        padding:18px;
        border-radius:18px;
        box-shadow:0 8px 20px rgba(0,0,0,.35);
    }

    /* ---------- Layout ---------- */

    div[data-testid="stVerticalBlock"]{
        gap:1rem;
    }

    /* ====================================================== */
    /*                 FILE UPLOADER                          */
    /* ====================================================== */

    div[data-testid="stFileUploader"]{
        width:100%;
    }

    section[data-testid="stFileUploaderDropzone"]{
        min-height:170px !important;
        background:#111827 !important;
        border:2px dashed #3B82F6 !important;
        border-radius:18px !important;

        display:flex !important;
        justify-content:center !important;
        align-items:center !important;

        transition:0.3s;
    }

    section[data-testid="stFileUploaderDropzone"]:hover{
        border-color:#60A5FA !important;
        background:#172554 !important;
    }

    section[data-testid="stFileUploaderDropzone"] *{
        color:white !important;
    }

    /* Browse files button */

div[data-testid="stBaseButton-secondary"] button{
    color:white !important;
    font-weight:600 !important;
    background:#2563EB !important;
    border:1px solid #3B82F6 !important;
}

div[data-testid="stBaseButton-secondary"] button:hover{
    background:#1D4ED8 !important;
}

    </style>
    """