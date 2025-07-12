"""
Tests for replication.py
"""
import unittest
from src.god_engine.replication import ReplicationModule

class TestReplicationModule(unittest.TestCase):
    def setUp(self):
        self.mock_config = {
            "replication_profile": {
                "strategy": "stealth_drip",
                "target_os": ["linux", "windows"],
                "max_replication_depth": 5
            }
        }
        self.replication_module = ReplicationModule(self.mock_config)

    def test_can_replicate_supported_os(self):
        target_host_linux = {"os": "linux", "ip": "192.168.1.1"}
        target_host_windows = {"os": "windows", "ip": "192.168.1.2"}
        self.assertTrue(self.replication_module.can_replicate(target_host_linux))
        self.assertTrue(self.replication_module.can_replicate(target_host_windows))

    def test_can_replicate_unsupported_os(self):
        target_host_macos = {"os": "macos", "ip": "192.168.1.3"}
        self.assertFalse(self.replication_module.can_replicate(target_host_macos))

    def test_replicate_supported_os(self):
        target_host_linux = {"os": "linux", "ip": "192.168.1.1"}
        self.assertTrue(self.replication_module.replicate(target_host_linux))

    def test_replicate_unsupported_os(self):
        target_host_macos = {"os": "macos", "ip": "192.168.1.3"}
        self.assertFalse(self.replication_module.replicate(target_host_macos))

    # TODO: verify stealth firmware drip replication

if __name__ == '__main__':
    unittest.main()
