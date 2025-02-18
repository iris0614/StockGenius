import os
import yfinance as yf
import pandas as pd
import numpy as np
import openai
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def fetch_stock_data(ticker):
    stock = yf.Ticker(ticker)
    return stock.history(period="1y")

def compare_competitors(ticker, competitors):
    comparison = {}
    target_stock = yf.Ticker(ticker)
    comparison[ticker] = {
        'PE Ratio': target_stock.info.get('trailingPE'),
        'Market Cap': target_stock.info.get('marketCap'),
        'Dividend Yield': target_stock.info.get('dividendYield')
    }
    for comp in competitors:
        comp_stock = yf.Ticker(comp)
        comparison[comp] = {
            'PE Ratio': comp_stock.info.get('trailingPE'),
            'Market Cap': comp_stock.info.get('marketCap'),
            'Dividend Yield': comp_stock.info.get('dividendYield')
        }
    return pd.DataFrame(comparison)

def analyze_investment_strategy(investment_strategy):
    """
    Uses OpenAI's ChatCompletion API to analyze the user's investment strategy
    and provide recommendations.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Initialize the client
    prompt = (
        "Please analyze the following investment strategy and provide recommendations "
        "on potential improvements, portfolio balancing, and risk considerations:\n\n"
        f"{investment_strategy}\n\nAnalysis:"
    )
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a knowledgeable financial advisor."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7,
        )
        analysis = response.choices[0].message.content.strip()
        return analysis
    except Exception as e:
        return f"Failed to analyze strategy: {e}"

def get_recommendations(risk_level, investment_duration, investment_strategy, custom_tickers):
    try:
        # Default tickers based on risk level.
        default_tickers = {
            "Low": ["VOO", "SCHD", "JNJ", "PG", "KO"],
            "Medium": ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"],
            "High": ["ARKK", "SQ", "PLTR", "NIO", "BTC-USD"]
        }
        # Start with defaults based on the selected risk level.
        recommended_tickers = set(default_tickers.get(risk_level, []))
        
        # Adjust recommendations based on investment strategy keywords.
        strat_lower = investment_strategy.lower()
        if "value" in strat_lower:
            recommended_tickers.update(["BRK-B", "JNJ"])
        if "growth" in strat_lower:
            recommended_tickers.update(["AMZN", "NFLX", "TSLA"])
        if "dividend" in strat_lower:
            recommended_tickers.update(["KO", "PG", "T"])
        
        # Incorporate user-provided tickers.
        if custom_tickers:
            user_tickers = [t.strip().upper() for t in custom_tickers.split(",") if t.strip()]
            recommended_tickers.update(user_tickers)
        
        # Build the recommendation list with additional stock details.
        recommendations_list = []
        for ticker in recommended_tickers:
            stock = yf.Ticker(ticker)
            info = stock.info
            recommendations_list.append({
                "Ticker": ticker,
                "Company Name": info.get('longName', 'N/A'),
                "PE Ratio": info.get('trailingPE', 'N/A'),
                "Dividend Yield": info.get('dividendYield', 'N/A'),
                "Market Cap": info.get('marketCap', 'N/A'),
                "Investment Strategy": investment_strategy
            })
        return pd.DataFrame(recommendations_list)
    except Exception as e:
        return f"Failed to generate recommendations: {e}"

def run_simulation(investment_amount, investment_period, risk_level, investment_strategy):
    try:
        # Map risk levels to a continuous base factor.
        risk_map = {"Low": 0.8, "Medium": 1.0, "High": 1.2}
        base_risk = risk_map.get(risk_level, 1.0)
        
        # Adjust strategy factor based on keywords in the investment strategy.
        strat_factor = 1.0
        strategy_lower = investment_strategy.lower()
        if "growth" in strategy_lower:
            strat_factor *= 1.2  # Growth strategies aim for higher returns.
        if "value" in strategy_lower:
            strat_factor *= 0.9  # Value strategies tend to be more conservative.
        if "dividend" in strategy_lower:
            strat_factor *= 0.85  # Dividend-focused strategies may be more stable.
        
        total_factor = base_risk * strat_factor
        
        # Determine the annual return using a continuous model.
        annual_return_mean = 6.0 + (total_factor - 1.0) * 4.0
        annual_return_std = 2.0 * total_factor
        annual_return = np.random.normal(annual_return_mean, annual_return_std)
        
        # Determine maximum drawdown in a similar manner.
        max_drawdown_mean = 10.0 + (total_factor - 1.0) * 15.0
        max_drawdown_std = 5.0 * total_factor
        max_drawdown = np.random.normal(max_drawdown_mean, max_drawdown_std)
        
        # Calculate the total return over the investment period using compound interest.
        years = investment_period / 12.0
        total_return_value = investment_amount * ((1 + annual_return/100) ** years - 1)
        
        simulation_results = {
            "Investment Amount (USD)": investment_amount,
            "Investment Period (Months)": investment_period,
            "Estimated Annual Return (%)": round(annual_return, 2),
            "Estimated Max Drawdown (%)": round(max_drawdown, 2),
            "Total Return over Period (USD)": round(total_return_value, 2)
        }
        return pd.DataFrame(simulation_results, index=[0])
    except Exception as e:
        return f"Failed to run simulation: {e}"

def generate_report(ticker, competitors, risk_level, investment_strategy):
    try:
        # Get competitor comparison.
        comparison_df = compare_competitors(ticker, competitors)
        
        # Helper: format individual values.
        def format_value(key, value):
            try:
                if pd.isna(value):
                    return "N/A"
            except Exception:
                pass
            if key == "PE Ratio":
                return f"{value:,.2f}"
            elif key == "Dividend Yield":
                return f"{value*100:.2f}%" if value is not None else "N/A"
            elif key == "Market Cap":
                if value is None:
                    return "N/A"
                if value >= 1e12:
                    return f"${value/1e12:,.2f}T"
                elif value >= 1e9:
                    return f"${value/1e9:,.2f}B"
                elif value >= 1e6:
                    return f"${value/1e6:,.2f}M"
                else:
                    return f"${value:,.2f}"
            else:
                if isinstance(value, (int, float)):
                    return f"{value:,.2f}"
                else:
                    return str(value)
        
        # Format the entire DataFrame.
        formatted_df = comparison_df.copy()
        for col in comparison_df.columns:
            formatted_df[col] = comparison_df[col].apply(lambda x: format_value(col, x))
        
        # Create a Markdown table from the DataFrame.
        md_table = formatted_df.to_markdown()
        
        # Get target metrics for the analyzed ticker.
        target_pe = format_value("PE Ratio", comparison_df.loc["PE Ratio", ticker])
        target_dividend = format_value("Dividend Yield", comparison_df.loc["Dividend Yield", ticker])
        
        # Build a formatted Markdown report.
        report_md = f"""
### Investment Analysis Report for {ticker}

**Competitor Comparison:**

{md_table}

**Summary:**
- **Risk Level:** {risk_level}
- **Investment Strategy:** {investment_strategy}

**Key Metrics for {ticker}:**
- **PE Ratio:** {target_pe}
- **Dividend Yield:** {target_dividend}

> **Note:** Higher risk investments may yield higher returns but can also experience larger drawdowns. Further detailed analysis is advised.
        """
        return report_md, formatted_df
    except Exception as e:
        return None, f"Failed to generate report: {e}"
