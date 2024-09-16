import asyncio
import os
import pytest
import re
import yaml

from nicegui import app, ui, events
from .local_file_picker import LocalFilePicker
from .version import version
from starlette.formparsers import MultiPartParser
from collections import defaultdict

MultiPartParser.max_file_size = 1024 * 1024 * 10  # 10 MB

local_file_picker = None
test_results_table = None
test_cases_tree = None
selected_test_cases = []
st_link_port = None
stepper = None

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
    pytest_args = []

    for test in tests:
        pytest_args += [f'{os.path.dirname(os.path.abspath(__file__))}/{test}']

    print(pytest_args)

    await asyncio.sleep(2)

    return pytest.main(pytest_args)

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

def on_tick_test_cases(event):
    global selected_test_cases
    selected_test_cases = event.value

async def execute_tests():
    stepper.next()
    test_results_table.style("background-color: white")

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
    print(e.client)
    files = await local_file_picker.get_selected_files()
    for file in files:
        print(file)
        ui.download(file)

def handle_upload(event: events.UploadEventArguments) -> None:
    wheel_pattern = r'^rpi_final_acceptance_test-(\d+\.\d+(\.\d+)?(\.dev\d+)?)-py3-none-any\.ewhl$'
    firmware_image_pattern = r'^sample_application-(\d+\.\d+\.\d+|[a-f0-9]{7,}-dev)\.bin$'

    for pattern in [wheel_pattern, firmware_image_pattern]:
        if re.match(pattern, event.name):
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

    with ui.header().classes(replace='row items-center') as header:
        with ui.tabs() as tabs:
            ui.tab('Test')
            ui.tab('Maintenance')

    with ui.tab_panels(tabs, value='Test').classes('w-full'):
        with ui.tab_panel('Test'):
            with ui.stepper().props('vertical').classes('w-full') as stepper:
                with ui.step('Test data'):
                    ui.input(label='Operator').props('rounded outlined dense')
                    with ui.stepper_navigation():
                        ui.button('Next', on_click=stepper.next)
                        ui.button('Back', on_click=stepper.previous)
                with ui.step('Device data'):
                    ui.input(label='Revision').props('rounded outlined dense')
                    ui.input(label='Serial number').props('rounded outlined dense')
                    with ui.stepper_navigation():
                        ui.button('Next', on_click=stepper.next)
                        ui.button('Back', on_click=stepper.previous)
                with ui.step('Select tests'):
                    test_cases_tree = ui.tree(test_cases_tree_list, tick_strategy='leaf', on_tick=on_tick_test_cases)
                    test_cases_tree.expand(['test cases'])
                    with ui.stepper_navigation():
                        ui.button('Next', on_click=lambda: execute_tests())
                        ui.button('Back', on_click=stepper.previous)
                with ui.step('Execute tests'):
                    columns = [
                        {'name': 'test_case', 'label': 'Test case', 'field': 'test_case', 'required': True, 'align': 'left'},
                        {'name': 'result', 'label': 'Result', 'field': 'result', 'sortable': True},
                    ]
                    test_results_table = ui.table(columns=columns, rows=[], row_key='name')
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
                    ui.label(f'version: {version}')
                    ui.upload(auto_upload=True, label='Upload update file', on_upload=handle_upload).classes('max-w-full')
                    ui.button('Restart', on_click=app.shutdown)

                with ui.tab_panel('Configuration'):
                    st_link_port = ui.input(label='ST link port', value=configuration['st_link_port']).props('rounded outlined dense')
                    with ui.row():
                        ui.button('Save', on_click=lambda: save_configuration())

ui.run()
