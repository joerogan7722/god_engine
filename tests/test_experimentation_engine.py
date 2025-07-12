import unittest
import os
import json
from god_engine.experimentation_engine import ExperimentationEngine
from god_engine.system_monitor import SystemMonitor

class TestExperimentationEngine(unittest.TestCase):

    def setUp(self):
        self.code_root = os.path.abspath(os.path.dirname(__file__))
        self.goals_config_path = os.path.join(self.code_root, "temp_goals.json")
        self.system_monitor = SystemMonitor()
        
        with open(self.goals_config_path, "w") as f:
            json.dump({}, f)
            
        self.exp_engine = ExperimentationEngine(
            self.code_root, self.goals_config_path, self.system_monitor
        )

    def tearDown(self):
        if os.path.exists(self.goals_config_path):
            os.remove(self.goals_config_path)

    def test_generate_goal_from_hypothesis(self):
        hypothesis = {
            "name": "test_hypothesis",
            "description": "A test hypothesis",
            "target_file": "test.py",
            "patch_logic": "pass",
            "completion_criteria": "pass",
            "priority": 1,
            "effort": 1,
            "validation_command": "pytest",
            "capability": "test_capability"
        }
        
        self.exp_engine.generate_goal_from_hypothesis(hypothesis, "10.0%")

        with open(self.goals_config_path, "r") as f:
            goals = json.load(f)
        
        self.assertIn("test_hypothesis", goals)
        self.assertEqual(goals["test_hypothesis"]["description"], "A test hypothesis")
        self.assertEqual(goals["test_hypothesis"]["associated_capability"], "test_capability")
        self.assertEqual(goals["test_hypothesis"]["experiment_summary"]["performance_gain"], "10.0%")

if __name__ == '__main__':
    unittest.main()
