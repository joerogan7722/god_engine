"""
Tests for policy/maintenance.py
"""
import unittest
from unittest.mock import Mock
from src.god_engine.policy.maintenance import MaintenanceEvaluator

class TestMaintenanceEvaluator(unittest.TestCase):
    def setUp(self):
        self.mock_hardware_interface = Mock()
        self.maintenance_evaluator = MaintenanceEvaluator(self.mock_hardware_interface)

    def test_evaluate_perfect_health(self):
        self.mock_hardware_interface.get_health_summary.return_value = {"comp1": 1.0, "comp2": 1.0}
        self.assertEqual(self.maintenance_evaluator.evaluate(), 0.0)

    def test_evaluate_some_damage(self):
        self.mock_hardware_interface.get_health_summary.return_value = {"comp1": 0.5, "comp2": 1.0}
        self.assertEqual(self.maintenance_evaluator.evaluate(), 0.25)

    def test_evaluate_critical_damage(self):
        self.mock_hardware_interface.get_health_summary.return_value = {"comp1": 0.0, "comp2": 0.0}
        self.assertEqual(self.maintenance_evaluator.evaluate(), 1.0)

    def test_evaluate_empty_health_summary(self):
        self.mock_hardware_interface.get_health_summary.return_value = {}
        self.assertEqual(self.maintenance_evaluator.evaluate(), 0.0)

    def test_evaluate_mixed_health(self):
        self.mock_hardware_interface.get_health_summary.return_value = {"comp1": 0.8, "comp2": 0.2, "comp3": 1.0}
        # (1.0 - (0.8 + 0.2 + 1.0) / 3) = (1.0 - 2.0/3) = 1.0 - 0.666... = 0.333...
        self.assertAlmostEqual(self.maintenance_evaluator.evaluate(), 1/3)

if __name__ == '__main__':
    unittest.main()
