import datetime
import os
import serial
import time
import pytest

from threading import Thread


def pytest_collection_modifyitems(session, config, items):
    # Ensure that 'test_program_device.py' is executed first
    program_device_tests = []
    other_tests = []

    for item in items:
        if 'test_program.py' in item.nodeid:
            program_device_tests.append(item)
        else:
            other_tests.append(item)

    # Place 'test_program_device.py' items at the start
    items[:] = program_device_tests + other_tests


class SerialCommandResponse:
    def __init__(self, port):
        self.thread = None
        self.serial = serial.Serial(port, 9600, timeout=1)
        self.serial.read(1000)

    def command(self, command):
        self.response_string = None
        self.thread = Thread(target=self._process)
        self.thread.start()
        self.serial.write(command.encode())

    def response(self, timeout=0.5):
        start_time = time.time()
        while self.response_string is None and time.time() < (start_time + timeout):
            pass
        time.sleep(1)
        self.thread.join()
        return self.response_string

    def _process(self):
        """
        Process for reading the serial debug port
        """
        self.response_string = self.serial.readline().decode().rstrip()


@pytest.fixture(scope="session")
def serial_command_response(pytestconfig):
    # return SerialCommandResponse(os.environ.get('st-link-com-port'))
    print('serial_command_response fixture')
    return None


@pytest.fixture(scope="session")
def board_serial_number(pytestconfig):
    return os.environ.get("board-serial-number")


@pytest.fixture(scope="session")
def operator_name(pytestconfig):
    return os.environ.get("operator-name")


@pytest.fixture(scope="session")
def firmware_version(pytestconfig):
    return os.environ.get('firmware_version')
