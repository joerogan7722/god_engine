"""
Tests for policy/camouflage.py
"""
import unittest
from unittest.mock import Mock
from src.god_engine.policy.camouflage import CamouflageEvaluator

class TestCamouflageEvaluator(unittest.TestCase):
    def setUp(self):
        self.mock_stealth_monitor = Mock()
        self.camouflage_evaluator = CamouflageEvaluator(self.mock_stealth_monitor)

    def test_evaluate_no_detection_risk(self):
        self.mock_stealth_monitor.get_current_detection_risk.return_value = 0.0
        self.assertEqual(self.camouflage_evaluator.evaluate(), 0.0)

    def test_evaluate_some_detection_risk(self):
        self.mock_stealth_monitor.get_current_detection_risk.return_value = 0.5
        self.assertEqual(self.camouflage_evaluator.evaluate(), 0.5)

    def test_evaluate_full_detection_risk(self):
        self.mock_stealth_monitor.get_current_detection_risk.return_value = 1.0
        self.assertEqual(self.camouflage_evaluator.evaluate(), 1.0)

    def test_evaluate_random_detection_risk(self):
        self.mock_stealth_monitor.get_current_detection_risk.return_value = 0.27
        self.assertEqual(self.camouflage_evaluator.evaluate(), 0.27)

if __name__ == '__main__':
    unittest.main()
