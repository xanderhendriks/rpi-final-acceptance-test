import logging
import time
import re


def test_version(serial_command_response, firmware_version):
    """
    Check the version
    """
    pattern = r"image_id:\s*(\d+),\s*version:\s*(\d+\.\d+\.\d+)-([a-f0-9]+)"

    serial_command_response.command('v')
    response = serial_command_response.response()

    print(f'response: {response}')

    match = re.search(pattern, response)

    assert match, "Can't read the image id and version"
    assert match.group(1) == '1', 'Incorrect image ID'

    if 'dev' in firmware_version:
        assert match.group(2) == '0.0.0', 'Incorrect version'
        assert match.group(3) == firmware_version.split('-')[0], 'Incorrect githash'
    else:
        assert match.group(2) == firmware_version, 'Incorrect version'


def test_sensor(serial_command_response):
    """
    Test the sensor output
    """
    serial_command_response.command('s')
    response = serial_command_response.response()

    print(f'response: {response}')

    assert response == 'sensor: 65535'


def test_sensor_failing(serial_command_response):
    """
    Test the sensor output
    """
    serial_command_response.command('s')
    response = serial_command_response.response()

    print(f'response: {response}')

    assert response == 'sensor: 0', 'Replace sensor'
