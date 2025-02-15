import unittest
from app.api import get_recommendations, run_simulation

class TestAPI(unittest.TestCase):
    def test_get_recommendations(self):
        recommendations = get_recommendations("中风险", "长期", "定投")
        self.assertIsInstance(recommendations, str)

    def test_run_simulation(self):
        simulation = run_simulation(1000, 36, "中风险")
        self.assertIsInstance(simulation, str)