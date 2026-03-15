import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="The Invisible 11",
    layout="wide"
)

st.title("⚽ The Invisible 11 — Player Impact Analyzer")

st.write(
"""
This dashboard explores player contribution beyond goals and assists
using the **Shadow Contribution Score (SCS)**.
"""
)

df = pd.read_csv("../data/processed/epl_2022-23_scs-ready.csv")