import re
import webbrowser
from typing import Tuple

import click

from helper.metadata import *
from helper.console import console_print

HOST_FORMAT = 'http://www.op.gg/champion/{champion_name}/statistics/{position}'
ENGLISH_REGEX = re.compile('^[A-z]+$')


def _map_korean_champion_name_to_english(champion_name: str) -> str:
    if champion_name not in CHAMPION_KOREAN_NAME_ENGLISH_NAME_MAPPING:
        raise ValueError()

    return CHAMPION_KOREAN_NAME_ENGLISH_NAME_MAPPING[champion_name]


def _map_korean_position_name_to_english(position_name: str) -> str:
    if position_name not in POSITION_KOREAN_NAME_ENGLISH_NAME_MAPPING:
        raise ValueError()

    return POSITION_KOREAN_NAME_ENGLISH_NAME_MAPPING[position_name]


def _map_korean_arguments_to_english(champion_name: str, position_name: str) -> Tuple[str, str]:
    return (
        champion_name if ENGLISH_REGEX.match(champion_name) else _map_korean_champion_name_to_english(champion_name),
        position_name if ENGLISH_REGEX.match(position_name) else _map_korean_position_name_to_english(position_name)
    )


def _extract_retrieve_target_info_from_arguments(arg1: str, arg2: str) -> Tuple[str, str]:
    """
    This function makes user can change the order of the arguments without any problems.
    ex) lulu support, support lulu

    returns tuple represents - (champion name, position name)
    """

    if arg1 in VALID_POSITION_NAMES:
        return arg2, arg1
    elif arg2 in VALID_POSITION_NAMES:
        return arg1, arg2
    elif arg1 in VALID_CHAMPION_NAMES:
        return arg1, arg2
    elif arg2 in VALID_CHAMPION_NAMES:
        return arg2, arg1
    else:
        raise ValueError()


def _are_arguments_valid(arg1: str, arg2: str) -> Tuple[bool, str]:
    if arg1 not in VALID_CHAMPION_NAMES and arg2 not in VALID_CHAMPION_NAMES:
        return False, '그런 챔피언 없음 ㅡㅡ'
    elif arg1 not in VALID_POSITION_NAMES and arg2 not in VALID_POSITION_NAMES:
        return False, '그런 포지션 없음 ㅡㅡ'
    else:
        return True, ''


@click.command()
@click.argument('arg1')
@click.argument('arg2')
@click.option('-c/--console', default=False)
def handler(arg1: str, arg2: str, c: bool):
    are_arguments_valid, msg = _are_arguments_valid(arg1, arg2)

    if are_arguments_valid:
        champion_name, position_name = _extract_retrieve_target_info_from_arguments(arg1, arg2)
        champion_name, position_name = _map_korean_arguments_to_english(champion_name, position_name)

        opgg_url = HOST_FORMAT.format(champion_name=champion_name, position=position_name)
        if c:
            console_print(opgg_url)
        else:
            webbrowser.open(opgg_url)
    else:
        print(msg)
