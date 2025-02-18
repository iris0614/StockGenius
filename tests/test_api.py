import unittest
import pandas as pd
from app.api import get_recommendations, run_simulation, analyze_investment_strategy, generate_report

class TestAPI(unittest.TestCase):
    def test_get_recommendations(self):
        # Test using a mix of default and custom tickers with a growth-oriented strategy.
        recs = get_recommendations("Medium", "Long-term", "Growth Investing", "AAPL, MSFT, GOOGL")
        self.assertIsInstance(recs, pd.DataFrame)
        self.assertIn("Ticker", recs.columns)
    
    def test_run_simulation(self):
        simulation = run_simulation(1000, 36, "Medium", "Growth Investing")
        self.assertIsInstance(simulation, pd.DataFrame)
        self.assertIn("Estimated Annual Return (%)", simulation.columns)
    
    def test_analyze_investment_strategy(self):
        analysis = analyze_investment_strategy("I want to focus on growth stocks and emerging technologies while maintaining a balanced risk.")
        self.assertIsInstance(analysis, str)
        self.assertGreater(len(analysis), 0)
    
    def test_generate_report(self):
        report_md, df = generate_report("AAPL", ["MSFT", "GOOGL", "AMZN"], "Low", "Conservative, long term (more than 5 years)")
        self.assertIsInstance(report_md, str)
        self.assertIn("Investment Analysis Report for AAPL", report_md)

if __name__ == '__main__':
    unittest.main()
