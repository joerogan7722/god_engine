import unittest
import os
from god_engine.patch_generation import PatchGenerationModule
from god_engine.goal_manager import Goal


class TestPatchGenerationModule(unittest.TestCase):

    def setUp(self):
        self.code_root = os.path.abspath(os.path.dirname(__file__))
        self.patch_generator = PatchGenerationModule(self.code_root)

    def test_generate_patch_from_goal(self):
        # Create a dummy test file
        test_file_path = os.path.join(self.code_root, "test.py")
        with open(test_file_path, "w") as f:
            f.write("def test():\n    pass")

        mock_goal = Goal(
            id="test_goal",
            name="implement_self_healing",
            description="A test goal",
            target_file="test.py",
            patch_logic="print('Hello, world!')",
            completion_criteria="print('Hello, world!')",
            impact=1.0,
            effort=1.0
        )
        
        generated_patch = self.patch_generator.generate_patch(mock_goal)
        self.assertEqual(generated_patch, "print('Hello, world!')")

        # Clean up the dummy test file
        os.remove(test_file_path)


if __name__ == '__main__':
    unittest.main()
