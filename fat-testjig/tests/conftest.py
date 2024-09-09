import datetime
import logging
import os
import pytest
import subprocess
import yaml


pytest_logging = logging.getLogger('pytest_logging')


# def program_stm32_flash(binary_file):
#     command = [
#         'openocd',
#         '-f', 'interface/stlink.cfg',
#         '-f', 'target/stm32f3x.cfg',
#         '-c', f'program {binary_file} verify reset exit 0x8000000'
#     ]

#     subprocess.check_output(command, stderr=subprocess.STDOUT)


# @pytest.fixture(scope="session", autouse=True)
# def jig(jig_config):
#     filename = f"sample_application-{jig_config['firmware']['version']}.bin"
#     pytest_logging.info(f'Programming target with {filename}')
#     program_stm32_flash(f"{os.path.dirname(os.path.realpath(__file__))}/../../files/firmware/{filename}")
#     yield
#     pytest_logging.info('teardown')


# @pytest.fixture(scope="session")
# def jig_config(pytestconfig):
#     with open(pytestconfig.getoption("--config"), 'r') as file:
#         jig_config = yaml.safe_load(file)
#     return jig_config


# @pytest.fixture(scope="session")
# def version_to_check(jig_config):
#     return jig_config['firmware']['version']


# @pytest.fixture(scope="session")
# def git_hash_to_check(jig_config):
#     return jig_config['firmware']['git_hash']


# @pytest.fixture(scope="session")
# def board_serial_number(pytestconfig):
#     return pytestconfig.getoption("--board-serial-number")


# @pytest.fixture(scope="session")
# def operator_name(pytestconfig):
#     return pytestconfig.getoption("--operator-name")


# @pytest.fixture(scope="function", autouse=True)
# def log_test_start(request):
#     pytest_logging.info('=' * 5 + request.node.name.ljust(70, '='))
#     pytest_logging.info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


# def pytest_addoption(parser):
#     parser.addoption("--board-serial-number", action="store", default="XXXXXXXXXX")
#     parser.addoption("--operator-name", action="store")
#     parser.addoption("--config", action="store", default=os.path.join(os.path.dirname(os.path.abspath(__file__)),
#                                                                       "config_testjig.yml"))
