import logging

from taximeter import Taximeter


def set_log():
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    ch.setFormatter(formatter)

    logger = logging.getLogger('taximeter')
    logger.setLevel(logging.ERROR)
    logger.addHandler(ch)

    return logger

if __name__ == '__main__':
    print("Welcome to the taximeter application.\n")

    logger = set_log()
    taximeter = Taximeter(logger)

    taximeter.run()