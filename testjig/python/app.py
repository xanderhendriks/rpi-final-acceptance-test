#!/usr/bin/env python
import glob
import logging
import os
import pytest

from datetime import datetime
from flask import Flask, request, send_file
from flask_cors import CORS
from flask_sse import sse

from drivers.testjig.power_control import PowerControl
from utils.logging.redis_logging import RedisLoggingHandler

app = Flask(__name__, static_folder='/home/pi/rpi-final-acceptance-test/testjig/react-flask-app/build',
            static_url_path='/')
CORS(app)
app.config["REDIS_URL"] = "redis://localhost:6379"
app.register_blueprint(sse, url_prefix='/stream')

# configure logging
logging_formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

file_logging_handler = logging.FileHandler('testjig.log')
file_logging_handler.setFormatter(logging_formatter)
redis_logging_handler = RedisLoggingHandler(app)
redis_logging_handler.setFormatter(logging_formatter)
std_err_logging_handler = logging.StreamHandler()
std_err_logging_handler.setFormatter(logging_formatter)

api_logging = logging.getLogger('remote')
api_logging.setLevel(logging.DEBUG)
api_logging.addHandler(file_logging_handler)
api_logging.addHandler(std_err_logging_handler)

redis_logging = logging.getLogger()
redis_logging.setLevel(logging.DEBUG)
redis_logging.addHandler(file_logging_handler)
redis_logging.addHandler(std_err_logging_handler)
redis_logging.addHandler(redis_logging_handler)

pytest_logging = logging.getLogger()
pytest_logging.setLevel(logging.DEBUG)
pytest_logging.addHandler(file_logging_handler)
pytest_logging.addHandler(std_err_logging_handler)
pytest_logging.addHandler(redis_logging_handler)

power_control = PowerControl(True)


@app.route('/')
def index():
    """Home page"""
    return app.send_static_file('index.html')


@app.route('/dut-power/set/<on_off>')
def dut_power_set(on_off):
    if 'on' in on_off.lower():
        power_control.power_on()
    else:
        power_control.power_off()

    return f"power: {'ON' if power_control.power_status() else 'OFF'}"


@app.route('/dut-power/get')
def dut_power_get():
    return f"power: {'ON' if power_control.power_status() else 'OFF'}"


@app.route('/api/test', methods=['POST'])
def test():
    requested_data = request.get_json()
    redis_logging.debug(requested_data)

    board_serial_number = requested_data['boardSerialNumber']
    operator_name = requested_data['operatorName']

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")  # Generate a timestamp
    report_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   f'../files/logs/test-report_{board_serial_number}_{timestamp}.html')

    result = pytest.main(args=['-v', '-s', '--capture', 'sys',
                               '--board-serial-number', board_serial_number,
                               '--operator-name', operator_name,
                               '--html', report_filename,
                               'tests'],
                         plugins=[pytest_logging])
    return {'status': result.name, 'report_filename': report_filename}


@app.route('/api/test-report/<board_serial_number>')
def testReport(board_serial_number):
    # Get the latest report file by sorting based on timestamp and selecting the last one
    report_files = sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                 f'../files/logs/test-report_{board_serial_number}_*.html')))
    if report_files:
        latest_report_filename = report_files[-1]
        return send_file(latest_report_filename)
    else:
        return {'error': 'No report available'}


@app.route('/api/log', methods=['POST'])
def log():
    log_data = request.get_json()
    level = log_data.get('level', 'info')
    message = log_data.get('message', '')

    # log message
    if level == 'debug':
        api_logging.debug(message)
    elif level == 'warning':
        api_logging.warning(message)
    elif level == 'error':
        api_logging.error(message)
    else:
        api_logging.info(message)

    return 'OK'


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, debug=True)
