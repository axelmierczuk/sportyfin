verbosity = False
no_verbosity = False

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
    return not(t == otype.DEBUG and not verbosity) and not no_verbosity


def p(s: str, c: str = "", t: str = otype.DEBUG, err: Exception = None) -> str:
    if check_verbosity(t):
        print(f"{c}[{t}]{colours.ENDC if t != otype.REGULAR else ''} {s}{colours.ENDC}")
    if err and verbosity and not no_verbosity:
        print(err.with_traceback())


def pind(s: str, c: str = "", t: str = otype.DEBUG) -> str:
    if check_verbosity(t):
        print(f"{c}---> [{t}]{colours.ENDC if t != otype.REGULAR else ''} {s}{colours.ENDC}")


def pind2(s: str, c: str = "", t: str = otype.DEBUG) -> str:
    if check_verbosity(t):
        print(f"{c}------> [{t}]{colours.ENDC if t != otype.REGULAR else ''} {s}{colours.ENDC}")
