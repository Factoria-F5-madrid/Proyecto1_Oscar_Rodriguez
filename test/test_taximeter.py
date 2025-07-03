import unittest
import logging
import logging.config
from io import StringIO

from taximeter import Taximeter


def set_log(data):
    handler = logging.StreamHandler(data)
    handler.setLevel(logging.DEBUG)

    my_logger = logging.getLogger('Taximeter')
    my_logger.setLevel(logging.DEBUG)
    my_logger.addHandler(handler)

    return my_logger

class TestApplication(unittest.TestCase):
    def test_set_moving_fare(self):
        log_data = StringIO()
        taximeter = Taximeter(set_log(log_data))
        taximeter.run("fare_moving 20")
        taximeter.run("end")
        taximeter.run("quit")

        log = log_data.getvalue().split("\n")
        result = log[len(log) - 9].strip()

        self.assertEqual(result, "New moving fare: 20")

    def test_set_stopped_fare(self):
        log_data = StringIO()
        taximeter = Taximeter(set_log(log_data))
        taximeter.run("fare_stopped 10")
        taximeter.run("end")
        taximeter.run("quit")

        log = log_data.getvalue().split("\n")
        result = log[len(log) - 9].strip()

        self.assertEqual("New stopped fare: 10", result)

    def test_start_stopped_for_1_second(self):
        log_data = StringIO()
        taximeter = Taximeter(set_log(log_data))
        taximeter.run("start")
        taximeter.run("wait 1")
        taximeter.run("end")
        taximeter.run("quit")

        log = log_data.getvalue().split("\n")
        result = log[len(log) - 4].strip()
        self.assertEqual("0.02", result)

    def test_start_stopped_move_for_1_second(self):
        log_data = StringIO()
        taximeter = Taximeter(set_log(log_data))
        taximeter.run("start")
        taximeter.run("move")
        taximeter.run("wait 1")
        taximeter.run("stop")
        taximeter.run("end")
        taximeter.run("quit")

        log = log_data.getvalue().split("\n")
        result = log[len(log) - 4].strip()
        self.assertEqual("0.05", result)

    def test_error_moving_fare_cannot_be_changed(self):
        log_data = StringIO()
        taximeter = Taximeter(set_log(log_data))
        taximeter.run("start")
        taximeter.run("fare_moving 3")
        taximeter.run("quit")

        log = log_data.getvalue().split("\n")
        result = log[len(log) - 4]
        self.assertEqual("The fare cannot be changed once the trip has started.", result)

    def test_error_stopped_fare_cannot_be_changed(self):
        log_data = StringIO()
        taximeter = Taximeter(set_log(log_data))
        taximeter.run("start")
        taximeter.run("fare_stopped 3")
        taximeter.run("quit")

        log = log_data.getvalue().split("\n")
        result = log[len(log) - 4]
        self.assertEqual("The fare cannot be changed once the trip has started.", result)

    def test_error_moving_fare_amount_missing(self):
        log_data = StringIO()
        taximeter = Taximeter(set_log(log_data))
        taximeter.run("start")
        taximeter.run("fare_moving")
        taximeter.run("quit")

        log = log_data.getvalue().split("\n")
        result = log[len(log) - 4]
        self.assertEqual("The new fare amount is missing.", result)

    def test_error_stopped_fare_amount_missing(self):
        log_data = StringIO()
        taximeter = Taximeter(set_log(log_data))
        taximeter.run("start")
        taximeter.run("fare_stopped")
        taximeter.run("quit")

        log = log_data.getvalue().split("\n")
        result = log[len(log) - 4]
        self.assertEqual("The new fare amount is missing.", result)

    def test_error_trip_started(self):
        log_data = StringIO()
        taximeter = Taximeter(set_log(log_data))
        taximeter.run("start")
        taximeter.run("start")
        taximeter.run("quit")

        log = log_data.getvalue().split("\n")
        result = log[len(log) - 4]
        self.assertEqual("Cannot start a trip if there is already a trip in progress.", result)

    def test_error_trip_not_started(self):
        log_data = StringIO()
        taximeter = Taximeter(set_log(log_data))
        taximeter.run("end")
        taximeter.run("quit")

        log = log_data.getvalue().split("\n")
        result = log[len(log) - 4]
        self.assertEqual("Taximeter is not stopped, or trip is not started.", result)

if __name__ == "__main__":
    unittest.main()
