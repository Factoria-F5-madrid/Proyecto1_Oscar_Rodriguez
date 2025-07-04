from enum import Enum


class Error(Enum):
    FARE_CANNOT_BE_CHANGED = 0
    FARE_MISSING = 1
    TRIP_IN_PROGRESS = 2
    TAXI_IS_NOT_STOPPED = 3
    TAXI_IS_NOT_MOVING = 4

    @classmethod
    def show(cls,logger,code):
        match code:
            case Error.FARE_CANNOT_BE_CHANGED:
                logger.get_log().error("The fare cannot be changed once the trip has started.")
            case Error.FARE_MISSING:
                logger.get_log().error("The new fare amount is missing.")
            case Error.TRIP_IN_PROGRESS:
                logger.get_log().error("Cannot start a trip if there is already a trip in progress.")
            case Error.TAXI_IS_NOT_STOPPED:
                logger.get_log().error("Taximeter is not stopped, or trip is not started.")
            case Error.TAXI_IS_NOT_MOVING:
                logger.get_log().error("Taximeter is not moving, or trip is not started.")
            case _:
                logger.get_log().error("Unknown error!")
