import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import plotly.io as pio
pio.templates.default = "plotly_white"

BASE_DIR = Path(__file__).resolve().parent.parent

df = pd.read_csv(BASE_DIR / "data/processed/epl_2022-23_scs-ready.csv")

st.set_page_config(
    page_title="The Invisible 11",
    page_icon="⚽",
    layout="wide"
)

st.title("⚽ The Invisible 11 — Player Impact Analyzer")

st.markdown(
"""
Explore player contributions beyond goals and assists using the **Shadow Contribution Score (SCS)**.
"""
)

st.subheader("🏆 Shadow Contribution Score Leaderboard")

leaderboard = (
    df.sort_values("SCS", ascending=False)
    [["Player", "Squad", "Pos", "Goals", "SCS"]]
    .reset_index(drop=True)
)

leaderboard.index = leaderboard.index + 1
leaderboard.index.name = "Rank"

st.dataframe(
    leaderboard,
    use_container_width=True
)

st.subheader("📊 Player Impact Map")

fig = px.scatter(
    df,
    x="Goals",
    y="SCS",
    color="Pos",
    hover_data={
        "Player": True,
        "Squad": True,
        "Goals": True,
        "SCS": ':.2f'
    },
    custom_data=["Player", "Squad", "Pos"],
    title="Player Impact Map: Revealing Contribution Beyond Goals",
    labels={
        "Goals": "Goals Scored",
        "SCS": "Shadow Contribution Score"
    },
    color_discrete_map={
        "FW": "#1f77b4",
        "MF": "#ff7f0e",
        "DF": "#2ca02c"
    }
)

# median lines
scs_median = df["SCS"].median()
goals_median = df["Goals"].median()

fig.add_annotation(
    x=0.5,
    y=88,
    text="Invisible Contributors",
    showarrow=False,
    font=dict(size=13, color="black")
)

fig.add_annotation(
    x=13,
    y=88,
    text="Elite All-Rounders",
    showarrow=False,
    font=dict(size=13, color="black")
)

fig.add_annotation(
    x=13,
    y=21.3,
    text="Goal Specialists",
    showarrow=False,
    font=dict(size=13, color="black")
)

fig.add_annotation(
    x=0.5,
    y=21.3,
    text="Low Impact Players",
    showarrow=False,
    font=dict(size=13, color="black")
)

fig.add_vline(
    x=goals_median,
    line_dash="dash",
    line_color="gray",
    line_width=2,
    opacity=0.6
)

fig.add_hline(
    y=scs_median,
    line_dash="dash",
    line_color="gray",
    line_width=2,
    opacity=0.6
)

fig.update_traces(
    marker=dict(
        size=9,
        opacity=0.85,
        line=dict(width=1, color="white")
    ),
    hovertemplate=
    "<b>%{customdata[0]}</b><br>" +
    "Squad=%{customdata[1]}<br>" +
    "Pos=%{customdata[2]}<br>" +
    "Goals Scored=%{x}<br>" +
    "Shadow Contribution Score=%{y:.2f}" +
    "<extra></extra>"
)

fig.update_layout(
    template="plotly_white",
    
    title=dict(
        text="Player Impact Map: Revealing Contribution Beyond Goals",
        x=0.5,
        xanchor="center",
        font=dict(size=22, color="black")
    ),

    height=650,

    paper_bgcolor="white",
    plot_bgcolor="white",

    legend=dict(
        title=dict(
            text="<b>Position</b>",
            font=dict(size=14, color="black")
        ),
        font=dict(size=12, color="black"),
        x=1.02,
        y=1,
        xanchor="left",
        yanchor="top"
    ),

    xaxis=dict(
        title="Goals Scored",
        title_font=dict(size=16, color="black"),
        tickfont=dict(size=12, color="black"),
        showgrid=True,
        gridcolor="rgba(0,0,0,0.06)",
        zeroline=False
    ),

        yaxis=dict(
        title="Shadow Contribution Score",
        title_font=dict(size=16, color="black"),
        tickfont=dict(size=12, color="black"),
        showgrid=True,
        gridcolor="rgba(0,0,0,0.06)",
        zeroline=False
    ),

    hoverlabel=dict(
        bgcolor="white",
        font_size=12,
        font_color="black"
    ),
    margin=dict(l=60, r=40, t=80, b=60),
    legend_title_side="top"
)

st.plotly_chart(fig, use_container_width=True)