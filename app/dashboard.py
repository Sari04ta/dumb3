import sys
import os

# Add project root to PYTHONPATH
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

import streamlit as st
import pandas as pd

from utils.data_utils import load_restaurant_data, get_restaurant_options
from utils.analysis_utils import (
    compute_all_metrics,
    get_overview,
    get_competitor_view,
    get_sentiment_view,
    get_delivery_view,
    get_price_view,
    get_menu_popularity_view,
)

from src.agent_code import build_context, run_agent

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Agent — Restaurant Market Analysis",
    layout="wide",
)

st.title("AI Agent — Restaurant Market Analysis")
st.caption(
    "Upload a restaurant reviews CSV to analyse performance, competition, "
    "delivery and pricing, and customer satisfaction — then ask an AI agent for insights."
)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("1. Upload data")
    uploaded_file = st.file_uploader("Restaurant reviews CSV", type=["csv"])

if uploaded_file is None:
    st.info("⬆️ Upload the CSV to begin.")
    st.stop()

# ---------------- LOAD DATA ----------------
@st.cache_data(show_spinner=True)
def load_df(file):
    return load_restaurant_data(file)

df = load_df(uploaded_file)

if df.empty:
    st.error("CSV loaded but dataframe is empty.")
    st.stop()

# ---------------- COMPUTE METRICS ----------------
@st.cache_data(show_spinner=True)
def compute(df):
    return compute_all_metrics(df)

metrics = compute(df)

# ---------------- FILTERS ----------------
with st.sidebar:
    st.header("2. Filters")

    names, cities, cuisines = get_restaurant_options(df)

    city = st.selectbox("City", ["All"] + cities)
    cuisine = st.selectbox("Cuisine", ["All"] + cuisines)

    valid_names = []
    for n in names:
        row = metrics["restaurants"].loc[n]
        if city in ("All", str(row["city"])) and cuisine in ("All", str(row["cuisine"])):
            valid_names.append(n)

    if not valid_names:
        st.error("No restaurants match filters.")
        st.stop()

    selected_name = st.selectbox("Restaurant", valid_names)

# ---------------- TABS ----------------
tabs = st.tabs([
    "Overview",
    "Competitors",
    "Sentiment",
    "Delivery",
    "Price",
    "Menu Popularity",
    "AI Agent",
    "Raw Data"
])

# -------- Overview --------
with tabs[0]:
    overview = get_overview(selected_name, metrics)
    st.metric("Avg Rating", f"{overview['avg_rating']:.2f}")
    st.plotly_chart(overview["rating_chart"], use_container_width=True)

# -------- Competitors --------
with tabs[1]:
    comp = get_competitor_view(selected_name, metrics)
    st.plotly_chart(comp["bar_chart"], use_container_width=True)

# -------- Sentiment --------
with tabs[2]:
    sent = get_sentiment_view(selected_name, metrics)
    st.plotly_chart(sent["chart"], use_container_width=True)

# -------- Delivery --------
with tabs[3]:
    st.plotly_chart(get_delivery_view(selected_name, metrics), use_container_width=True)

# -------- Price --------
with tabs[4]:
    st.plotly_chart(get_price_view(selected_name, metrics), use_container_width=True)

# -------- Menu --------
with tabs[5]:
    st.plotly_chart(get_menu_popularity_view(selected_name, metrics), use_container_width=True)

# -------- AI Agent --------
with tabs[6]:
    question = st.text_area("Ask the AI agent")
    if st.button("Run"):
        ctx = build_context(selected_name, question, metrics)
        answer = run_agent(question, ctx)
        st.write(answer)

# -------- Raw Data --------
with tabs[7]:
    st.dataframe(df.head(500))
