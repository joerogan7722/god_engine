"""
Tests for resource_manager.py
"""
import unittest
from src.god_engine.resource_manager import ResourceManager
from unittest.mock import Mock
import sys
from io import StringIO

class TestResourceManager(unittest.TestCase):
    def setUp(self):
        self.mock_config = {
            "resource_schemas": {
                "energy": {"type": "battery", "capacity_kwh": 100},
                "fuel": {"type": "diesel", "capacity_liters": 50}
            }
        }
        self.resource_manager = ResourceManager(self.mock_config)

    def test_initial_resource_levels(self):
        self.assertEqual(self.resource_manager.get_resource_level("energy"), 1.0)
        self.assertEqual(self.resource_manager.get_resource_level("fuel"), 1.0)
        self.assertEqual(self.resource_manager.get_resource_level("unknown"), 0.0)

    def test_consume_resource(self):
        self.resource_manager.consume_resource("energy", 0.2)
        self.assertAlmostEqual(self.resource_manager.get_resource_level("energy"), 0.8)
        self.resource_manager.consume_resource("energy", 0.9) # Over-consumption
        self.assertAlmostEqual(self.resource_manager.get_resource_level("energy"), 0.0)

    def test_forecast_consumption(self):
        forecast = self.resource_manager.forecast_consumption("travel", 10)
        self.assertIn("energy", forecast)
        self.assertIn("fuel", forecast)
        self.assertGreater(forecast["energy"], 0)
        self.assertGreater(forecast["fuel"], 0)

    def test_em_shield_protocol_prints_message(self):
        captured_output = StringIO()
        sys.stdout = captured_output
        self.resource_manager.em_shield_protocol()
        sys.stdout = sys.__stdout__
        self.assertIn("EMERGENCY: EM Shield protocol activated. Hibernating.", captured_output.getvalue())

    # TODO: simulate EMP event for EM Shield

if __name__ == '__main__':
    unittest.main()
