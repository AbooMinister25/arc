import logging
from logging.config import dictConfig
import json


class Logger:
    def __init__(self, config_dict: dict = None):
        if config_dict is not None:
            self.config_dict = config_dict
        else:
            self.config_dict = dict(
                version = 1,
                formatters={
                    'f': {'format':
                          '\n%(levelname)s: %(message)s'}
                },
                handlers={
                    'h': {'class': 'logging.StreamHandler',
                          'formatter': 'f',
                          'level': logging.INFO}
                },
                root={
                    'handlers': ['h'],
                    'level': logging.INFO,
                },
            )

        dictConfig(self.config_dict)

        self.logger = logging.getLogger()

    def log(self, message: str, level: str) -> None:
        levels = {
            "info": self.logger.info,
            "debug": self.logger.debug,
            "warning": self.logger.warning,
            "error": self.logger.error,
            "critical": self.logger.critical
        }

        levels[level](message)


def config_from_json(path: str) -> dict:
    with open(path, "r") as f:
        config_dict = json.load(f)

    return config_dict
