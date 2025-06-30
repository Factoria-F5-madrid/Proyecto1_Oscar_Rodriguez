from enum import Enum


class Status(Enum):
    WAITING = 0
    STOPPED = 1
    MOVING = 2
    QUIT = 3

    @classmethod
    def show(cls, status):
        match status:
            case Status.WAITING:
                return "trip not started"
            case Status.STOPPED:
                return "trip started. Taximeter is paused"
            case Status.MOVING:
                return "trip started. Taximeter is running"
            case _:
                return "unknown status"