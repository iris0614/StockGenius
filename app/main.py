import sys
import os
import streamlit as st
from dotenv import load_dotenv

# Add the project root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.api import get_recommendations, run_simulation, generate_report

# Load environment variables
load_dotenv()

# Streamlit page setup
st.set_page_config(page_title="StockGenius", page_icon="📈", layout="wide")

# Custom CSS
st.markdown(
    """
    <style>
    .title {
        font-size: 36px;
        font-weight: bold;
        color: #2E86C1;
        text-align: center;
        margin-bottom: 30px;
    }
    .section-header {
        font-size: 24px;
        font-weight: bold;
        color: #34495E;
        margin-bottom: 20px;
    }
    .description {
        font-size: 16px;
        color: #566573;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Page title
st.markdown('<div class="title">StockGenius 📈</div>', unsafe_allow_html=True)

# User preferences
st.markdown('<div class="section-header">设置您的投资偏好</div>', unsafe_allow_html=True)
risk_level = st.selectbox("风险偏好", ["低风险", "中风险", "高风险"])
investment_duration = st.selectbox("投资时长", ["短期 (<1年)", "中期 (1-3年)", "长期 (>3年)"])
investment_strategy = st.selectbox("投资策略", ["定投", "一次性投资"])

# Stock recommendations
if st.button("生成推荐"):
    st.markdown('<div class="section-header">推荐股票</div>', unsafe_allow_html=True)
    recommendations = get_recommendations(risk_level, investment_duration, investment_strategy)
    st.write(recommendations)

# DCA simulation
st.markdown('<div class="section-header">定投模拟</div>', unsafe_allow_html=True)
investment_amount = st.number_input("每月定投金额（美元）", min_value=100, value=1000)
investment_period = st.number_input("定投时长（月）", min_value=1, value=36)

if st.button("运行模拟"):
    st.markdown('<div class="section-header">模拟结果</div>', unsafe_allow_html=True)
    simulation_result = run_simulation(investment_amount, investment_period, risk_level)
    st.write(simulation_result)

# Generate analysis report
if st.button("生成报告"):
    st.markdown('<div class="section-header">投资分析报告</div>', unsafe_allow_html=True)
    report_content = generate_report(risk_level, investment_duration, investment_strategy)
    st.markdown(report_content, unsafe_allow_html=True)