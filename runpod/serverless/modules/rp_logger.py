'''
PodWorker | modules | logging.py

Log Levels (Level - Value - Description)

NOTSET - 0 - No logging is configured, the logging system is effectively disabled.
DEBUG - 1 - Detailed information, typically of interest only when diagnosing problems. (Default)
INFO - 2 - Confirmation that things are working as expected.
WARN - 3 - An indication that something unexpected happened.
ERROR - 4 - Serious problem, the software has not been able to perform some function.
'''

import os
from dotenv import load_dotenv

env_path = os.path.join(os.getcwd(), '.env')
load_dotenv(env_path)  # Load environment variables

LOG_LEVELS = ['NOTSET', 'DEBUG', 'INFO', 'WARN', 'ERROR']


def _validate_log_level(log_level):
    '''
    Checks the debug level and returns the debug level name.
    '''
    if isinstance(log_level, str):
        log_level = log_level.upper()

        if log_level not in LOG_LEVELS:
            raise ValueError(f'Invalid debug level: {log_level}')

        return log_level

    if isinstance(log_level, int):
        if log_level < 0 or log_level > 4:
            raise ValueError(f'Invalid debug level: {log_level}')

        return LOG_LEVELS[log_level]

    raise ValueError(f'Invalid debug level: {log_level}')


class RunPodLogger:
    '''Singleton class for logging.'''

    __instance = None
    level = _validate_log_level(os.environ.get('RUNPOD_DEBUG_LEVEL', 'DEBUG'))

    def __new__(cls):
        if RunPodLogger.__instance is None:
            RunPodLogger.__instance = object.__new__(cls)
        return RunPodLogger.__instance

    def set_level(self, new_level):
        '''
        Set the debug level for logging.
        Can be set to the name or value of the debug level.
        '''
        self.level = _validate_log_level(new_level)
        self.info(f'Log level set to {self.level}')

    def log(self, message, message_level='INFO'):
        '''
        Log message to stdout if RUNPOD_DEBUG is true.
        '''
        if self.level == 'NOTSET':
            return

        level_index = LOG_LEVELS.index(self.level)
        if level_index > LOG_LEVELS.index(message_level) and message_level != 'TIP':
            return

        print(f'{message_level.ljust(7)}| {message}', flush=True)
        return

    def secret(self, secret_name, secret):
        '''
        Censors secrets for logging.
        Replaces everything except the first and last characters with *
        '''
        secret = str(secret)
        redacted_secret = secret[0] + '*' * (len(secret)-2) + secret[-1]
        self.info(f"{secret_name}: {redacted_secret}")

    def debug(self, message):
        '''
        debug log
        '''
        self.log(message, 'DEBUG')

    def info(self, message):
        '''
        info log
        '''
        self.log(message, 'INFO')

    def warn(self, message):
        '''
        warn log
        '''
        self.log(message, 'WARN')

    def error(self, message):
        '''
        error log
        '''
        self.log(message, 'ERROR')

    def tip(self, message):
        '''
        tip log
        '''
        self.log(message, 'TIP')
