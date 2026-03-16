import streamlit as st
import pandas as pd
from pathlib import Path

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