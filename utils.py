from typing import Iterator


def id_generator(size: int) -> Iterator:
    """
    Creates iterable that generates new id
    :return: iterator object
    """
    for i in range(1, size):
        yield i


from datetime import datetime


def get_time():
    """
    It's used to get current time for logging
    :return:
    """
    return datetime.now().strftime("%F %H:%M:%S")


