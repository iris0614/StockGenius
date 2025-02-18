import sys
import os
import streamlit as st
from dotenv import load_dotenv
import pandas as pd

# Add the project root directory to sys.path.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.api import (
    get_recommendations,
    run_simulation,
    generate_report,
    analyze_investment_strategy,
)

# Load environment variables.
load_dotenv()

# Streamlit page setup.
st.set_page_config(page_title="StockGenius", page_icon="📈", layout="wide")

# Custom CSS for a professional, minimalist UI.
st.markdown(
    """
    <style>
    body {
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        background-color: #f5f5f7;
        color: #1d1d1f;
        margin: 0;
        padding: 0;
    }
    .title {
        font-size: 42px;
        font-weight: 700;
        color: #007aff;
        text-align: center;
        margin-top: 30px;
        margin-bottom: 20px;
    }
    .section-header {
        font-size: 26px;
        font-weight: 600;
        color: #1d1d1f;
        margin-top: 40px;
        margin-bottom: 20px;
        border-bottom: 2px solid #e0e0e0;
        padding-bottom: 5px;
    }
    .stButton>button {
        background-color: #007aff;
        color: #ffffff;
        border: none;
        padding: 10px 20px;
        border-radius: 8px;
        font-size: 16px;
        font-weight: 600;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #005bb5;
    }
    .input-label {
        font-size: 16px;
        font-weight: 500;
        margin-bottom: 5px;
    }
    .report-box {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 20px;
        margin-top: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        padding: 10px;
    }
    .stNumberInput>div>div>input {
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        padding: 10px;
    }
    .stSelectbox>div>div>div {
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Page title.
st.markdown('<div class="title">StockGenius 📈</div>', unsafe_allow_html=True)

# User Investment Preferences.
st.markdown('<div class="section-header">Set Your Investment Preferences</div>', unsafe_allow_html=True)
risk_level = st.selectbox("Risk Level", ["Low", "Medium", "High"])
investment_duration = st.selectbox("Investment Duration", ["Short-term (<1 year)", "Medium-term (1-3 years)", "Long-term (>3 years)"])
investment_strategy = st.text_input("Investment Strategy", "Enter your custom strategy here")

# AI Investment Strategy Analysis.
if st.button("Analyze Investment Strategy"):
    st.markdown('<div class="section-header">AI Investment Strategy Analysis</div>', unsafe_allow_html=True)
    strategy_analysis = analyze_investment_strategy(investment_strategy)
    st.markdown(f"<div class='report-box'><pre>{strategy_analysis}</pre></div>", unsafe_allow_html=True)

# Stock tickers input.
custom_tickers = st.text_input("Enter Stock Tickers (comma separated)", "AAPL, MSFT, GOOGL, AMZN")

# Generate Recommendations.
if st.button("Generate Recommendations"):
    st.markdown('<div class="section-header">Recommended Stocks</div>', unsafe_allow_html=True)
    recs = get_recommendations(risk_level, investment_duration, investment_strategy, custom_tickers)
    if isinstance(recs, pd.DataFrame):
        st.table(recs)
    else:
        st.error(recs if recs else "Please enter at least one ticker.")

# Investment Simulation.
st.markdown('<div class="section-header">Investment Simulation</div>', unsafe_allow_html=True)
investment_amount = st.number_input("Investment Amount (USD)", min_value=100, value=1000)
investment_period = st.number_input("Investment Period (Months)", min_value=1, value=36)

if st.button("Run Simulation"):
    st.markdown('<div class="section-header">Simulation Results</div>', unsafe_allow_html=True)
    sim_result = run_simulation(investment_amount, investment_period, risk_level, investment_strategy)
    if isinstance(sim_result, pd.DataFrame):
        st.table(sim_result)
    else:
        st.error(sim_result)

# Investment Analysis Report.
if st.button("Generate Report"):
    st.markdown('<div class="section-header">Investment Analysis Report</div>', unsafe_allow_html=True)
    ticker = st.text_input("Enter Target Ticker for Analysis", "AAPL")
    competitors_input = st.text_input("Enter Competitor Tickers (comma separated)", "MSFT, GOOGL, AMZN")
    competitors = [t.strip().upper() for t in competitors_input.split(",") if t.strip()]
    report_md, _ = generate_report(ticker.upper(), competitors, risk_level, investment_strategy)
    if report_md is not None:
        st.markdown(f"<div class='report-box'>{report_md}</div>", unsafe_allow_html=True)
    else:
        st.error("Failed to generate report.")