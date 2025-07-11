# Taximeter
This is a simple taximeter application. It allows the user to start the taximeter (this
simulates the case when a new customer gets into the taxi), change the status of the 
taximeter from stopped (taxi is not moving) to moving (taxi is moving) and to end the 
taximeter (simulates the customer getting out of the taxi and paying the fare). It also allows
to change the default fares for when the taxi is moving or stopped to new fares.

The taximeter has a log system to keep track of the events that occur in the application. In addition, 
any error messages are also displayed on the screen. Classes and Enums have been used to code the
application.

## Running the application
Please clone this repo in your computer (follow github instructions) and create a virtual environment using
the following command:

`bash-5.2$ python3 -m venv .venv`

Once the virtual environment has been created, activate it:

`bash-5.2$ source .venv/bin/activate`

If everything is fine, you should see something similar to this:

```
bash-5.2$ source .venv/bin/activate
(.venv) bash-5.2
``` 
Install the requirements:

`(.venv) bash-5.2$ pip install -r requirements.txt `

No errors should appear. Once the requirements have been installed, you can run the application:

`python main.py`

You should see the following on your terminal window:

```
(.venv) bash-5.2$ python main.py 
Welcome to the taximeter application.

The following commands are available:

- fare_stopped <number>. Sets the amount in cents per second that the customer will be
                         charged when the taxi is not moving. The default is: 2 cents.
- fare_moving <number>.  Sets the amount in cents per second that the customer will be
                         charged when the taxi is moving. The default is: 5 cents.
- start.                 New trip. Taximeter is stopped
- move.                  Taximeter is moving.
- stop.                  Taximeter is stopped.
- end.                   Trip is completed. Total fare is calculated and displayed.
- quit.                  Ends the application. Taximeter must be in waiting status.
- help.                  Shows list of commands.

Please enter a command (trip not started): 
```
From here you can play with the taximeter application. Have fun!

## Run the unit tests
We are assuming that the user has already cloned the repository, created a virtual environment, activated it
and installed the requirements. If not, please check [Running the application](#running-the-application) section.

To run the unit tests, run the following command from the command line:

`bash-5.2$ pytest`

Where "test" is the directory where the test files are located. If all the tests are executed
fine, you should see something like this (don't forget to activate the virtual environment):

```
(.venv) bash-5.2$ pytest
================================= test session starts =================================
platform linux -- Python 3.13.3, pytest-8.4.1, pluggy-1.6.0
rootdir: /home/oscarro/Development/IA/Modulo1/Proyecto1_Oscar_Rodriguez
collected 10 items                                                                    

test/test_taximeter.py ..........                                               [100%]

================================= 10 passed in 2.02s ==================================
```

If any of the tests fail, you should see something like this. Check the output for information about
the error or errors:

```
(.venv) bash-5.2$ pytest
.
.
.
=============================== short test summary info ===============================
FAILED test/test_taximeter.py::TestApplication::test_set_moving_fare - AssertionError: 
assert 'New moving fare: 20' == 'New moving fare: 201'
============================= 1 failed, 9 passed in 2.07s =============================
```

## The code
The structure of the code looks like this:

```commandline
.
├── lib
│   ├── error.py
│   ├── logger.py
│   └── status.py
├── LICENSE
├── main.py
├── README.md
├── taximeter.log
├── taximeter.py
└── test
    ├── __init__.py
    └── test_taximeter.py
```

### The `lib` directory
The `lib` directory contains utilities and libraries used by the application. For the taximeter
application there are two libs:

- `error.py` This is an enum type that contains all the error codes the application supports,
and the method to log the error with an explanation message.
- `status.py` This is another enum type that contains all the possible statuses the application
can take, plus a method to show the current status in the application. There is an extra status
called `QUIT` that will be used to indicate the user wants to exit from the application.

### The `test` directory
The `test` directory has all the code related to unit testing the application (see [Run the unit tests](#run-the-unit-tests)
in the documentation.)

### The `main` directory
The main directory has to files (plus the log file if the application has been run at least once),
the main program file (`main.py`) and a file that implements the taximeter application (`taximeter.py`).

The `main.py`creates the log that will be used in the application, prints a welcome message and then
initializes the taximeter calling the class defined in `taximeter.py` passing the log created
previously and then starts running the taximeter. When the taximeter ends its execution, a farewell
message is displayed. The log writes to a file (log level DEBUG) and to the console (log level ERROR).

The `taximeter.py` creates a class called `Taximeter` that implementes the taximeter. All the properties
and methods in the class are private except for the one that starts the taximeter.
