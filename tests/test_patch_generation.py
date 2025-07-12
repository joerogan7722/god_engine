import unittest
import os
import json
from god_engine.patch_generation import PatchGenerationModule
from god_engine.goal_manager import Goal

class TestPatchGenerationModule(unittest.TestCase):

    def setUp(self):
        self.code_root = os.path.abspath(os.path.dirname(__file__))
        self.patch_generator = PatchGenerationModule(self.code_root)

    def test_generate_patch_from_goal(self):
        mock_goal = Goal(
            name="test_goal",
            description="A test goal",
            target_file="test.py",
            patch_logic="print('Hello, world!')",
            completion_criteria="print('Hello, world!')",
            priority=1,
            effort=1
        )
        
        generated_patch = self.patch_generator.generate_patch(mock_goal)
        self.assertEqual(generated_patch, "print('Hello, world!')")

if __name__ == '__main__':
    unittest.main()
