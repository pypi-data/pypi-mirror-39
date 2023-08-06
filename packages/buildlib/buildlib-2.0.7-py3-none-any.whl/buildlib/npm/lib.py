import json
from typing import Optional
from cmdi import CmdResult, command, set_result, strip_args
import subprocess as sp


class cmd:

    @staticmethod
    @command
    def bump_version(
        new_version: str, filepath: str = 'package.json', **cmdargs
    ) -> CmdResult:
        return set_result(bump_version(**strip_args(locals())))

    @staticmethod
    @command
    def publish(**cmdargs) -> CmdResult:
        return set_result(publish(**strip_args(locals())))


def bump_version(
    new_version: str,
    filepath: Optional[str] = 'package.json',
    indent: Optional[int] = 4,
) -> None:

    data = ''

    with open(filepath, 'r') as f:
        data = json.load(f)

    data['version'] = new_version

    with open(filepath, 'w') as f:
        json.dump(data, f, indent=indent)


def publish() -> None:
    """"""
    sp.run(
        ['npm', 'publish'],
        check=True,
    )
