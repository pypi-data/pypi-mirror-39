import prmt
from headlines import h3
from buildlib.git import lib as git


def commit_msg(
    fmt=None,
    editor: bool = True,
) -> str:

    return prmt.string(
        question='Enter COMMIT message:\n',
        fmt=fmt,
        force_val=True,
        editor=editor,
    )


def branch(
    default=None,
    fmt=None,
) -> str:

    default = git.cmd.get_default_branch().val

    return prmt.string(
        question='Enter BRANCH name:\n',
        default=default,
        fmt=fmt,
    )


def confirm_status(
    default: str = 'y',
    fmt=None,
) -> bool:

    print(h3('Git Status'))
    git.cmd.status()

    return prmt.confirm(
        question='GIT STATUS ok?\n',
        default=default,
        fmt=fmt,
    )


def confirm_diff(
    default: str = 'y',
    fmt=None,
) -> bool:

    print(h3('Git Diff'))
    git.cmd.diff()

    return prmt.confirm(
        question='GIT DIFF ok?\n',
        default=default,
        fmt=fmt,
    )


def should_run_git(
    default: str = 'y',
    fmt=None,
) -> bool:

    return prmt.confirm(
        question='Run ANY GIT COMMANDS?\n',
        default=default,
        fmt=fmt,
    )


def should_add_all(
    default: str = 'y',
    fmt=None,
) -> bool:

    return prmt.confirm(
        question='Run GIT ADD ALL ("git add --all")?\n',
        default=default,
        fmt=fmt,
    )


def should_commit(
    default: str = 'y',
    fmt=None,
) -> bool:

    return prmt.confirm(
        question='Run GIT COMMIT?\n',
        default=default,
        fmt=fmt,
    )


def should_tag(
    default: str = 'y',
    fmt=None,
) -> bool:

    return prmt.confirm(
        question='Run GIT TAG?\n',
        default=default,
        fmt=fmt,
    )


def should_push(
    default: str = 'y',
    fmt=None,
) -> bool:

    return prmt.confirm(
        question='GIT PUSH to GITHUB?\n',
        default=default,
        fmt=fmt,
    )
