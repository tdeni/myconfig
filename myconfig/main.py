from json import load as j_load
from json.decoder import JSONDecodeError
from pathlib import Path
from typing import Any

from toml import load as t_laod
from yaml import safe_load as y_load

DIR = Path.cwd()


class MyConfig():
    def __init__(self, filenames: list) -> None:
        self.config = parser(filenames)

    def __getattr__(self, key) -> Any:
        return self.config.get(key, None)


def parser(files: list) -> dict:
    '''This is a function that parses files.

    Args:
        files (list): Path to the files.

    Raises:
        Exception: Unknown format.
        Exception: Specify the correct path to the files.

    Returns:
        dict: Parsed data.
    '''

    format = files[0].split('.')[1]
    data = dict()
    try:
        if format == 'json':
            for file in files:
                with open(DIR.joinpath(file)) as f:
                    try:
                        data.update(j_load(f))
                    except JSONDecodeError:
                        pass
        elif format == 'toml':
            for file in files:
                with open(DIR.joinpath(file)) as f:
                    data.update(t_laod(f))
        elif format == 'yaml':
            for file in files:
                with open(DIR.joinpath(file)) as f:
                    data.update(y_load(f))
        else:
            raise Exception('Unknown format.')
    except FileNotFoundError:
        raise Exception('Specify the correct path to the files.')
    return data
