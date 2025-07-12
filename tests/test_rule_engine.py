"""
Tests for rule_engine.py
"""
import unittest
from src.god_engine.rule_engine import PanicProtocol, DirectiveRuleEngine
import sys
from io import StringIO

class TestPanicProtocol(unittest.TestCase):
    def test_engage_prints_message(self):
        captured_output = StringIO()
        sys.stdout = captured_output
        PanicProtocol.engage("critical system failure")
        sys.stdout = sys.__stdout__
        self.assertIn("PANIC: Engaging lockdown due to critical system failure. Non-essential systems offline.", captured_output.getvalue())

class TestDirectiveRuleEngine(unittest.TestCase):
    def setUp(self):
        self.engine = DirectiveRuleEngine()

    def test_initialization(self):
        self.assertEqual(self.engine.rules, [])

    def test_load_rules_prints_message(self):
        captured_output = StringIO()
        sys.stdout = captured_output
        self.engine.load_rules("dummy_rules.txt")
        sys.stdout = sys.__stdout__
        self.assertIn("Loading directive rules from dummy_rules.txt", captured_output.getvalue())

    def test_evaluate_no_rules(self):
        self.assertIsNone(self.engine.evaluate({}))

    # TODO: add tests for HumanOverrideDisabler and PanicProtocol
    # These will require more complex mocks or a DSL for rules
    # For now, just placeholder tests for basic functionality.

if __name__ == '__main__':
    unittest.main()
