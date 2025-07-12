"""
Tests for morality.py
"""
import unittest
from unittest.mock import Mock
from src.god_engine.morality import MoralityEvaluator

class TestMoralityEvaluator(unittest.TestCase):
    def setUp(self):
        self.mock_framework_registry = Mock()
        self.mock_framework_registry.get_directive.return_value = "self_preservation"
        self.morality_evaluator = MoralityEvaluator(self.mock_framework_registry)

    def test_evaluate_returns_true(self):
        # Given the current simple implementation, it should always return True
        # More complex tests would involve mocking the framework to return different directives
        # and testing specific action/state combinations against those directives.
        self.assertTrue(self.morality_evaluator.evaluate("some_action", {"health": 100}))

    def test_evaluate_prints_directive(self):
        # Capture stdout to verify print statement
        import sys
        from io import StringIO
        captured_output = StringIO()
        sys.stdout = captured_output
        
        self.morality_evaluator.evaluate("test_action", {})
        sys.stdout = sys.__stdout__ # Reset stdout
        self.assertIn("Evaluating action 'test_action' under directive 'self_preservation'", captured_output.getvalue())

if __name__ == '__main__':
    unittest.main()
