from termcolor import colored


def red(msg, attrs=None):
    return colored(msg, "red", attrs=attrs)


def green(msg, attrs=None):
    return colored(msg, "green", attrs=attrs)


def yellow(msg, attrs=None):
    return colored(msg, "yellow", attrs=attrs)


def info(msg, attrs=None):
    """
    Use if you want to highlight general info in the console.
    """
    print((colored(msg, "green", attrs=attrs)))


def warn(msg, attrs=None):
    """
    Use if you want to highlight a warning in the console.
    """
    print((colored(msg, "yellow", attrs=attrs)))


def error(msg, attrs=None):
    """
    Use if you want to highlight an error in the console.
    """
    print((colored(msg, "red", attrs=["bold"])))