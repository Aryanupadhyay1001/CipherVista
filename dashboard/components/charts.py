import pandas as pd
import plotly.express as px
import streamlit as st


def render_charts(attack_breakdown):

    header_html = """<div class="cv-card-header" style="margin-top: 10px;">
<div>
<div class="cv-card-title">📊 Attack Analytics</div>
<div class="cv-card-subtitle">Visual distribution and frequency analysis of detected threat vectors</div>
</div>
<div class="cv-badge">VISUALIZATION</div>
</div>"""

    st.markdown(header_html, unsafe_allow_html=True)

    if not attack_breakdown:
        st.info("No attack data available to display charts.")
        return

    chart_df = pd.DataFrame(
        attack_breakdown.items(),
        columns=["Attack Type", "Count"]
    )

    # FIXED: Re-added the "" symbol so it stops hyphenating every letter!
    # Also added extra cleanup to ensure the text looks pristine.
    chart_df["Attack Type"] = (
        chart_df["Attack Type"]
        .str.replace("", "-", regex=False)
        .str.replace("_", " ")
        .str.replace("Web Attack -", "Web Attack")
        .str.replace("-", " ") 
        .str.strip()
    )

    chart_df = (
        chart_df
        .sort_values("Count", ascending=False)
        .head(6)
    )

    CYBER_PALETTE = [
        "#EF4444", "#F97316", "#8B5CF6", "#0EA5E9", "#F43F5E", "#10B981"
    ]

    left, right = st.columns(2)

    # ---------------- PIE / DONUT CHART ---------------- #

    with left:

        sub_pie_html = """<div style="background: #0F172A; border: 1px solid #243244; border-radius: 16px; padding: 16px; margin-bottom: 12px;">
<div style="color: white; font-size: 18px; font-weight: 700;">📊 Attack Distribution</div>
<div style="color: #94A3B8; font-size: 13px;">Percentage breakdown of top attack classes</div>
</div>"""
        st.markdown(sub_pie_html, unsafe_allow_html=True)

        pie = px.pie(
            chart_df,
            names="Attack Type",
            values="Count",
            hole=.75, 
            color="Attack Type",
            color_discrete_sequence=CYBER_PALETTE
        )

        pie.update_traces(
            textposition="outside",
            textinfo="percent",
            textfont=dict(size=15, color="white", family="Arial Black, sans-serif"),
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Flows: %{value:,}<br>"
                "Share: %{percent}<extra></extra>"
            ),
            marker=dict(
                line=dict(
                    color="#0B1220", 
                    width=4          
                )
            )
        )

        pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=20, b=20),
            height=450,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.25,
                xanchor="center",
                x=0.5,
                font=dict(color="#E2E8F0", size=13, family="sans-serif")
            ),
            font=dict(color="white")
        )

        st.plotly_chart(pie, use_container_width=True)

    # ---------------- HORIZONTAL BAR CHART ---------------- #

    with right:

        sub_bar_html = """<div style="background: #0F172A; border: 1px solid #243244; border-radius: 16px; padding: 16px; margin-bottom: 12px;">
<div style="color: white; font-size: 18px; font-weight: 700;">🏆 Top Attack Types</div>
<div style="color: #94A3B8; font-size: 13px;">Total flow count of identified threats</div>
</div>"""
        st.markdown(sub_bar_html, unsafe_allow_html=True)

        # FIXED: Pass text="Count" directly into px.bar so Plotly handles the sorting!
        bar = px.bar(
            chart_df,
            x="Count",
            y="Attack Type",
            orientation="h",
            color="Attack Type", 
            text="Count", 
            color_discrete_sequence=CYBER_PALETTE
        )

        bar.update_traces(
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Count: %{x:,}<extra></extra>"
            ),
            texttemplate="%{text:,}", # Format numbers with commas dynamically
            textposition="outside",
            textfont=dict(size=14, color="white", family="Arial Black, sans-serif"),
            marker=dict(
                line=dict(color="rgba(255,255,255,0.1)", width=1)
            )
        )

        bar.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
            font=dict(
                color="white",
                size=14,
                family="sans-serif"
            ),
            yaxis=dict(
                categoryorder="total ascending",
                showgrid=False,
                tickfont=dict(size=13, color="#E2E8F0", family="sans-serif", weight="bold")
            ),
            xaxis=dict(
                showgrid=True,
                gridcolor="rgba(255,255,255,0.05)",
                tickfont=dict(size=12, color="#64748B")
            ),
            xaxis_title="",
            yaxis_title="",
            margin=dict(
                l=10,
                r=50, 
                t=10,
                b=10
            ),
            height=450,
            # Extend x-axis slightly so the numbers don't get cut off on the right
            xaxis_range=[0, chart_df["Count"].max() * 1.25]
        )

        st.plotly_chart(bar, use_container_width=True)

    st.markdown("<div class='cv-divider'></div>", unsafe_allow_html=True)