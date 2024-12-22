import time

from nxs_python.testing.pytest_runner import PytestRunner
from typing import List


class TestPytestRunner():
    def __init__(self):
        self.runner = PytestRunner(self.test_callback)

    def discover_and_run(self):
        # Discover tests (blocks until discovery is complete)
        test_dir = "./rpi_final_acceptance_test/tests"
        discovered_tests = self.runner.discover_tests(test_dir)
        print(f"Discovered Tests: {discovered_tests}")

        # Start tests (after discovery completes)
        self.runner.start_tests([f'{test_dir}/test_sample_application.py::test_version', f'{test_dir}/test_sample_application.py::test_sensor_failing'], {'firmware_version': '1.2.3'})
        time.sleep(4)
        self.runner.stop_tests()          

    def test_callback(self, message: dict):
        if message.get('reason') == 'running':
            print(f"{message['timestamp']}: Running test {message['current_index']}/{message['total_tests']}: {message['test_name']}")
        elif message.get('reason') == 'completed':
            print(f"{message['timestamp']}: Test {message['test_name']} finished with result: {message}")
        elif message.get('reason') == 'error':
            print(f"{message['timestamp']}: Error: {message['stderror']}")
        elif message.get('reason') == 'cancelled':
            print(f"{message['timestamp']}: Test run was cancelled.")
        elif message.get('reason') == 'log':
                print(f"{message['timestamp']}: {message['stdout']}")

if __name__ == "__main__":
    test_runner = TestPytestRunner()
    test_runner.discover_and_run()