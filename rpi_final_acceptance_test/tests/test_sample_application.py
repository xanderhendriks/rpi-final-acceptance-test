import logging
import time

file_logging = logging.getLogger()


def test_version():
    a = 5
    b = 10
    assert a == b, f"Expected {a} to be equal to {b}, but they are not."


def test_sensor():
    pass
