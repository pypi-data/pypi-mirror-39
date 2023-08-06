import sys


class colors:
    _error = "\033[0;38;5;9m"
    _warn = "\033[0;38;5;11m"
    _ok = "\033[0;38;5;2m"
    _clear = "\033[0m"

    @classmethod
    def error(cls, message):
        return f"{cls._error}{message}{cls._clear}"

    @classmethod
    def warn(cls, message):
        return f"{cls._warn}{message}{cls._clear}"

    @classmethod
    def ok(cls, message):
        return f"{cls._ok}{message}{cls._clear}"


def print_and_exit(message, code=0):
    print(message)
    sys.exit(code)


def print_error(message):
    print(colors.error(f"ERROR: {message}"), file=sys.stderr)


def print_error_and_exit(message, code=1):
    print_error(message)
    sys.exit(code)


def print_warn(message):
    print(colors.warn(f"WARNING: {message}"))


def print_ok(message):
    print(colors.ok(f"OK: {message}"))
