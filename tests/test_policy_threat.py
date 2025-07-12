"""
Tests for policy/threat.py
"""
import unittest
from unittest.mock import Mock
from src.god_engine.policy.threat import ThreatEvaluator

class TestThreatEvaluator(unittest.TestCase):
    def setUp(self):
        self.mock_threat_detector = Mock()
        self.threat_evaluator = ThreatEvaluator(self.mock_threat_detector)

    def test_evaluate_no_threats(self):
        self.mock_threat_detector.scan_for_threats.return_value = {}
        self.assertEqual(self.threat_evaluator.evaluate(), 0.0)

    def test_evaluate_single_threat(self):
        self.mock_threat_detector.scan_for_threats.return_value = {"emp": 0.5}
        self.assertEqual(self.threat_evaluator.evaluate(), 0.5)

    def test_evaluate_multiple_threats(self):
        self.mock_threat_detector.scan_for_threats.return_value = {"emp": 0.3, "capture": 0.4, "physical": 0.1}
        self.assertEqual(self.threat_evaluator.evaluate(), 0.8)

    def test_evaluate_threats_exceeding_one(self):
        self.mock_threat_detector.scan_for_threats.return_value = {"emp": 0.8, "capture": 0.5}
        self.assertEqual(self.threat_evaluator.evaluate(), 1.0) # Should be capped at 1.0

if __name__ == '__main__':
    unittest.main()
