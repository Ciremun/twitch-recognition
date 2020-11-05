import subprocess
import logging
import time
import os
from logging.handlers import RotatingFileHandler
from typing import Callable, List, Tuple
from threading import Thread
from pathlib import Path

from src.recognize import recognize_audio
from src.parse import Config

Config.channel = Config.channel.lower()
Config.engine = Config.engine.lower()

Path("audio/").mkdir(exist_ok=True)
Path("log/").mkdir(exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fileHandler = RotatingFileHandler(f'log/{Config.channel}.log', mode='a', maxBytes=5242880, backupCount=2)
fileHandler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s [%(filename)s:%(lineno)d] %(message)s'))
logger.addHandler(fileHandler)


def valid_filename(x: str) -> bool:
    return x.lower().startswith(Config.channel) and x.endswith('.wav')


def print_and_log(msg: str, logger_func: Callable):
    print(msg)
    logger_func(msg)


def send_message(msg: str):
    print_and_log(msg, logger.warning)


def delete_audio_files(files_to_delete: List[str]):
    for filename in files_to_delete:
        try:
            os.remove(f'audio/{filename}')
        except Exception as e:
            logger.exception(e)


def find_targets() -> List[str]:
    filenames = [x for x in os.listdir('audio/') if valid_filename(x)]
    processed_files = []
    for filename in filenames[:-1]:
        processed_files.append(filename)
        part = recognize_audio(f'audio/{filename}', Config.engine, Config.language)
        if not part:
            continue
        print_and_log(f'{Config.channel}: {part}', logger.info)
        for target, message in Config.targets.items():
            if target in part.lower():
                send_message(message)
    return processed_files


def words():
    while True:
        time.sleep(Config.segment_time)
        processed_files = find_targets()
        if processed_files:
            delete_audio_files(processed_files)


def main():
    command = f'youtube-dl -x --get-url https://twitch.tv/{Config.channel} --cookies cookies.txt'
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    url = process.communicate()[0].decode().rstrip()
    command = f'ffmpeg -i {url} -v quiet -f segment -segment_time {Config.segment_time} -segment_format wav audio/{Config.channel}%05d.wav'
    process = subprocess.Popen(command.split())
    words_thread = Thread(target=words)
    words_thread.daemon = True
    words_thread.start()
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
