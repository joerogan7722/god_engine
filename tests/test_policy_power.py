"""
Tests for policy/power.py
"""
import unittest
from unittest.mock import Mock
from src.god_engine.policy.power import PowerEvaluator

class TestPowerEvaluator(unittest.TestCase):
    def setUp(self):
        self.mock_resource_manager = Mock()
        self.power_evaluator = PowerEvaluator(self.mock_resource_manager)

    def test_evaluate_full_resources(self):
        self.mock_resource_manager.get_resource_level.side_effect = [1.0, 1.0] # Energy, Fuel
        self.assertEqual(self.power_evaluator.evaluate(), 0.0)

    def test_evaluate_empty_resources(self):
        self.mock_resource_manager.get_resource_level.side_effect = [0.0, 0.0] # Energy, Fuel
        self.assertEqual(self.power_evaluator.evaluate(), 1.0)

    def test_evaluate_mixed_resources(self):
        self.mock_resource_manager.get_resource_level.side_effect = [0.5, 1.0] # Energy, Fuel
        self.assertEqual(self.power_evaluator.evaluate(), 0.25)

    def test_evaluate_different_mixed_resources(self):
        self.mock_resource_manager.get_resource_level.side_effect = [0.2, 0.8] # Energy, Fuel
        # (1-0.2 + 1-0.8) / 2 = (0.8 + 0.2) / 2 = 1.0 / 2 = 0.5
        self.assertEqual(self.power_evaluator.evaluate(), 0.5)

if __name__ == '__main__':
    unittest.main()
