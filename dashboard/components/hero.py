from pathlib import Path
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
LOGO_PATH = ROOT / "assets" / "logo.png"


def render_hero():

    col1, col2 = st.columns([1.3, 4.7], vertical_alignment="center")

    with col1:

        if LOGO_PATH.exists():
            st.image(str(LOGO_PATH), width=190)

    with col2:

        title_col, badge_col = st.columns([5, 2])

        with title_col:
            st.markdown(
                """
                <h1 style="
                    font-size:56px;
                    font-weight:800;
                    margin:0;
                    color:white;
                    letter-spacing:-2px;
                ">
                    CipherVista
                </h1>
                """,
                unsafe_allow_html=True
            )

        with badge_col:
            st.markdown(
                """
                <div style="
                    background:#2563EB;
                    color:white;
                    text-align:center;
                    border-radius:999px;
                    padding:8px 18px;
                    margin-top:12px;
                    font-size:14px;
                    font-weight:700;
                    width:130px;
                    float:right;
                ">
                    Version 3.0
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown(
            """
            <h3 style="
                margin-top:10px;
                color:#60A5FA;
                font-weight:700;
                margin-bottom:10px;
            ">
                AI-Powered Threat Intelligence Platform
            </h3>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <p style="
                font-size:18px;
                color:#CBD5E1;
                line-height:1.8;
                margin-bottom:20px;
            ">
                Enterprise Network Threat Detection,
                AI-powered Investigation,
                Machine Learning Analytics,
                and Automated SOC Reporting using
                <b>Random Forest</b>,
                <b>Isolation Forest</b>,
                and
                <b>Google Gemini AI</b>.
            </p>
            """,
            unsafe_allow_html=True
        )

        chip1, chip2, chip3, chip4 = st.columns(4)

        with chip1:
            st.success("🟢 Threat Engine")

        with chip2:
            st.success("🟢 AI Analyst")

        with chip3:
            st.success("🟢 ML Detection")

        with chip4:
            st.success("🟢 System Online")

    st.divider()