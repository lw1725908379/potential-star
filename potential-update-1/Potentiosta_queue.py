from __future__ import print_function
import json
import threading
import queue as Queue
import potentiostat as ps

"""
Potentiostat Queue Module

This module extends the functionality of the Potentiostat class to include
asynchronous data reception using a queue. The main functionalities include:

    1. Initializing a Potentiostat object with queue functionality.
    2. Running a test on the potentiostat and collecting data asynchronously.
    3. Storing the received data in a queue for further processing.

Classes:
    PotentiostatWithQueue - A subclass of Potentiostat with queue functionality.

Usage Example:
    potentiostat = PotentiostatWithQueue(port='/dev/ttyUSB0')
    potentiostat.run_test(testname='cyclic', param=test_params)
"""

class PotentiostatWithQueue(ps.Potentiostat):

    """
    A subclass of Potentiostat class with queue functionality for receiving data asynchronously.
    """

    def __init__(self, port, timeout=10.0, debug=False):
        """
                Initialize PotentiostatWithQueue object.

                Args:
                    port (str): The port where the potentiostat is connected.
                    timeout (float): The timeout for communication in seconds. Defaults to 10.0.
                    debug (bool): Flag for enabling debug mode. Defaults to False.

                Attributes:
                    data_queue (Queue.Queue): A queue to store received data asynchronously.
        """
        super(PotentiostatWithQueue, self).__init__(port, timeout=timeout, debug=debug)
        self.data_queue = Queue.Queue()


    def receive_data(self, timeunit):
        """
        Receive data from the device asynchronously and put it into the data queue.

        Args:
            timeunit (str): The time unit for scaling the time values.
        """

        while self.test_running:
            # Get json data (bytes type) from the device
            sample_json = self.readline()
            sample_json = sample_json.strip()
            try:
                # json to utf-8(default) to dict
                sample_dict = json.loads(sample_json.decode())
            except ValueError:
                continue
            # Put new values in data queue
            if len(sample_dict) > 0:
                tval = sample_dict[ps.TimeKey] * ps.TimeUnitToScale[timeunit]
                volt = sample_dict[ps.VoltKey]
                curr = sample_dict[ps.CurrKey]
                self.data_queue.put({'tval': tval, 'volt': volt, 'curr': curr})
            else:
                # Put empty dict if no data received
                self.data_queue.put({})
                # Stop receiving data if no data received
                self.test_running = False


    def run_test(self, testname, param=None, timeunit='s'):
    # def run_test(self, testname, param=None, filename=None, volt_lims=None, curr_lims=None, timeunit='s'):
        """
            Run a test on the potentiostat and start receiving data asynchronously.

            Args:
                testname (str): The name of the test to run.
                param (dict, optional): The parameters for the test.
                timeunit (str, optional): The time unit for scaling the time values. Defaults to 's'.
        """
        if timeunit not in ps.TimeUnitToScale:
            raise RuntimeError('uknown timeunit option {0}'.format(timeunit))

        if param is not None:
            self.set_param(testname, param)

        # Get the test completion time, t_done is the converted time value
        # Call get_test_done_time method to calculate the total time required for the test based on testname, and convert it according to timeunit
        t_done = self.get_test_done_time(testname, timeunit=timeunit)

        # Set up a background thread to collect data from the device
        # Create a new thread, the target function is self.receive_data, passing timeunit as an argument
        data_worker = threading.Thread(target=self.receive_data, args=(timeunit,))
        # Set the thread as a daemon thread, which means it will automatically end when the main program exits
        data_worker.daemon = True
        self.data_queue = Queue.Queue()

        # Send command to run the test
        cmd_dict = {
            ps.CommandKey: ps.RunTestCmd,
            ps.TestKey: testname
        }
        msg_dict = self.send_cmd(cmd_dict)
        self.test_running = True
        data_worker.start()
