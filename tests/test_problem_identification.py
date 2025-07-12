import unittest
import os
import json
from god_engine.problem_identification import ProblemIdentificationModule
from god_engine.system_monitor import SystemMonitor

class TestProblemIdentificationModule(unittest.TestCase):

    def setUp(self):
        self.code_root = os.path.abspath(os.path.dirname(__file__))
        self.goals_config_path = os.path.join(self.code_root, "temp_goals.json")
        self.system_monitor = SystemMonitor()
        
        # Create a dummy goals file
        with open(self.goals_config_path, "w") as f:
            json.dump({}, f)
            
        self.problem_identifier = ProblemIdentificationModule(
            self.code_root, self.goals_config_path, self.system_monitor
        )

    def tearDown(self):
        if os.path.exists(self.goals_config_path):
            os.remove(self.goals_config_path)

    def test_generate_new_goal(self):
        new_goal = {
            "name": "test_goal",
            "description": "A test goal",
            "target_file": "test.py",
            "patch_logic": "pass",
            "completion_criteria": "pass",
            "priority": 1,
            "effort": 1,
            "validation_command": "pytest"
        }
        self.problem_identifier.generate_new_goal(new_goal)

        with open(self.goals_config_path, "r") as f:
            goals = json.load(f)
        
        self.assertIn("test_goal", goals)
        self.assertEqual(goals["test_goal"]["description"], "A test goal")

    def test_generate_existing_goal(self):
        existing_goal = {
            "name": "existing_goal",
            "description": "An existing goal",
            "target_file": "test.py",
            "patch_logic": "pass",
            "completion_criteria": "pass",
            "priority": 1,
            "effort": 1,
            "validation_command": "pytest"
        }
        
        with open(self.goals_config_path, "w") as f:
            json.dump({"existing_goal": existing_goal}, f)

        self.problem_identifier.generate_new_goal(existing_goal)
        
        # Should not raise an error and should not modify the file
        with open(self.goals_config_path, "r") as f:
            goals = json.load(f)
        
        self.assertEqual(len(goals), 1)

if __name__ == '__main__':
    unittest.main()
