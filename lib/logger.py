import logging
import logging.config
from io import StringIO


class Logger:
    def __init__(self, log_name = "unit_test"):
        if log_name == "unit_test":
            self.__init_unit_test()
            return
        self.__init_production(log_name)

    def __init_production(self, log_name):
        logging_config = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'default': {
                    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                },
            },
            'handlers': {
                'file': {
                    'level': 'DEBUG',
                    'class': 'logging.FileHandler',
                    'filename': log_name + '.log',
                    'formatter': 'default',
                },
                'stdout': {
                    'level': 'ERROR',
                    'class': 'logging.StreamHandler',
                    'formatter': 'default',
                },
            },
            'loggers': {
                log_name: {
                    'handlers': ['file', 'stdout'],
                    'level': 'DEBUG',
                    'propagate': True,
                },
            },
        }

        logging.config.dictConfig(logging_config)
        self.__log = logging.getLogger(log_name)

    def __init_unit_test(self):
        self.__data = StringIO()

        handler = logging.StreamHandler(self.__data)
        handler.setLevel(logging.DEBUG)

        my_logger = logging.getLogger('unit_test')
        my_logger.setLevel(logging.DEBUG)
        my_logger.addHandler(handler)

        self.__log = my_logger

    def get_log(self):
        return self.__log

    def get_log_data(self):
        return self.__data

