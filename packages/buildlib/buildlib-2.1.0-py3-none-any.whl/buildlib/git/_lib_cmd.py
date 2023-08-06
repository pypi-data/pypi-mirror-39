from typing import Optional
from cmdi import command, CmdResult, set_result, strip_args

from ..git import _lib


@command
def add_all(**cmdargs) -> CmdResult:
    return _lib.set_result(add_all(**strip_args(locals())))


@command
def commit(
    msg: str,
    **cmdargs,
) -> CmdResult:
    return _lib.set_result(commit(**strip_args(locals())))


@command
def tag(
    version: str,
    branch: str,
    **cmdargs,
) -> CmdResult:
    return _lib.set_result(tag(**strip_args(locals())))


@command
def push(
    branch: str,
    **cmdargs,
) -> CmdResult:
    return _lib.set_result(push(**strip_args(locals())))


@command
def get_default_branch(**cmdargs) -> CmdResult:
    return _lib.set_result(get_default_branch(**strip_args(locals())))


@command
def status(**cmdargs) -> CmdResult:
    return _lib.set_result(status(**strip_args(locals())))


@command
def diff(**cmdargs) -> CmdResult:
    return _lib.set_result(diff(**strip_args(locals())))
