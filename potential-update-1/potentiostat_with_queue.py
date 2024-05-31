from __future__ import print_function
import json
import threading
import queue as Queue
import potentiostat as ps


class PotentiostatWithQueue(ps.Potentiostat):

    def __init__(self, port, timeout=10.0, debug=False):
        super(PotentiostatWithQueue,self).__init__(port,timeout=timeout,debug=debug)
        self.data_queue = Queue.Queue()

    def get_default_volt_lims(self):
        volt_range = self.get_volt_range()
        volt_range_value = float(volt_range[:-1])
        volt_lims = -volt_range_value, volt_range_value
        return volt_lims


    def get_default_curr_lims(self):
        curr_range = self.get_curr_range()
        curr_range_value = float(curr_range[:-2])
        curr_lims = -curr_range_value, curr_range_value
        return curr_lims


    def get_curr_unit(self):
        curr_range = self.get_curr_range()
        curr_unit = curr_range[-2:]
        return curr_unit

    def receive_data(self,timeunit):

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