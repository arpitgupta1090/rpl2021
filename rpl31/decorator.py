from datetime import datetime
import pytz

IST = pytz.timezone("Asia/Kolkata")


def time_taken(func):
    def wrapper(*args, **kwargs):
        now = datetime.now(IST).strftime('%Y:%m:%d %H:%M:%S %Z %z')
        print("Started ", func.__name__, "at", now)
        start = datetime.now()
        val = func(*args, **kwargs)
        now = datetime.now(IST).strftime('%Y:%m:%d %H:%M:%S %Z %z')
        print("Ended ", func.__name__, "at", now)
        stop = datetime.now()
        print("total time taken: ", stop - start)
        return val

    return wrapper


if __name__ == "__main__":
    @time_taken
    def test(st):
        print("doing something", st)
        return st


    stri = test('hi')

    print(stri)
