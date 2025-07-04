import unittest

from lib.logger import Logger
from taximeter import Taximeter


class TestApplication(unittest.TestCase):
    logger = Logger()

    def test_set_moving_fare(self):
        taximeter = Taximeter(self.logger)
        taximeter.run("fare_moving 20")
        taximeter.run("end")
        taximeter.run("quit")

        log = self.logger.get_log_data().getvalue().split("\n")
        result = log[len(log) - 9].strip()

        self.assertEqual(result, "New moving fare: 20")

    def test_set_stopped_fare(self):
        taximeter = Taximeter(self.logger)
        taximeter.run("fare_stopped 10")
        taximeter.run("end")
        taximeter.run("quit")

        log = self.logger.get_log_data().getvalue().split("\n")
        result = log[len(log) - 9].strip()

        self.assertEqual("New stopped fare: 10", result)

    def test_start_stopped_for_1_second(self):
        taximeter = Taximeter(self.logger)
        taximeter.run("start")
        taximeter.run("wait 1")
        taximeter.run("end")
        taximeter.run("quit")

        log = self.logger.get_log_data().getvalue().split("\n")
        result = log[len(log) - 4].strip()
        self.assertEqual("0.02", result)

    def test_start_stopped_move_for_1_second(self):
        taximeter = Taximeter(self.logger)
        taximeter.run("start")
        taximeter.run("move")
        taximeter.run("wait 1")
        taximeter.run("stop")
        taximeter.run("end")
        taximeter.run("quit")

        log = self.logger.get_log_data().getvalue().split("\n")
        result = log[len(log) - 4].strip()
        self.assertEqual("0.05", result)

    def test_error_moving_fare_cannot_be_changed(self):
        taximeter = Taximeter(self.logger)
        taximeter.run("start")
        taximeter.run("fare_moving 3")
        taximeter.run("quit")

        log = self.logger.get_log_data().getvalue().split("\n")
        result = log[len(log) - 4]
        self.assertEqual("The fare cannot be changed once the trip has started.", result)

    def test_error_stopped_fare_cannot_be_changed(self):
        taximeter = Taximeter(self.logger)
        taximeter.run("start")
        taximeter.run("fare_stopped 3")
        taximeter.run("quit")

        log = self.logger.get_log_data().getvalue().split("\n")
        result = log[len(log) - 4]
        self.assertEqual("The fare cannot be changed once the trip has started.", result)

    def test_error_moving_fare_amount_missing(self):
        taximeter = Taximeter(self.logger)
        taximeter.run("start")
        taximeter.run("fare_moving")
        taximeter.run("quit")

        log = self.logger.get_log_data().getvalue().split("\n")
        result = log[len(log) - 4]
        self.assertEqual("The new fare amount is missing.", result)

    def test_error_stopped_fare_amount_missing(self):
        taximeter = Taximeter(self.logger)
        taximeter.run("start")
        taximeter.run("fare_stopped")
        taximeter.run("quit")

        log = self.logger.get_log_data().getvalue().split("\n")
        result = log[len(log) - 4]
        self.assertEqual("The new fare amount is missing.", result)

    def test_error_trip_started(self):
        taximeter = Taximeter(self.logger)
        taximeter.run("start")
        taximeter.run("start")
        taximeter.run("quit")

        log = self.logger.get_log_data().getvalue().split("\n")
        result = log[len(log) - 4]
        self.assertEqual("Cannot start a trip if there is already a trip in progress.", result)

    def test_error_trip_not_started(self):
        taximeter = Taximeter(self.logger)
        taximeter.run("end")
        taximeter.run("quit")

        log = self.logger.get_log_data().getvalue().split("\n")
        result = log[len(log) - 4]
        self.assertEqual("Taximeter is not stopped, or trip is not started.", result)

if __name__ == "__main__":
    unittest.main()
