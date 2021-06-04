from pathlib import Path


def path_is_valid(path):
    if Path(path).is_file():
        return True
    return False

class PathIsNotValid(Exception):
    pass