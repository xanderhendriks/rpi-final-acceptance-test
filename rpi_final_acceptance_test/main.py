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
from collections import defaultdict
from datetime import datetime
from nicegui import app, ui, events
from starlette.formparsers import MultiPartParser
from nxs_python.encrypt_decrypt import encrypt_file, key
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


def pytest_collect_tests(directory):
    """Collect pytest items using pytest's collection mechanism."""
    pytest_args = [directory, "--collect-only"]
    items = []

    # Run pytest's collection phase programmatically
    pytest.main(pytest_args, plugins=[TestCollectorPlugin(items)])

    return items


async def pytest_execute_tests(tests):
    pytest_args = [f'--st-link-com-port={st_link_port.value}', f'--firmware-version={firmware_version}', f'--operator-name={operator.value}' ,f'--board-serial-number={serial_number.value}', '--json-report', '-s', '-W', 'ignore:Module already imported:pytest.PytestWarning']

    for test in tests:
        pytest_args += [f'{os.path.dirname(os.path.abspath(__file__))}/{test}']

    file_logging.info(pytest_args)

    await asyncio.sleep(2)

    captured_output = io.StringIO()

    # Redirect sys.stdout to the StringIO object
    sys.stdout = captured_output

    try:
        result = pytest.main(pytest_args)
    finally:
        # Reset sys.stdout to its default value
        sys.stdout = sys.__stdout__

    # Get the output from the StringIO object
    output = captured_output.getvalue()

    with open('.report.json') as json_report_file:
        json_report = json.load(json_report_file)

    file_logging.info(output)
    if result != 0:
        result_string = json_report['tests'][0]['call']['crash']['message']
        match = re.search(r'AssertionError:\s*(.*?)\s*assert', result_string)
        if match:
            test_results_log.push(match.group(1))
        else:
            test_results_log.push(result_string)

    return result


class TestCollectorPlugin:
    """A pytest plugin to collect test items."""

    def __init__(self, items):
        self.items = items

    def pytest_collection_modifyitems(self, session, config, items):
        """Called after pytest has collected all items."""
        self.items.extend(items)


with open(f"{os.getcwd()}/configuration.yaml", 'r') as file:
    configuration = yaml.safe_load(file)

if configuration is None:
    configuration = {}

test_cases = pytest_collect_tests(f'{os.path.dirname(os.path.abspath(__file__))}/tests')

grouped_tests = defaultdict(list)
for test_case in test_cases:
    module_name = test_case.module.__name__
    test_name = test_case.name
    grouped_tests[module_name].append({'id': f'{module_name}.py::{test_name}', 'label': test_name})

test_cases_tree_list = [{'id': 'test cases', 'label': 'test cases', 'children': [{'id': module, 'label': module, 'children': children} for module, children in grouped_tests.items()]}]

files = os.listdir('files')
for file in files:
    match = re.match(firmware_image_pattern, file)
    if match:
        firmware_version = match.group(1)


def on_tick_test_cases(event):
    global selected_test_cases
    selected_test_cases = event.value


async def execute_tests():
    stepper.next()
    test_results_table.style("background-color: white")
    test_results_log.clear()

    rows = []
    for test_case in selected_test_cases:
        rows.append({'test_case': test_case, 'result': '-'})

    test_results_table.rows = rows

    end_result = 'Passed'
    for index, test_case in enumerate(selected_test_cases):
        if await pytest_execute_tests([f'tests/{test_case}']) == 0:
            rows[index]['result'] = 'Passed'
        else:
            rows[index]['result'] = 'Failed'
            end_result = 'Failed'
        test_results_table.update()

    test_results_table.style(f"background-color: {'green' if end_result == 'Passed' else 'red'}")


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

@ui.page('/')
def index():
    global local_file_picker
    global test_results_table
    global test_cases_tree
    global selected_test_cases
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
                with ui.step('Select tests'):
                    test_cases_tree = ui.tree(test_cases_tree_list, tick_strategy='leaf', on_tick=on_tick_test_cases)
                    test_cases_tree.expand(['test cases'])
                    with ui.stepper_navigation():
                        ui.button('Execute test', on_click=lambda: execute_tests())
                        ui.button('Back', on_click=stepper.previous)
                with ui.step('Execute tests'):
                    columns = [
                        {'name': 'test_case', 'label': 'Test case', 'field': 'test_case', 'required': True, 'align': 'left'},
                        {'name': 'result', 'label': 'Result', 'field': 'result', 'sortable': True},
                    ]
                    test_results_table = ui.table(columns=columns, rows=[], row_key='name')
                    test_results_log = ui.log().classes('max-w-full h-40')

                    with ui.stepper_navigation():
                        ui.button('Done', on_click=lambda: stepper.set_value('Device data'))
                        ui.button('Back', on_click=stepper.previous)

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
