import pandas as pd
import streamlit as st
import requests

from styles import load_css
from components import hero, attack_pie_chart, traffic_bar_chart

st.set_page_config(
    page_title="CipherVista",
    page_icon="🛡",
    layout="wide"
)

st.markdown(load_css(), unsafe_allow_html=True)

hero()

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
### 📂 Upload Network Traffic

Upload your network traffic dataset for AI-powered threat detection.

**Supported format:** CSV

**Maximum file size:** 200 MB
""")

uploaded_file = st.file_uploader(
    "",
    type=["csv"],
    label_visibility="collapsed"
)

if uploaded_file is not None:

    if st.button("🔍 Analyze Threats"):

        with st.spinner("Running AI Threat Analysis..."):

            response = requests.post(
                "http://127.0.0.1:8000/predict-file",
                files={
                    "file": (
                        uploaded_file.name,
                        uploaded_file,
                        "text/csv"
                    )
                }
            )

        if response.status_code == 200:

            data = response.json()

            summary = data["summary"]
            stats = data["statistics"]
            risk = data["risk"]

            total = summary["total_records"]
            benign = summary["benign"]
            attacks = summary["attacks"]
            anomalies = summary["anomalies"]

            confidence = stats["average_confidence"]
            risk_level = risk["level"]

            st.success("✅ Analysis Completed Successfully")

            c1, c2, c3, c4, c5, c6 = st.columns(6)

            c1.metric("Total Flows", f"{total:,}")
            c2.metric("Benign", f"{benign:,}")
            c3.metric("Attacks", f"{attacks:,}")
            c4.metric("Anomalies", f"{anomalies:,}")
            c5.metric("Average Prediction Confidence", f"{confidence}%")
            c6.metric("Risk", risk_level)

            st.divider()

            top_left, top_right = st.columns([2, 1])

            with top_left:
                attack_pie_chart(benign, attacks)

            with top_right:
                st.subheader("📋 Model Information")

                st.write("**Classifier**")
                st.write("Random Forest")

                st.write("**Anomaly Detector**")
                st.write("Isolation Forest")

                st.write("**Dataset**")
                st.write("CICIDS2017")

                st.write("**Average Prediction Confidence**")
                st.write(f"{confidence}%")

            st.divider()

            bottom_left, bottom_right = st.columns([2, 1])

            with bottom_left:
                traffic_bar_chart(benign, attacks)

            with bottom_right:
                st.subheader("🚨 Executive Summary")

                st.success(f"Risk Level: {risk_level}")

                st.write(f"**Attack Traffic:** {stats['attack_percentage']}%")
                st.write(f"**Benign Traffic:** {stats['benign_percentage']}%")
                st.write(f"**Total Flows:** {total:,}")

            st.divider()

            threats = pd.DataFrame(data["threats"])

            # def severity(row):
            #     if row["prediction"] == "Attack" and row["anomaly"]:
            #         return "Critical"
            #     elif row["prediction"] == "Attack":
            #         return "High"
            #     return "Safe"

            # threats["Severity"] = threats.apply(severity, axis=1)

            critical_count = len(threats[threats["Severity"] == "Critical"])
            high_count = len(threats[threats["Severity"] == "High"])
            safe_count = len(threats[threats["Severity"] == "Safe"])

            st.subheader("📊 Threat Statistics")

            m1, m2, m3, m4 = st.columns(4)

            m1.metric("🚨 Critical", critical_count)
            m2.metric("⚠️ High", high_count)
            m3.metric("🟢 Safe", safe_count)
            m4.metric("📈 Avg Confidence", f"{confidence}%")

            st.divider()

            st.subheader("🔍 Threat Investigation")

            left, right = st.columns(2)

            with left:
                prediction_filter = st.selectbox(
                    "Prediction",
                    ["All", "Attack", "Benign"]
                )

            with right:
                severity_filter = st.selectbox(
                    "Severity",
                    ["All", "Critical", "High", "Safe"]
                )

            filtered = threats.copy()

            if prediction_filter != "All":
                filtered = filtered[
                    filtered["prediction"] == prediction_filter
                ]

            if severity_filter != "All":
                filtered = filtered[
                    filtered["Severity"] == severity_filter
                ]

            st.dataframe(
                filtered,
                use_container_width=True,
                hide_index=True
            )

            st.download_button(
                "📥 Download Investigation CSV",
                filtered.to_csv(index=False),
                file_name="ciphervista_investigation.csv",
                mime="text/csv"
            )
            st.divider()

            st.subheader("🔥 Highest Confidence Attacks")

            top_attacks = pd.DataFrame(data["top_attacks"])

            # top_attacks["Severity"] = top_attacks.apply(severity, axis=1)

            if top_attacks.empty:
                st.info("No attack records found.")
            else:
                display = top_attacks[
                    [
                        "prediction",
                        "Severity",
                        "confidence",
                        "anomaly",
                        "anomaly_score"
                    ]
                ]

                st.dataframe(
                    display,
                    use_container_width=True,
                    hide_index=True
                )
        else:
            st.error(response.text)