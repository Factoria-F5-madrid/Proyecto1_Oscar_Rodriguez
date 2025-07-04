from lib.logger import Logger
from taximeter import Taximeter

if __name__ == '__main__':
    print("Welcome to the taximeter application.\n")

    logger = Logger("taximeter")
    logger.get_log().debug("Initializing the application.")
    taximeter = Taximeter(logger)

    logger.get_log().debug("Starting the application.")
    taximeter.run(None)