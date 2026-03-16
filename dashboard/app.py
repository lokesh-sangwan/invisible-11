import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
from pathlib import Path

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


st.subheader("🕸 Player Performance Radar")

player_list = sorted(df["Player"].unique())

selected_player = st.selectbox(
    "Select a player",
    player_list
)

radar_features = [
    "defensive_impact",
    "pressing_ball_winning",
    "ball_progression",
    "chance_creation",
    "possession_retention",
    "off_ball_activity"
]

radar_labels = [
    "Defensive Impact",
    "Pressing & Ball Winning",
    "Ball Progression",
    "Chance Creation",
    "Possession Retention",
    "Off-Ball Activity"
]

player_data = df[df["Player"] == selected_player].iloc[0]

values = [player_data[f] for f in radar_features]
values += values[:1]

labels = radar_labels + radar_labels[:1]

radar_fig = go.Figure()

radar_fig.add_trace(go.Scatterpolar(
    r=values,
    theta=labels,
    fill="toself",
    name=selected_player,

    mode="lines+markers",

    line=dict(
        color="royalblue",
        width=3
    ),

    marker=dict(
        size=6,
        color="royalblue"
    ),

    fillcolor="rgba(65,105,225,0.30)",

    hovertemplate="<b>%{theta}</b><br>Percentile: %{r:.1f}<extra></extra>"
))

radar_fig.update_layout(

    title=dict(
        text=f"{selected_player} — Performance Profile",
        x=0.5,
        xanchor="center",
        font=dict(size=22, color="black")
    ),

    polar=dict(

        bgcolor="white",

        radialaxis=dict(
            visible=True,
            range=[0,100],
            tickvals=[0,20,40,60,80,100],
            tickfont=dict(size=11, color="black"),
            gridcolor="rgba(0,0,0,0.18)",
            linecolor="rgba(0,0,0,0.35)",
            linewidth=1.5
        ),

        angularaxis=dict(
            tickfont=dict(size=12, color="black"),
            gridcolor="rgba(0,0,0,0.15)",
            linecolor="rgba(0,0,0,0.35)"
        )
    ),

    paper_bgcolor="white",
    plot_bgcolor="white",

    height=650,

    margin=dict(l=80, r=80, t=80, b=80),

    showlegend=False
)

st.plotly_chart(radar_fig, use_container_width=True)