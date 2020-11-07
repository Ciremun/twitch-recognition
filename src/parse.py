import os
from argparse import ArgumentParser
from typing import Tuple

from .config import Config

parser = ArgumentParser()
parser.add_argument('-c', '--channel', type=str, help='twitch.tv username', nargs=1)
parser.add_argument('-e', '--engine', type=str, help='Google or Sphinx', nargs=1)
parser.add_argument('-l', '--language', type=str, help='language code', nargs=1)
parser.add_argument('-st', '--segment-time', type=int, help='ffmpeg segment_time in seconds', nargs=1)
parsed_args = parser.parse_args()

def try_parse_arguments(*args: Tuple[str]):
    for arg in args:
        value = getattr(parsed_args, arg)
        if value is None and not getattr(Config, arg):
            parser.error(f'{arg} parameter is missing, edit config or use flag')
        elif value is not None:
            setattr(Config, arg, value[0])

try_parse_arguments('engine')

if not any(Config.engine == x for x in Config.engines):
    print(f'Unknown engine, available: {", ".join(Config.engines)}')
    os._exit(0)

try_parse_arguments('channel', 'language', 'segment_time')
