import logging
import logging.config

from taximeter import Taximeter


def set_log():
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
                'filename': 'taximeter.log',
                'formatter': 'default',
            },
            'stdout': {
                'level': 'ERROR',
                'class': 'logging.StreamHandler',
                'formatter': 'default',
            },
        },
        'loggers': {
            'Taximeter': {
                'handlers': ['file', 'stdout'],
                'level': 'DEBUG',
                'propagate': True,
            },
        },
    }

    logging.config.dictConfig(logging_config)
    my_logger = logging.getLogger('Taximeter')

    return my_logger

if __name__ == '__main__':
    print("Welcome to the taximeter application.\n")

    logger = set_log()
    logger.debug("Initializing the application.")
    taximeter = Taximeter(logger)

    logger.debug("Starting the application.")
    taximeter.run(None)