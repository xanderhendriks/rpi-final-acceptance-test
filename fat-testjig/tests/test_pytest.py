import logging

pytest_logging = logging.getLogger('pytest_logging')


def test_show_operator_and_serial_number(operator_name, board_serial_number):
    pytest_logging.info(f'Operator: {operator_name}')
    pytest_logging.info(f'Serial number: {board_serial_number}')

    # This test case could be used to program the serial number in the device
