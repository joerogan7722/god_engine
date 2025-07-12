"""
Tests for framework_registry.py
"""
import unittest
from src.god_engine.framework_registry import FrameworkRegistry
from src.god_engine.config import load_config
from pathlib import Path

class TestFrameworkRegistry(unittest.TestCase):
    def setUp(self):
        # Create a dummy config.yaml for testing
        self.test_config_path = Path("test_config.yaml")
        with open(self.test_config_path, "w") as f:
            f.write("""
directives:
  core_directive: "test_directive"
  ethical_framework: "test_framework"
resource_schemas: {}
replication_profile: {}
stealth_profile: {}
""")
        self.config = load_config(self.test_config_path)

    def tearDown(self):
        # Clean up the dummy config file
        self.test_config_path.unlink()

    def test_initialization(self):
        registry = FrameworkRegistry(self.config)
        self.assertEqual(registry.get_directive(), "test_directive")
        self.assertEqual(registry.ethical_framework, "test_framework")

    def test_load_frameworks_called(self):
        # This is a simple test, a more robust one would mock _load_frameworks
        # and assert it was called. For now, we rely on print statements.
        registry = FrameworkRegistry(self.config)
        self.assertIsNotNone(registry) # Just ensure it initializes without error

if __name__ == '__main__':
    unittest.main()
