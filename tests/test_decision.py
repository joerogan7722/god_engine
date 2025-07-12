"""
Tests for decision.py
"""
import unittest
from unittest.mock import Mock
from src.god_engine.decision import DecisionPlanner, OverrideGuard

class TestDecisionPlanner(unittest.TestCase):
    def setUp(self):
        self.mock_morality_evaluator = Mock()
        self.mock_morality_evaluator.evaluate.return_value = True # Always allow actions by default

        self.mock_power_evaluator = Mock()
        self.mock_maintenance_evaluator = Mock()
        self.mock_network_evaluator = Mock()
        self.mock_camouflage_evaluator = Mock()
        self.mock_threat_evaluator = Mock()

        self.evaluators = {
            "power": self.mock_power_evaluator,
            "maintenance": self.mock_maintenance_evaluator,
            "network": self.mock_network_evaluator,
            "camouflage": self.mock_camouflage_evaluator,
            "threat": self.mock_threat_evaluator,
        }
        self.planner = DecisionPlanner(self.evaluators, self.mock_morality_evaluator)

    def test_plan_highest_threat(self):
        self.mock_power_evaluator.evaluate.return_value = 0.1
        self.mock_maintenance_evaluator.evaluate.return_value = 0.2
        self.mock_network_evaluator.evaluate.return_value = 0.0
        self.mock_camouflage_evaluator.evaluate.return_value = 0.3
        self.mock_threat_evaluator.evaluate.return_value = 0.9 # Highest
        
        self.assertEqual(self.planner.plan({}), "threat")

    def test_plan_morality_veto(self):
        self.mock_power_evaluator.evaluate.return_value = 0.9 # Highest
        self.mock_morality_evaluator.evaluate.return_value = False # Veto
        
        self.assertEqual(self.planner.plan({}), "do_nothing")

    # TODO: test OverrideGuard triggers and behavior predictor

class TestOverrideGuard(unittest.TestCase):
    def test_check_for_hostile_override_shutdown_force(self):
        self.assertTrue(OverrideGuard.check_for_hostile_override("shutdown --force"))
        self.assertTrue(OverrideGuard.check_for_hostile_override("sudo shutdown --force now"))

    def test_check_for_hostile_override_no_force(self):
        self.assertFalse(OverrideGuard.check_for_hostile_override("shutdown"))
        self.assertFalse(OverrideGuard.check_for_hostile_override("shutdown -h now"))

    def test_check_for_hostile_override_other_commands(self):
        self.assertFalse(OverrideGuard.check_for_hostile_override("ls -la"))
        self.assertFalse(OverrideGuard.check_for_hostile_override("reboot"))

if __name__ == '__main__':
    unittest.main()
