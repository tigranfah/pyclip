from pathlib import Path


def path_is_valid(path):
    if Path(path).is_file():
        return True
    return False


def is_of_type(value, type):
    return isinstance(value, tuple)


class PathIsNotValid(Exception):
    pass


class ValueError(Exception):
    pass


class SingletonClass(Exception):
    pass
