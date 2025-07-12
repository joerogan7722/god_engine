import unittest
import time
from god_engine.system_monitor import SystemMonitor

class TestSystemMonitor(unittest.TestCase):

    def setUp(self):
        self.monitor = SystemMonitor()

    def test_log_error(self):
        self.monitor.log_error("test_module")
        self.assertEqual(self.monitor.error_counts["test_module"], 1)
        self.monitor.log_error("test_module")
        self.assertEqual(self.monitor.error_counts["test_module"], 2)

    def test_record_function_timing(self):
        self.monitor.record_function_timing("test_func", 0.1)
        self.assertEqual(self.monitor.function_timings["test_func"], [0.1])
        self.monitor.record_function_timing("test_func", 0.2)
        self.assertEqual(self.monitor.function_timings["test_func"], [0.1, 0.2])

    def test_get_error_rates(self):
        self.monitor.log_error("module_a")
        self.monitor.log_error("module_b")
        self.monitor.log_error("module_a")
        rates = self.monitor.get_error_rates()
        self.assertEqual(rates["module_a"], 2)
        self.assertEqual(rates["module_b"], 1)

    def test_get_performance_bottlenecks(self):
        self.monitor.record_function_timing("fast_func", 0.01)
        self.monitor.record_function_timing("slow_func", 0.5)
        self.monitor.record_function_timing("medium_func", 0.1)
        bottlenecks = self.monitor.get_performance_bottlenecks(top_n=2)
        self.assertEqual(len(bottlenecks), 2)
        self.assertEqual(bottlenecks[0][0], "slow_func")
        self.assertAlmostEqual(bottlenecks[0][1], 0.5)

    def test_time_function_decorator(self):
        @self.monitor.time_function
        def my_test_function():
            time.sleep(0.01)
            return "done"

        result = my_test_function()
        self.assertEqual(result, "done")
        self.assertIn("my_test_function", self.monitor.function_timings)
        self.assertGreater(self.monitor.function_timings["my_test_function"][0], 0.0)

if __name__ == '__main__':
    unittest.main()
