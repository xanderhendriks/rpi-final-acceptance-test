import logging

file_logging = logging.getLogger()


def test_show_operator_and_serial_number(operator_name, board_serial_number):
    file_logging.info(f'Operator: {operator_name}')
    file_logging.info(f'Serial number: {board_serial_number}')
    print(f'Operator: {operator_name}')
    print(f'Serial number: {board_serial_number}')
    # This test case could be used to program the serial number in the device
