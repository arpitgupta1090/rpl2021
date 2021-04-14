from datetime import datetime
import pytz
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s")
IST = pytz.timezone("Asia/Kolkata")


def time_taken(func):
    def wrapper(*args, **kwargs):
        now = datetime.now(IST).strftime('%Y:%m:%d %H:%M:%S %Z %z')
        logging.info(f"Started {func.__name__} at {now}")
        start = datetime.now()
        val = func(*args, **kwargs)
        now = datetime.now(IST).strftime('%Y:%m:%d %H:%M:%S %Z %z')
        logging.info(f"Ended {func.__name__} at {now}")
        stop = datetime.now()
        logging.info(f"total time taken for {func.__name__} at {stop - start}")
        return val

    return wrapper


def logger(func):
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
    function_string = '''for name in dir():
            if not name.startswith('__'):
                if name != "debug":
                    my_value = eval(name)
                    print(f"{name} {type(my_value)} = {my_value}")'''

    def wrapper(*args):
        val = func(*args, debug=function_string)
        return val
    return wrapper


if __name__ == "__main__":

    @print_all_variables
    @time_taken
    # @logger
    def test(st, debug=None):
        val1 = "arpit"
        print(f" doing something {st}{val1}")

        if debug:
            exec(debug)
        return st

    test('hi')
