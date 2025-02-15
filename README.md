# StockGenius 📈

---

## Introduction
**StockGenius** is a stock investment analysis tool built with Streamlit and powered by DeepSeek API. It helps users generate personalized stock recommendations, dollar-cost averaging (DCA) simulations, and investment analysis reports based on their risk preferences, investment horizon, and strategy. Whether you're a beginner or an experienced investor, StockGenius provides data-driven insights to guide your investment decisions.

---

## Key Features
- **Personalized Stock Recommendations**: Get tailored stock suggestions based on your risk tolerance and investment goals.
- **DCA Simulation**: Simulate the returns and risks of a dollar-cost averaging plan with visual charts.
- **Investment Analysis Report**: Generate concise analysis reports and download them as PDFs.
- **AI-Powered Insights**: Leverage DeepSeek API for intelligent analysis and recommendations.

---

## Setup

1. **Clone the repository**:
   ```bash
   git clone git@github.com:iris0614/StockGenius.git
   cd StockGenius
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   - Create a `.env` file in the root directory with your OpenAI API key:
     ```env
     OPENAI_API_KEY=your_openai_api_key
     ```


1. **Run the Streamlit app**:
   ```bash
   streamlit run app/main.py
   ```

After a moment, Streamlit will open a new tab in your browser (usually at `http://localhost:8501`).