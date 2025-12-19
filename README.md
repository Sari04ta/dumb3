# AI Agent – Restaurant Market Analysis (Final)

This repository is a modular AI Agent system for restaurant market intelligence.

## Key Agents
- Data Agent (CSV ingestion)
- NLP & Sentiment Agent
- Competitor Analysis Agent
- Seating Intelligence Agent
- Complaint Intelligence Agent
- Decision Agent
- Streamlit Dashboard

## Structure
src/    -> AI agent logic
app/    -> Streamlit dashboard
utils/  -> Data & analysis helpers
data/   -> Input CSVs
models/ -> Trained models
reports/-> Generated outputs

## Run
pip install -r requirements.txt
streamlit run app/dashboard.py