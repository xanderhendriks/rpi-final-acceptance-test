import asyncio
import io
import json
import logging
import os
import pytest
import re
import subprocess
import sys
import yaml

from .local_file_picker import LocalFilePicker
from .version import version
from datetime import datetime
from nicegui import app, ui, events
from starlette.formparsers import MultiPartParser
from nxs_python.utils.encrypt_decrypt import encrypt_file, key
from nxs_python.testing.pytest_ui import PytestUI
from pathlib import Path

logging_formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

file_logging_handler = logging.FileHandler(f'files/logs/{datetime.now().strftime("%Y-%m-%d")}.log', 'a')
file_logging_handler.setFormatter(logging_formatter)
std_err_logging_handler = logging.StreamHandler()
std_err_logging_handler.setFormatter(logging_formatter)

file_logging = logging.getLogger('main')
file_logging.setLevel(logging.INFO)
file_logging.addHandler(file_logging_handler)
file_logging.addHandler(std_err_logging_handler)

MultiPartParser.max_file_size = 1024 * 1024 * 10  # 10 MB

firmware_image_pattern = r'^sample_application-(\d+\.\d+\.\d+|[a-f0-9]{7,}-dev)\.bin$'
test_path = Path(__file__).parent / 'tests'

local_file_picker = None
test_results_table = None
test_cases_tree = None
selected_test_cases = []
st_link_port = None
stepper = None
firmware_version = '-.-.-'
firmware_version_label = None
operator = None
serial_number = None
test_results_log = None


def set_background(color: str) -> None:
    ui.query('body').style(f'background-color: {color}')

with open(f"{os.getcwd()}/configuration.yaml", 'r') as file:
    configuration = yaml.safe_load(file)

if configuration is None:
    configuration = {}

files = os.listdir('files')
for file in files:
    match = re.match(firmware_image_pattern, file)
    if match:
        firmware_version = match.group(1)

def save_configuration():
    configuration['st_link_port'] = st_link_port.value
    with open('configuration.yaml', 'w') as file:
        yaml.dump(configuration, file)


async def download_logs(e):
    file_logging.info(e.client)
    files = await local_file_picker.get_selected_files()
    for file in files:
        basename = Path(file).with_suffix('')
        encrypt_file(f'{basename}.log', f'{basename}.elog', key, os.urandom(16))
        file_logging.info(f'{basename}.elog')
        ui.download(f'{basename}.elog')


def handle_upload(event: events.UploadEventArguments) -> None:
    global firmware_version
    wheel_pattern = r'^rpi_final_acceptance_test-(\d+\.\d+(\.\d+)?(\.dev\d+)?)-py3-none-any\.ewhl$'

    for pattern in [wheel_pattern, firmware_image_pattern]:
        match = re.match(pattern, event.name)
        if match:
            if pattern == firmware_image_pattern:
                firmware_version = match.group(1)
                firmware_version_label.set_text(firmware_version)

            # Remove old image(s)
            files = os.listdir('files')
            for file in files:
                if re.match(pattern, file):
                    os.remove(f'files/{file}')

            # Save new one
            with open(f'files/{event.name}', 'wb') as downloaded_file:
                downloaded_file.write(event.content.read())

def pytest_callback(message: dict):
    if message.get('reason') == 'back':
        stepper.previous()
    elif message.get('reason') == 'done':
        stepper.set_value('Device data')


@ui.page('/')
def index():
    global local_file_picker
    global st_link_port
    global stepper
    global firmware_version_label
    global operator
    global serial_number
    global test_results_log

    with ui.header().classes(replace='row items-center') as header:
        with ui.tabs() as tabs:
            ui.tab('Test')
            ui.tab('Maintenance')

    with ui.tab_panels(tabs, value='Test').classes('w-full'):
        with ui.tab_panel('Test'):
            with ui.stepper().props('vertical').classes('w-full') as stepper:
                with ui.step('Test data'):
                    operator = ui.input(label='Operator').props('rounded outlined dense')
                    with ui.stepper_navigation():
                        ui.button('Next', on_click=stepper.next)
                        ui.button('Back', on_click=stepper.previous)
                with ui.step('Device data'):
                    ui.input(label='Revision').props('rounded outlined dense')
                    serial_number = ui.input(label='Serial number').props('rounded outlined dense')
                    with ui.stepper_navigation():
                        ui.button('Next', on_click=stepper.next)
                        ui.button('Back', on_click=stepper.previous)
                test_excution = PytestUI(stepper, test_path, pytest_callback)

        with ui.tab_panel('Maintenance'):
            with ui.tabs() as tabs:
                ui.tab('Logs')
                ui.tab('Update')
                ui.tab('Configuration')

            with ui.tab_panels(tabs, value='Logs').classes('w-[800px]'):
                with ui.tab_panel('Logs'):
                    local_file_picker = LocalFilePicker('files/logs', multiple=True).classes('w-full')
                    with ui.row():
                        ui.button('Download', on_click=download_logs)

                with ui.tab_panel('Update'):
                    with ui.card():
                        with ui.row():
                            ui.label('gui version:').tailwind.font_weight('extrabold')
                            ui.label(version)
                        with ui.row():
                            ui.label('firmware version:').tailwind.font_weight('extrabold')
                            firmware_version_label = ui.label(firmware_version)
                    ui.upload(auto_upload=True, label='Upload update file', on_upload=handle_upload).classes('max-w-full')
                    ui.button('Restart', on_click=app.shutdown)

                with ui.tab_panel('Configuration'):
                    st_link_port = ui.input(label='ST link port', value=configuration['st_link_port']).props('rounded outlined dense')
                    with ui.row():
                        ui.button('Save', on_click=lambda: save_configuration())

ui.run()
