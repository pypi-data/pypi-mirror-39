import oyaml as yaml
import sys
from typing import Any


def loadfile(file: str, safe=False) -> dict:
    """
    Load yaml file.
    """
    if safe:
        with open(file, 'r') as f:
            return yaml.safe_load(f.read())
    else:
        with open(file, 'r') as f:
            return yaml.load(f.read())


def savefile(data: Any, file: str, **kwargs) -> None:
    """
    Save data to yaml file.
    """
    with open(file, 'w') as f:
        yaml.dump(data=data, stream=f, **kwargs)


def pprint_yaml(data: Any) -> None:

    lines: list = yaml.dump(
        data,
        indent=4,
        block_seq_indent=4,
    ).splitlines(True)

    print(''.join([line for line in lines]))
