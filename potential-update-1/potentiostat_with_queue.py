from __future__ import print_function
import json
import threading
import queue as Queue
import potentiostat as ps

"""
PotentiostatWithQueue extends the Potentiostat class to add support for
asynchronous data collection using a queue. This class provides methods
to run tests, receive data from the device, and retrieve default voltage
and current limits.

Methods:
    __init__(port, timeout=10.0, debug=False): Initializes the object.
    get_default_volt_lims(): Returns default voltage limits.
    get_default_curr_lims(): Returns default current limits.
    get_curr_unit(): Returns the unit of current range.
    receive_data(timeunit): Continuously receives data from the device.
    run_test(testname, param=None, filename=None, timeunit='s'): Runs a test and collects data asynchronously.
"""

class PotentiostatWithQueue(ps.Potentiostat):


    def __init__(self, port, timeout=10.0, debug=False):
        """
        Initialize the PotentiostatWithQueue object, setting up the port, timeout,
        and debug options, and initializing the data queue.

        Args:
            port (str): The port to which the potentiostat is connected.
            timeout (float, optional): The timeout for communication. Default is 10.0 seconds.
            debug (bool, optional): Debug mode flag. Default is False.
        """
        super(PotentiostatWithQueue,self).__init__(port,timeout=timeout,debug=debug)
        self.data_queue = Queue.Queue()

    def get_default_volt_lims(self):
        """
        Get the default voltage limits based on the voltage range of the device.

        Returns:
            tuple: A tuple containing the negative and positive voltage limits.
        """
        volt_range = self.get_volt_range()
        volt_range_value = float(volt_range[:-1])
        volt_lims = -volt_range_value, volt_range_value
        return volt_lims


    def get_default_curr_lims(self):
        """
        Get the default current limits based on the current range of the device.

        Returns:
            tuple: A tuple containing the negative and positive current limits.
        """
        curr_range = self.get_curr_range()
        curr_range_value = float(curr_range[:-2])
        curr_lims = -curr_range_value, curr_range_value
        return curr_lims


    def get_curr_unit(self):
        """
        Get the unit of the current range.

        Returns:
            str: The unit of the current range (e.g., 'uA', 'mA').
        """
        curr_range = self.get_curr_range()
        curr_unit = curr_range[-2:]
        return curr_unit

    def receive_data(self,timeunit):
        """
        Continuously receive data from the device while the test is running,
        decode the JSON data, and put it into the data queue.

        Args:
            timeunit (str): The unit of time for the collected data (e.g., 's' for seconds).
        """
        while self.test_running:
            # Get json data from the device
            sample_json = self.readline()
            sample_json = sample_json.strip()
            try:
                sample_dict = json.loads(sample_json.decode())
            except ValueError:
                continue
            # Put new values in data queue
            if len(sample_dict) > 0:
                tval = sample_dict[ps.TimeKey]*ps.TimeUnitToScale[timeunit]
                volt = sample_dict[ps.VoltKey]
                curr = sample_dict[ps.CurrKey]
                self.data_queue.put({'tval': tval, 'volt': volt, 'curr': curr})
            else:
                self.data_queue.put({})
                self.test_running = False

    def run_test(self, testname, param=None,filename=None, timeunit='s'):
        """
        Run the specified test with given parameters and collect data asynchronously.

        Args:
            testname (str): Name of the test.
            param (dict, optional): Parameters for the test.
            filename (str, optional): Filename to save the data (not used in this method).
            timeunit (str): Time unit for the collected data.
        """
        if timeunit not in ps.TimeUnitToScale:
            raise RuntimeError('uknown timeunit option {0}'.format(timeunit))
        if param is not None:
            self.set_param(testname,param)

        # Setup up working thread to collect data from device
        data_worker = threading.Thread(target=self.receive_data,args=(timeunit,))
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