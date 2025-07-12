"""
Tests for policy/network.py
"""
import unittest
from unittest.mock import Mock
from src.god_engine.policy.network import NetworkEvaluator

class TestNetworkEvaluator(unittest.TestCase):
    def setUp(self):
        self.mock_network_scanner = Mock()
        self.network_evaluator = NetworkEvaluator(self.mock_network_scanner)

    def test_evaluate_no_vulnerable_nodes(self):
        self.mock_network_scanner.scan_for_vulnerable_nodes.return_value = []
        self.assertEqual(self.network_evaluator.evaluate(), 0)

    def test_evaluate_some_vulnerable_nodes(self):
        self.mock_network_scanner.scan_for_vulnerable_nodes.return_value = ["node1", "node2", "node3"]
        self.assertEqual(self.network_evaluator.evaluate(), 3)

    def test_evaluate_many_vulnerable_nodes(self):
        self.mock_network_scanner.scan_for_vulnerable_nodes.return_value = [f"node{i}" for i in range(10)]
        self.assertEqual(self.network_evaluator.evaluate(), 10)

if __name__ == '__main__':
    unittest.main()
