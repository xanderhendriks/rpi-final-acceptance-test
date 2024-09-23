import datetime
import logging
import serial
import time
import pytest

from threading import Thread


file_logging = logging.getLogger('main')


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
    return SerialCommandResponse(pytestconfig.getoption('--st-link-com-port'))


@pytest.fixture(scope="session")
def board_serial_number(pytestconfig):
    return pytestconfig.getoption("--board-serial-number")


@pytest.fixture(scope="session")
def operator_name(pytestconfig):
    return pytestconfig.getoption("--operator-name")


@pytest.fixture(scope="session")
def firmware_version(pytestconfig):
    return pytestconfig.getoption("--firmware-version")


@pytest.fixture(scope="function", autouse=True)
def log_test_start(request):
    file_logging.info('=' * 5 + request.node.name.ljust(70, '='))
    file_logging.info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


def pytest_addoption(parser):
    parser.addoption('--st-link-com-port', action='store')
    parser.addoption("--board-serial-number", action="store")
    parser.addoption("--operator-name", action="store")
    parser.addoption("--firmware-version", action="store")
