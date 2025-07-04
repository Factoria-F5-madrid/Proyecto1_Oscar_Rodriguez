import time

from lib.error import Error
from lib.status import Status


class Taximeter:
    FARE_STOPPED = 2
    FARE_MOVING  = 5

    def __init__(self, logger):
        """
        Initializes the class

        :param logger: Used to write message to the log
        """
        self.__logger = logger
        self.__logger.get_log().debug("In Taximeter.init")
        self.__status = Status.WAITING
        self.__fare_moving = self.FARE_MOVING
        self.__fare_stopped = self.FARE_STOPPED
        self.__total_fare = 0
        self.__seconds_moving = 0
        self.__seconds_stopped = 0
        self.__start_time = 0
        self.__stop_time = 0
        self.__last_error = ""

    def __error(self,error_number):
        """
        Writes an error message

        :param error_number: The error code to be displayed
        :return:
        """
        self.__logger.get_log().debug("In Taximeter.error")
        self.__last_error = Error.show(self.__logger, error_number)

    def __show_help(self):
        """
        Shows help on the screen

        :return:
        """
        self.__logger.get_log().debug("In Taximeter.show_help")
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
        """
        Shows the available commands on the screen

        :return:
        """
        self.__logger.get_log().debug("In Taximeter.show_commands")
        print("\nAvailable commands:")
        print("fare_stopped, fare_moving, start, move, stop, end, quit, help")

    def run(self, cmd=None):
        """
        Runs the taximeter. The taximeter will keep running until the command
        'quit' is entered.

        :param cmd: One of the valid commands for the taximeter, if any
        :return:
        """
        self.__logger.get_log().debug("In Taximeter.run")

        if cmd is not None:
                self.__process_command(cmd.split())
        else:
            self.__show_help()
            while self.__status != Status.QUIT:
                cmd = input("\nPlease enter a command (" + Status.show(self.__status) + "): ")
                self.__process_command(cmd.split())

            print("Thank you for using the taximeter application!")

    def __set_stopped_fare(self, new_fare):
        """
        Sets the fare when the taximeter is stopped.

        :param new_fare: The new fare value
        :return:
        """
        self.__logger.get_log().debug("In Taximeter.set_stopped_fare %s", new_fare)
        if self.__status == Status.WAITING:
            self.__fare_stopped = int(new_fare)
            print("The fare when the taxi is stopped is now: " + str(self.__fare_stopped) + " cents.")
            self.__logger.get_log().debug(f"New stopped fare: {self.__fare_stopped}")
        else:
            self.__error(Error.FARE_CANNOT_BE_CHANGED)

    def __set_moving_fare(self, new_fare):
        """
        Sets the fare when the taximeter is running

        :param new_fare: The new fare value
        :return:
        """
        self.__logger.get_log().debug("In Taximeter.set_moving_fare %s", new_fare)
        if self.__status == Status.WAITING:
            self.__fare_moving = int(new_fare)
            print("The fare when the taxi is moving is now: " + str(self.__fare_moving) + " cents.")
            self.__logger.get_log().debug(f"New moving fare: {self.__fare_moving}")
        else:
            self.__error(Error.FARE_CANNOT_BE_CHANGED)

    def __start(self):
        """
        Starts the taximeter only if the status is WAITING. Sets the
        status to STOPPED and reset the seconds counter

        :return:
        """
        self.__logger.get_log().debug("In Taximeter.start")
        if self.__status == Status.WAITING:
            self.__status = Status.STOPPED
            self.__start_time = time.time()
        else:
            self.__error(Error.TRIP_IN_PROGRESS)

    def __move(self):
        """
        Sets the status to MOVING only if status is STOPPED.

        Adds the total number of seconds to the stopped counter and
        resets the seconds counter

        :return:
        """
        self.__logger.get_log().debug("In Taximeter.move")
        if self.__status == Status.STOPPED:
            self.__stop_time = time.time()
            self.__seconds_stopped = self.__seconds_stopped + (self.__stop_time - self.__start_time)
            self.__status = Status.MOVING
            self.__start_time = time.time()
        else:
            self.__error(Error.TAXI_IS_NOT_STOPPED)

    def __stop(self):
        """
        Set the status to STOPPED only the status is MOVING.

        Adds the total number of seconds to the moving counter and
        reset the seconds counter

        :return:
        """
        self.__logger.get_log().debug("In Taximeter.stop")
        if self.__status == Status.MOVING:
            self.__stop_time = time.time()
            self.__seconds_moving = self.__seconds_moving + (self.__stop_time - self.__start_time)
            self.__status = Status.STOPPED
            self.__start_time = time.time()
        else:
            self.__error(Error.TAXI_IS_NOT_MOVING)

    def __end(self):
        """
        Set the status to WAITING if the status is STOPPED. if the status
        is MOVING, call the stop() method.

        Computes the total number of seconds stopped, display the total number
        of seconds moving and stopped and the total amount to pay in €.

        :return:
        """
        self.__logger.get_log().debug("In Taximeter.end")
        if self.__status == Status.MOVING:
            self.__stop()

        if self.__status == Status.STOPPED:
            self.__stop_time = time.time()
            self.__seconds_stopped = self.__seconds_stopped + (self.__stop_time - self.__start_time)
            self.__status = Status.WAITING
            self.__total_fare = self.__calculate_fare()
            print(f"\nSeconds taximeter was paused: {self.__seconds_stopped: .1f}")
            print(f"Seconds taximeter was running: {self.__seconds_moving: .1f}\n")
            print(f"Total to pay: {self.__total_fare: .2f}€")
            self.__logger.get_log().debug(f"{self.__total_fare: .2f}")
            self.__seconds_moving = 0
            self.__seconds_stopped = 0
            self.__total_fare = 0
        else:
            self.__error(Error.TAXI_IS_NOT_STOPPED)

    def __calculate_fare(self):
        """
        Computes the total amount to pay

        :return:
        """
        self.__logger.get_log().debug("In Taximeter.calculate_fare")
        return (self.__seconds_moving * self.__fare_moving + self.__seconds_stopped * self.__fare_stopped) / 100

    def __process_command(self, cmd):
        """
        Keeps processing commands entered by the user (or by the parameter cmd) till
        the command 'quit' is entered

        :param cmd: Command to process (used by unit testing)
        :return:
        """
        self.__logger.get_log().debug("In Taximeter.process_command")
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
            case "wait":
                time.sleep(int(cmd[1]))
            case "quit":
                if self.__status == Status.WAITING:
                    self.__status = Status.QUIT
            case "help":
                self.__show_commands()
            case _:
                self.__show_commands()
