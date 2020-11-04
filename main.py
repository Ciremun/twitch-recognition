import subprocess
import signal
import random
import time
import sys
import os
from threading import Thread
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
python = sys.executable

if sys.platform == 'win32':
    interrupt_signal = signal.CTRL_C_EVENT

Path("audio/").mkdir(exist_ok=True)

targets = {
    'unless': '\U0001F633'
}

processed_filenames = []

def get_filename(folder, filename, form) -> str:
    path = Path(f'{folder}{filename}{form}')
    while path.is_file():
        filename = f"{channel}_{''.join(random.choices('qwertyuiopasdfghjklzxcvbnm1234567890', k=5))}"
        path = Path(f'{folder}{filename}{form}')
    return filename


def delete_processed_files():
    while True:
        time.sleep(120)
        for filename in processed_filenames:
            try:
                os.remove(f'audio/{filename}')
            except Exception as e:
                logger.exception(e)
        processed_filenames.clear()


def send_message(message: str):
    print(message)
    logger.warning(message)


def find_words():
    filenames = [x for x in os.listdir('audio/') if x.lower().startswith(channel) and x.endswith('.wav') and not any(x == y for y in processed_filenames)]
    for filename in filenames:
        part = recognize_audio(f'audio/{filename}', engine)
        msg = f'{channel}: {part}'
        logger.info(msg)
        print(msg)
        for target, message in targets.items():
            if target in part:
                send_message(message)
        processed_filenames.append(filename)


def words():
    while True:
        time.sleep(1)
        find_words()


def download():
    while True:
        filename = get_filename('audio/', channel, '.wav')
        download_process = subprocess.Popen([python, 'src/download.py', channel, filename])
        time.sleep(10)
        download_process.send_signal(interrupt_signal)


if __name__ == "__main__":
    Thread(target=words).start()
    Thread(target=download).start()
    Thread(target=delete_processed_files).start()
