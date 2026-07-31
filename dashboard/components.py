import streamlit as st
import plotly.express as px


def hero():
    st.markdown("""
    <div class="hero">
        <h1>🛡 CipherVista</h1>
        <p>
        AI Threat Intelligence Platform<br>
        Detect • Analyze • Investigate • Respond
        </p>
    </div>
    """, unsafe_allow_html=True)


def attack_pie_chart(benign, attacks):

    fig = px.pie(
    names=["Benign", "Attack"],
    values=[benign, attacks],
    hole=0.45,
    color_discrete_sequence=[
        "#22C55E",
        "#EF4444"
    ]
)

    fig.update_layout(
    title="🛡 Attack Distribution",
    height=420,
    template="plotly_dark",
    paper_bgcolor="#111827",
    plot_bgcolor="#111827",
    font_color="white",
    legend_title="Traffic"
)

    st.plotly_chart(fig, use_container_width=True)

def traffic_bar_chart(benign, attacks):

    import plotly.graph_objects as go

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=["Benign", "Attack"],
            y=[benign, attacks],
            marker_color=[ "#22C55E","#EF4444"]
        )
    )

    fig.update_layout(
    title="📊 Traffic Comparison",
    height=400,
    template="plotly_dark",
    paper_bgcolor="#111827",
    plot_bgcolor="#111827",
    font_color="white",
    showlegend=False,
    xaxis_title="Traffic Type",
    yaxis_title="Flows"
)

    st.plotly_chart(fig, use_container_width=True)