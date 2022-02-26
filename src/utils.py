import datetime
import logging

from colorama import init as c_init, Fore, Back, Style


c_init(autoreset=True)


def dtp(message: str, level: str = 'INFO') -> None:
    print(f'{Fore.BLUE}[{datetime.datetime.utcnow()}] - {Fore.YELLOW}[{level}] {Fore.WHITE}- {message}')


class STDOUT_LOGGER(logging.Handler):

    def __init__(self):
        super(STDOUT_LOGGER, self).__init__()

    def emit(self, record: logging.LogRecord) -> None:
        if record.levelname == 'DEBUG':
            return

        level = record.levelname
        message = record.msg

        if record.levelname == 'ERROR':
            message = f'{Fore.RED}{message}'

        elif record.levelname in ('WARNING', 'CRITICAL'):
            message = f'{Fore.YELLOW}{message}'

        else:
            message = f'{Fore.CYAN}{message}'

        print(f'{Fore.BLUE}[{datetime.datetime.utcnow()}] - {Fore.YELLOW}[{level}] {Fore.WHITE}- {message}')
