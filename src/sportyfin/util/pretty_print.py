import os
from dotenv import load_dotenv

load_dotenv()

verbosity = os.environ.get("verbosity")
no_verbosity = os.environ.get("no_verbosity")


class otype:
    ERROR = '-'
    DEBUG = '*'
    REGULAR = '+'


class colours:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def check_verbosity(t: str = otype.DEBUG):
    verbosity = os.environ.get("verbosity")
    no_verbosity = os.environ.get("no_verbosity")
    return (not(t == otype.DEBUG and verbosity == "1") and no_verbosity == "1") or t == otype.ERROR


def p(s: str, c: str = "", t: str = otype.DEBUG, err: Exception = None) -> str:
    if check_verbosity(t):
        print(f"{c}[{t}]{colours.ENDC} {s}")
    if err and verbosity == "0" and not no_verbosity == "0":
        print(err.with_traceback())


def pind(s: str, c: str = "", t: str = otype.DEBUG) -> str:
    if check_verbosity(t):
        print(f"{c}---> [{t}]{colours.ENDC} {s}")


def pind2(s: str, c: str = "", t: str = otype.DEBUG) -> str:
    if check_verbosity(t):
        print(f"{c}------> [{t}]{colours.ENDC} {s}")
