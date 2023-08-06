import logging
from contextlib import contextmanager


@contextmanager
def print_message(message):
    print(message, flush=True, end="")
    yield
    print(" \b\b" * len(message), flush=True, end="")


def init_logger(level="info"):
    logging.root.setLevel(level.upper())

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('\033[0;32m%(asctime)s \033[0;34m%(levelname)s\t%(name)s:\033[0m %(message)s')
    ch.setFormatter(formatter)
    logging.root.addHandler(ch)
