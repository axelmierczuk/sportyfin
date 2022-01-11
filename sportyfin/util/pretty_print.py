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
    HEADER = '\033[95m' if os.name != 'nt' else ""
    OKBLUE = '\033[94m' if os.name != 'nt' else ""
    OKCYAN = '\033[96m' if os.name != 'nt' else ""
    OKGREEN = '\033[92m' if os.name != 'nt' else ""
    WARNING = '\033[93m' if os.name != 'nt' else ""
    FAIL = '\033[91m' if os.name != 'nt' else ""
    ENDC = '\033[0m' if os.name != 'nt' else ""
    BOLD = '\033[1m' if os.name != 'nt' else ""
    UNDERLINE = '\033[4m' if os.name != 'nt' else ""


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
