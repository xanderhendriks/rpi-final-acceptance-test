import pytest
import subprocess
import time

from pathlib import Path


@pytest.mark.order(1)
def test_program_firmware(firmware_version):
    # fw_file = Path(f'files/sample_application-{firmware_version}.bin')
    # programmed_OK = False

    # if fw_file.is_file():
    #     subprocess_output = subprocess.run([
    #         'openocd',
    #         '-f', 'interface/stlink.cfg',
    #         '-f', 'target/stm32f3x.cfg',
    #         '-c', f'program {fw_file} verify reset exit 0x8000000'
    #     ], capture_output=True, text=True)

    #     if subprocess_output.returncode == 0:
    #         programmed_OK = True
    #         output = 'Device programmed successfully'
    #     else:
    #         output = 'Error programming device'
    # else:
    #     output = 'Upload firmware first through Maintenance tab'

    # print(subprocess_output.stdout, subprocess_output.stderr)
    # assert programmed_OK, output
    print('test_program_firmware - start')
    time.sleep(1)
    print('test_program_firmware - end')


@pytest.mark.order(2)
def test_program_serial_number(board_serial_number):
    """
    This test case could be used to program the serial number in the device
    """
    # print(f'Serial number: {board_serial_number}')
    print('test_program_serial_number - start')
    time.sleep(1)
    print('test_program_serial_number - end')

