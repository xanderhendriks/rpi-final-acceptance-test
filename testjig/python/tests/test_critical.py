import logging
import pytest

pytest_logging = logging.getLogger('pytest_logging')


@pytest.mark.critical
def test_critical(operator_name, board_serial_number):
    pytest_logging.info(f'Operator: {operator_name}')
    pytest_logging.info(f'Serial number: {board_serial_number}')
