import subprocess
import signal
import random
import json
import time
import sys
import os
from threading import Thread
from typing import Callable
from pathlib import Path

from src.recognize import recognize_audio
from src.log import logger

channel = sys.argv[1].lower()
engine = sys.argv[2].lower()
engines = ['google', 'sphinx']

if not any(engine == x for x in engines):
    print(f'Unknown engine, available: {", ".join(engines)}')
    os._exit(0)

interrupt_signal = signal.SIGINT

if sys.platform == 'win32':
    interrupt_signal = signal.CTRL_C_EVENT

Path("audio/").mkdir(exist_ok=True)
config = json.load(open('config.json'))
processed_filenames = []

def valid_filename(x: str) -> bool:
    return all(x != y for y in processed_filenames) and x.lower().startswith(channel) and x.endswith('.wav')


def rand_str(*, length: int) -> str:
    random_string = ''.join(random.choices('qwertyuiopasdfghjklzxcvbnm1234567890', k=length))
    return random_string


def get_filename(folder, form) -> str:
    filename = f"{channel}_{rand_str(length=6)}"
    path = Path(f'{folder}{filename}{form}')
    while path.is_file():
        filename = f"{channel}_{rand_str(length=6)}"
        path = Path(f'{folder}{filename}{form}')
    return filename


def print_and_log(msg: str, logger_func: Callable):
    print(msg)
    logger_func(msg)


def send_message(msg: str):
    print_and_log(msg, logger.warning)


def delete_processed_files():
    while True:
        time.sleep(120)
        for filename in processed_filenames:
            try:
                os.remove(f'audio/{filename}')
            except Exception as e:
                logger.exception(e)
        processed_filenames.clear()


def find_words():
    filenames = [x for x in os.listdir('audio/') if valid_filename(x)]
    for filename in filenames:
        part = recognize_audio(f'audio/{filename}', engine, config['language'])
        if not part:
            continue
        print_and_log(f'{channel}: {part}', logger.info)
        for target, message in config['targets'].items():
            if target in part.lower():
                send_message(message)
        processed_filenames.append(filename)


def words():
    while True:
        time.sleep(1)
        find_words()

def download():
    while True:
        filename = get_filename('audio/', '.wav')
        command = f"""\
youtube-dl \
-x https://twitch.tv/{channel} \
--audio-format wav \
--cookies cookies.txt \
-q \
-o audio/{filename}.%(ext)s\
"""
        print(filename)
        download_process = subprocess.Popen(command.split())
        time.sleep(10)
        download_process.send_signal(interrupt_signal)

if __name__ == "__main__":
    Thread(target=words).start()
    Thread(target=download).start()
    Thread(target=delete_processed_files).start()
