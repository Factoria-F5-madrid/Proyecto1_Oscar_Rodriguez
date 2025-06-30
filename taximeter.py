import time

from lib.error import Error
from lib.status import Status


class Taximeter:
    FARE_STOPPED = 2
    FARE_MOVING  = 5

    def __init__(self, logger):
        self.__logger = logger
        self.__logger.debug("In Taximeter.init")
        self.__status = Status.WAITING
        self.__fare_moving = self.FARE_MOVING
        self.__fare_stopped = self.FARE_STOPPED
        self.__total_fare = 0
        self.__seconds_moving = 0
        self.__seconds_stopped = 0
        self.__start_time = 0
        self.__stop_time = 0

    def __error(self,error_number):
        self.__logger.debug("In Taximeter.error")
        Error.show(self.__logger, error_number)

    def __show_help(self):
        self.__logger.debug("In Taximeter.show_help")
        print("The following commands are available:")
        print()
        print("- fare_stopped <number>. Sets the amount in cents per second that the customer will be")
        print("                         charged when the taxi is not moving. The default is: "
               + str(self.FARE_STOPPED) + " cents.")
        print("- fare_moving <number>.  Sets the amount in cents per second that the customer will be")
        print("                         charged when the taxi is moving. The default is: "
              + str(self.FARE_MOVING) + " cents.")
        print("- start.                 New trip. Taximeter is stopped")
        print("- move.                  Taximeter is moving.")
        print("- stop.                  Taximeter is stopped.")
        print("- end.                   Trip is completed. Total fare is calculated and displayed.")
        print("- quit.                  Ends the application. Taximeter must be in waiting status.")
        print("- help.                  Shows list of commands.")

    def __show_commands(self):
        self.__logger.debug("In Taximeter.show_commands")
        print("\nAvailable commands:")
        print("fare_stopped, fare_moving, start, move, stop, end, quit, help")

    def run(self):
        self.__logger.debug("In Taximeter.run")
        self.__show_help()

        while self.__status != Status.QUIT:
            cmd = input("\nPlease enter a command (" + Status.show(self.__status) + "): ")
            self.__process_command(cmd.split())

        print("Thank you for using the taximeter application!")

    def __set_stopped_fare(self, new_fare):
        self.__logger.debug("In Taximeter.set_stopped_fare %s", new_fare)
        if self.__status == Status.WAITING:
            self.__fare_stopped = int(new_fare)
            print("The fare when the taxi is stopped is now: " + str(self.__fare_stopped) + " cents.")
        else:
            self.__error(Error.FARE_CANNOT_BE_CHANGED)

    def __set_moving_fare(self, new_fare):
        self.__logger.debug("In Taximeter.set_moving_fare %s", new_fare)
        if self.__status == Status.WAITING:
            self.__fare_moving = int(new_fare)
            print("The fare when the taxi is moving is now: " + str(self.__fare_moving) + " cents.")
        else:
            self.__error(Error.FARE_CANNOT_BE_CHANGED)

    def __start(self):
        self.__logger.debug("In Taximeter.start")
        if self.__status == Status.WAITING:
            self.__status = Status.STOPPED
            self.__start_time = time.time()
        else:
            self.__error(Error.TRIP_IN_PROGRESS)

    def __move(self):
        self.__logger.debug("In Taximeter.move")
        if self.__status == Status.STOPPED:
            self.__stop_time = time.time()
            self.__seconds_stopped = self.__seconds_stopped + (self.__stop_time - self.__start_time)
            self.__status = Status.MOVING
            self.__start_time = time.time()
        else:
            self.__error(Error.TAXI_IS_NOT_STOPPED)

    def __stop(self):
        self.__logger.debug("In Taximeter.stop")
        if self.__status == Status.MOVING:
            self.__stop_time = time.time()
            self.__seconds_moving = self.__seconds_moving + (self.__stop_time - self.__start_time)
            self.__status = Status.STOPPED
            self.__start_time = time.time()
        else:
            self.__error(Error.TAXI_IS_NOT_MOVING)

    def __end(self):
        self.__logger.debug("In Taximeter.end")
        if self.__status == Status.MOVING:
            self.__stop()

        if self.__status == Status.STOPPED:
            self.__stop_time = time.time()
            self.__seconds_stopped = self.__seconds_stopped + (self.__stop_time - self.__start_time)
            self.__status = Status.WAITING
            self.__total_fare = self.__calculate_fare()
            print(f"Seconds taximeter was paused: {self.__seconds_stopped: .1f}")
            print(f"Seconds taximeter was running: {self.__seconds_moving: .1f}\n")
            print(f"Total to pay: {self.__total_fare: .2f}€")
            self.__seconds_moving = 0
            self.__seconds_stopped = 0
            self.__total_fare = 0
        else:
            self.__error(Error.TAXI_IS_NOT_STOPPED)

    def __calculate_fare(self):
        self.__logger.debug("In Taximeter.calculate_fare")
        return (self.__seconds_moving * self.__fare_moving + self.__seconds_stopped * self.__fare_stopped) / 100

    def __process_command(self, cmd):
        self.__logger.debug("In Taximeter.process_command")
        if len(cmd) == 0:
            self.__show_commands()
            return

        match cmd[0].lower():
            case "fare_stopped":
                if len(cmd) == 1:
                    self.__error(Error.FARE_MISSING)
                else:
                    self.__set_stopped_fare(cmd[1])
            case "fare_moving":
                if len(cmd) == 1:
                    self.__error(Error.FARE_MISSING)
                else:
                    self.__set_moving_fare(cmd[1])
            case "start":
                self.__start()
            case "move":
                self.__move()
            case "stop":
                self.__stop()
            case "end":
                self.__end()
            case "quit":
                if self.__status == Status.WAITING:
                    self.__status = Status.QUIT
            case "help":
                self.__show_commands()
            case _:
                self.__show_commands()
