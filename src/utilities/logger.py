import os
import logging

from configuration import DEFAULT_LOGGING_LEVEL, LOG_FILE_PATH


class Logger:
    def __init__(self, name: str, log_level: str) -> None:
        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging.INFO)

        if not os.path.exists(LOG_FILE_PATH):
            os.makedirs(LOG_FILE_PATH)

        formatter = logging.Formatter(
            "%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")

        file_handler = logging.FileHandler(filename=os.path.join(LOG_FILE_PATH, name + ".log"))
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(log_level)
        stream_handler.setFormatter(formatter)

        self._logger.addHandler(file_handler)
        self._logger.addHandler(stream_handler)

    @property
    def logger(self) -> logging:
        return self._logger
