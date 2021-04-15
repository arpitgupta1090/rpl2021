from datetime import datetime
import pytz
import logging
import os


def set_logger():
    logging_mode = os.environ.get('LOGGER_MODE')
    logging_level = getattr(logging, logging_mode)
    logging.basicConfig(level=logging_level, format="%(asctime)s:%(levelname)s:%(message)s")


def time_taken(func):
    time_ist = pytz.timezone("Asia/Kolkata")
    set_logger()

    def wrapper(*args, **kwargs):
        now = datetime.now(time_ist).strftime('%Y:%m:%d %H:%M:%S %Z %z')
        logging.info(f"Started {func.__name__} at {now}")
        start = datetime.now()
        val = func(*args, **kwargs)
        now = datetime.now(time_ist).strftime('%Y:%m:%d %H:%M:%S %Z %z')
        logging.info(f"Ended {func.__name__} at {now}")
        stop = datetime.now()
        logging.info(f"total time taken for {func.__name__} at {stop - start}")
        return val

    return wrapper


def print_return_value(func):
    set_logger()

    def wrapper(*args, **kwargs):
        not_my_data = set(dir())
        val = func(*args, **kwargs)
        my_data = set(dir()) - not_my_data

        for name in my_data:
            if name != "not_my_data":
                my_value = eval(name)
                logging.info(f"{name} {type(my_value)} = {my_value}")
        return val
    return wrapper


def print_all_variables(func):
    set_logger()
    function_string = '''for name in dir():
            if not name.startswith('__'):
                if name != "debug":
                    my_value = eval(name)
                    logging.info(f"{name} {type(my_value)} = {my_value}")'''

    def wrapper(*args):
        val = func(*args, debug=function_string)
        return val
    return wrapper


if __name__ == "__main__":

    set_logger()

    def test(st, debug=None):
        val1 = "arpit"
        logging.error(f" doing something {st}{val1}")

        if debug:
            exec(debug)
        return st

    test('hi')
