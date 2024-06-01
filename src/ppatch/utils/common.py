import subprocess
from typing import Any

from ppatch.app import logger
from ppatch.model import CommandResult, CommandType


def clean_repo():
    output = subprocess.run(["git", "clean", "-df"], capture_output=True).stdout.decode(
        "utf-8"
    )
    logger.debug(output)

    output = subprocess.run(
        ["git", "reset", "--hard"], capture_output=True
    ).stdout.decode("utf-8")
    logger.debug(output)


def process_title(filename: str):
    """
    Process the file name to make it suitable for path
    """
    return "".join([letter for letter in filename if letter.isalnum()])


def find_list_positions(main_list: list[str], sublist: list[str]) -> list[int]:
    sublist_length = len(sublist)
    positions = []

    for i in range(len(main_list) - sublist_length + 1):
        if main_list[i : i + sublist_length] == sublist:
            positions.append(i)

    return positions


def isnamedtupleinstance(x):
    _type = type(x)
    bases = _type.__bases__
    if len(bases) != 1 or bases[0] != tuple:
        return False
    fields = getattr(_type, "_fields", None)
    if not isinstance(fields, tuple):
        return False
    return all(type(i) == str for i in fields)


def unpack(obj):
    if isinstance(obj, dict):
        return {key: unpack(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [unpack(value) for value in obj]
    elif isnamedtupleinstance(obj):
        return {key: unpack(value) for key, value in obj._asdict().items()}
    elif isinstance(obj, tuple):
        return tuple(unpack(value) for value in obj)
    else:
        return obj


def post_executed(executed_command_result: CommandResult | Any, **kwargs) -> None:
    """Executed command result callback function"""
    if type(executed_command_result) != CommandResult:
        return

    logger.debug(f"Executed {executed_command_result.type}")

    match executed_command_result.type:
        case CommandType.AUTO:
            clean_repo()
        case _:
            pass
