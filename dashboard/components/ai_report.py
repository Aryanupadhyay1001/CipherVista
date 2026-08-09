import streamlit as st


def render_ai_report(ai_report):

    st.title("🤖 AI Security Report")

    st.caption(
        "Generated automatically by Google Gemini based on "
        "CipherVista threat detection results."
    )

    st.divider()

    st.markdown(ai_report)