from doit.action import CmdAction  # type: ignore


def task_install_precommit() -> dict:
    """Install pre-commit hooks."""

    def cmd_precommit_hooks() -> str:
        return "poetry run pre-commit install"

    def cmd_precommit_commitmsg_hooks() -> str:
        return "poetry run pre-commit install --hook-type commit-msg"

    return {
        "actions": [
            CmdAction(cmd_precommit_hooks),
            CmdAction(cmd_precommit_commitmsg_hooks),
        ],
        "verbosity": 2,
    }
