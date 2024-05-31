import tkinter as tk
from tkinter import ttk
from tkinter import Menu
import serial
import serial.tools.list_ports
import sys
from tkinter import Menu
import tkinter as tk
from tkinter import messagebox as msg
# from potentiostat import Potentiostat
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from threading import Thread
import threading
from tkinter import filedialog, dialog
from time import sleep
import scipy
import os
# from potentiostat_live_plot3 import *
import potentiostat as ps
import matplotlib.pyplot as plt
import json
import queue as Queue
from Potentiosta_queue import *
from matplotlib import style

style.use("ggplot")


def handler(event, comb, frames):
    index = comb.current()
    for i in frames:
        i.grid_forget()
    frames[index].grid(column=0, row=4, padx=20, pady=20)


# Create instance
win = tk.Tk()

# Add a title
win.title("Electrochamical Potentiostat")
# w = win.winfo_screenwidth()
# h = win.winfo_screenheight()
win.geometry("450x650+350+50")
win.resizable(0,0)
file_path = ''
global number, number2, name, name1, name2, name3, name4, name5, name6, number7, number22, name24, name26, name28, name29, name211, number32, name34, \
    name36, name38, name39, name310, name312, number42, name44, name46, name48, name49, name410, name411, number52, name54, name56, \
    name58, name59, name511, name512, name513, name514, number62, name60, name61, name62, name63, name64, name65, name66, name67, checkVar1, \
    checkVar2, checkVar3, curr_unit,C_range
C_range = tk.StringVar()
number = tk.StringVar(value="cyclic")
number2 = tk.StringVar(value='10-4')
name = tk.IntVar(value="100")
name1 = tk.IntVar(value="0")
name2 = tk.DoubleVar(value="0")
name3 = tk.DoubleVar(value="-1")
name4 = tk.DoubleVar(value="1")
name5 = tk.DoubleVar(value="0.5")
name6 = tk.IntVar(value="1")
name7 = tk.DoubleVar(value="1")
number22 = tk.StringVar(value='10-4')
name24 = tk.IntVar(value="100")
name26 = tk.IntVar(value="0")
name28 = tk.DoubleVar(value="0")
name29 = tk.DoubleVar(value="0")
name211 = tk.IntVar(value="0")
number32 = tk.StringVar(value='10-4')
name34 = tk.IntVar(value="100")
name36 = tk.IntVar(value="0")
name38 = tk.DoubleVar(value="0")
name39 = tk.IntVar(value="0")
name310 = tk.DoubleVar(value="0")
name311 = tk.IntVar(value='0')
name312 = tk.DoubleVar(value="0")
number42 = tk.StringVar(value='10-4')
name44 = tk.IntVar(value="0")
name46 = tk.IntVar(value="0")
name48 = tk.DoubleVar(value="0")
name49 = tk.DoubleVar(value="0")
name410 = tk.DoubleVar(value="0")
name411 = tk.IntVar(value="0")
number52 = tk.StringVar(value='10-4')
name54 = tk.IntVar(value="100")
name56 = tk.IntVar(value="0")
name58 = tk.DoubleVar(value="0")
name59 = tk.IntVar(value="1")
name511 = tk.DoubleVar(value="0")
name512 = tk.DoubleVar(value="0")
name513 = tk.DoubleVar(value="0")
name514 = tk.IntVar(value="0")

number62 = tk.StringVar(value='10-4')
name60 = tk.IntVar(value="100")
name61 = tk.IntVar(value="0")
name62 = tk.DoubleVar(value="0")
name63 = tk.DoubleVar(value="1")
name64 = tk.DoubleVar(value="0")
name65 = tk.DoubleVar(value="0")
name66 = tk.DoubleVar(value="0")
name67 = tk.DoubleVar(value="0")

checkVar1 = tk.IntVar()
checkVar2 = tk.IntVar()
checkVar3 = tk.IntVar()


# def saveData():

def savefile():
    global file_path
    file_path = filedialog.asksaveasfilename(title=u'Save file')
    if file_path is not None:
        dialog.Dialog(None, {'title': 'File Modified', 'text': 'Save file', 'bitmap': 'warning', 'default': 0,
                             'strings': ('OK', 'Cancle')})
        #        sf2=datatfile1.get('1.0',tk.END)

        #        a1=tk.String(sf)
    val = file_path
    val1.set(val)


tabControl = ttk.Notebook(win)
tab1 = ttk.Frame(tabControl)
tabControl.add(tab1, text='Potentiostat')
tabControl.pack(side='top', fill='both', expand=1)

def run_potentiostat():
    datafile = file_path
    test_name = number_chosen.get()
    port = Port_list.get()
    if test_name == "cyclic":
        sample_rate = name.get()
        volt_min = name3.get()
        volt_max = name4.get()
        volt_per_sec = name5.get()
        quiet_value = name2.get()
        quiet_time = name1.get()
        num_cycles = name6.get()
        volt_lims = [volt_min, volt_max]
        curr_range = C_range_chosen.get()
        # cur = int(curr_range[:-2])
        # curr_lims = [-cur, cur]
        curr_unit = curr_range[-2:]
        shift = name7.get()  # Waveform phase shift - expressed as [0,1] number
        if curr_range == "100nA" or curr_range == "60nA":
            cur = int(curr_range[:-2])/1000
        else:
            cur = int(curr_range[:-2])
        curr_lims = [-cur, cur]

        if volt_min > 10 or volt_min < -10:
            msg.showerror('Python Message Error Box',
                          '\nError: The V_init value should be between -10 to 10 V ')
        elif volt_max > 10 or volt_max < -10:
            msg.showerror('Python Message Error Box',
                          "\nError: The V_end value should be between -10 to 10 V ")
       #elif volt_min > volt_max:
       #     msg.showerror('Python Message Error Box',
       #                   '\nError: The V_init value should be smaller than V_end ')
        elif sample_rate == 0:
            msg.showerror('Python Message Error Box',
                          '\nError: please input the sample rate ')
        elif num_cycles == 0:
            msg.showerror('Python Message Error Box',
                          '\nError: please input the cycle number')
        elif volt_per_sec == 0.0:
            msg.showerror('Python Message Error Box',
                          '\nError: please input V_per_sec')
        elif datafile == None:
            msg.showerror('Python Message Error Box',
                          '\nError: please input flie path and file name')
        else:
            amplitude = (volt_max - volt_min) / 2.0  # Waveform peak amplitude (V)
            offset = (volt_max + volt_min) / 2.0  # Waveform offset (V)
            period_ms = int(1000 * 4 * amplitude / volt_per_sec)  # Waveform period in (ms)
            dev = PotentiostatWithQueue(port=port)
            dev.set_curr_range(curr_range)
            dev.set_sample_rate(sample_rate)
            # global test_param
            test_param = {
                'quietValue': quiet_value,
                'quietTime': quiet_time,
                'amplitude': amplitude,
                'offset': offset,
                'period': period_ms,
                'numCycles': num_cycles,
                'shift': shift,
            }
            # global dev
            dev.set_param(test_name, test_param)
            # global t_done
            test_done_tval = dev.get_test_done_time(test_name, timeunit='ms')
            t_done = test_done_tval / 1000
            print(test_done_tval,curr_range)

            # Create figure and live plot
            fig = plt.figure(figsize=(8, 8), dpi=100)
            plt.ion()
            ax1 = plt.subplot(211)
            volt_line, = plt.plot([0], [0], "b")
            plt.xlim(0, t_done)
            plt.ylim(*volt_lims)
            plt.grid('on')
            plt.ylabel('Potention (V)')
            plt.xlabel('t (s)')
            plt.title('Potentiostat Live Plot')
            ax3 = plt.subplot(212)
            curr_line, = plt.plot([0], [0], "b")
            plt.xlim(*volt_lims)
            plt.ylim(*curr_lims)
            # plt.autoscale(enable=True,axis="both",tight=True)
            plt.grid('on')
            plt.xlabel('Potention (V)')
            plt.ylabel('Current (uA)')
            fig.canvas.flush_events()
            plt.pause(0.001)
            # Lists for incoming data
            tval_list = []
            volt_list = []
            curr_list = []
            filename = datafile

            # Start test
            done = False
            dev.run_test(test_name)
            if filename is not None:
                fid = open(filename, 'w')
            while not done:
                # Get data from queue and add store for plotting
                have_new_data = False
                while True:

                    try:
                        data = dev.data_queue.get(False)
                    except Queue.Empty:
                        break

                    if data:
                        tval = data['tval']
                        volt = data['volt']
                        curr = data['curr']
                        print('{0:1.3f}, {1:1.4f}, {2:1.4f}'.format(tval, volt, curr))
                        tval_list.append(tval)
                        volt_list.append(volt)
                        curr_list.append(curr)
                        # Write data to file
                        if filename is not None:
                            fid.write('{0:1.3f}, {1:1.4f}, {2:1.4f}\n'.format(tval, volt, curr))
                        have_new_data = True
                    else:
                        done = True
                        break
                # # Update live plot
                if have_new_data:
                    volt_line.set_xdata(tval_list)
                    volt_line.set_ydata(volt_list)
                    curr_line.set_xdata(volt_list)
                    curr_line.set_ydata(curr_list)
                    fig.canvas.flush_events()
                    plt.pause(0.001)
                    plt.show()
            dev.atexit_cleanup()
            dev.close()
        print(test_name, port, volt_max, volt_min, volt_per_sec, shift, num_cycles, quiet_time, quiet_value,
              curr_range, sample_rate)

    # ##############################################################
    elif test_name == "constant voltage":
        test_name = 'constant'
        sample_rate = name24.get()
        quiet_value = name28.get()
        quiet_time = name26.get()
        curr_range = C_range_chosen.get()
        duration = name211.get()
        value = name29.get()
        val1 = value * 0.5
        val2 = value / 0.5
        port = Port_list.get()
        # cur = int(curr_range[:-2])
        # curr_lims = [-cur, cur]
        curr_unit = curr_range[-2:]
        volt_lims = [val1, val2]
        if curr_range == "100nA" or curr_range == "60nA":
            cur = int(curr_range[:-2]) / 1000
        else:
            cur = int(curr_range[:-2])
        curr_lims = [-cur, cur]

        if value > 10 or value < -10:
            msg.showerror('Python Message Error Box',
                          '\nError: The Voltage value should be between -10 to 10 V ')
        elif sample_rate == 0:
            msg.showerror('Python Message Error Box',
                          '\nError: please input the sample rate ')
        elif datafile is None:
            msg.showerror('Python Message Error Box',
                          '\nError: please input flie path and file name')

        else:

            dev = PotentiostatWithQueue(port=port)
            dev.set_curr_range(curr_range)
            dev.set_sample_rate(sample_rate)
            test_param = {
                'quietValue': quiet_value,  # Output voltage during quiet peroid
                'quietTime': quiet_time,  # Duration of quiet period (ms)
                'value': value,  # Output volatage (V) durring constant voltag~Q锛乣`e test
                'duration': duration,  # Duration of constant voltage test (ms)
            }
            dev.set_param(test_name, test_param)
            test_done_tval = dev.get_test_done_time(test_name, timeunit='ms')
            t_done = test_done_tval / 1000

            fig = plt.figure(figsize=(8, 8), dpi=100)
            plt.ion()

            ax1 = plt.subplot(211)
            volt_line, = plt.plot([0], [0], "b")
            plt.xlim(0, t_done)
            plt.ylim(*volt_lims)
            plt.grid('on')
            plt.ylabel('Potention (V)')
            plt.xlabel('t (s)')
            plt.title('Potentiostat Live Plot')

            ax2 = plt.subplot(212)
            ct_line, = plt.plot([0], [0], "b")
            plt.xlim(0, t_done)
            plt.ylim(*curr_lims)
            plt.grid('on')
            plt.xlabel('t (s)')
            plt.ylabel('Current (uA)')

            fig.canvas.flush_events()
            plt.pause(0.001)

            # Lists for incoming data
            tval_list = []
            volt_list = []
            curr_list = []
            filename = datafile

            # Start test
            done = False
            dev.run_test(test_name)
            if filename is not None:
                fid = open(filename, 'w')
            while not done:
                # Get data from queue and add store for plotting
                have_new_data = False
                while True:

                    try:
                        data = dev.data_queue.get(False)
                    except Queue.Empty:
                        break

                    if data:
                        tval = data['tval']
                        volt = data['volt']
                        curr = data['curr']
                        print('{0:1.3f}, {1:1.4f}, {2:1.4f}'.format(tval, volt, curr))
                        tval_list.append(tval)
                        volt_list.append(volt)
                        curr_list.append(curr)
                        # Write data to file
                        if filename is not None:
                            fid.write('{0:1.3f}, {1:1.4f}, {2:1.4f}\n'.format(tval, volt, curr))
                        have_new_data = True
                    else:
                        done = True
                        break
                # # Update live plot
                if have_new_data:
                    volt_line.set_xdata(tval_list)
                    volt_line.set_ydata(volt_list)
                    ct_line.set_xdata(tval_list)
                    ct_line.set_ydata(curr_list)
                    fig.canvas.flush_events()
                    plt.pause(0.001)
                    plt.show()
            dev.atexit_cleanup()
            dev.close()
        print(test_name, sample_rate, quiet_value, quiet_time, value, duration, port, curr_range)

    elif test_name == "chronoamperometry":
        test_name = test_name[0:9]
        sample_rate = name34.get()
        quiet_value = name38.get()
        quiet_time = name36.get()
        curr_range = C_range_chosen.get()
        duration1 = name39.get()
        value1 = name310.get()
        duration2 = name311.get()
        value2 = name312.get()
        port = Port_list.get()
        val1 = max(value1, value2) / 0.5
        val2 = min(value1, value2) * 0.5
        # cur = int(curr_range[:-2])
        curr_unit = curr_range[-2:]
        volt_lims = [val2, val1]
        # curr_lims = [-cur, cur]
        if curr_range == "100nA" or curr_range == "60nA":
            cur = int(curr_range[:-2]) / 1000
        else:
            cur = int(curr_range[:-2])
        curr_lims = [-cur, cur]
        if value1 > 10 or value1 < -10:
            msg.showerror('Python Message Error Box',
                          '\nError: The Voltage value should be between -10 to 10 V ')
        elif value2 > 10 or value2 < -10:
            msg.showerror('Python Message Error Box',
                          '\nError: The Voltage value should be between -10 to 10 V ')
        elif sample_rate == 0:
            msg.showerror('Python Message Error Box',
                          '\nError: please input the sample rate ')
        elif datafile is None:
            msg.showerror('Python Message Error Box',
                          '\nError: please input flie path and file name')

        else:
            dev = PotentiostatWithQueue(port=port)
            dev.set_curr_range(curr_range)
            dev.set_sample_rate(sample_rate)
            test_param = {
                'quietValue': quiet_value,  # Output voltage during quiet peroid
                'quietTime': quiet_time,  # Duration of quiet period (ms)
                'step': [(duration1, value1), (duration2, value2)]
                # Output volatage (V) durring constant voltag~Q锛乣`e test

            }
            # global dev
            dev.set_param(test_name, test_param)
            # global t_done
            test_done_tval = dev.get_test_done_time(test_name, timeunit='ms')
            t_done = test_done_tval / 1000

            # # Create figure and live plot
            fig = plt.figure(figsize=(8, 8), dpi=100)
            plt.ion()

            ax1 = plt.subplot(211)
            volt_line, = plt.plot([0], [0], "b")
            plt.xlim(0, t_done)
            plt.ylim(*volt_lims)
            plt.grid('on')
            plt.ylabel('Potention (V)')
            plt.xlabel('t (s)')
            plt.title('Potentiostat Live Plot')

            ax2 = plt.subplot(212)
            ct_line, = plt.plot([0], [0], "b")
            plt.xlim(0, t_done)
            plt.ylim(*curr_lims)
            plt.grid('on')
            plt.xlabel('t (s)')
            plt.ylabel('Current (uA)')

            fig.canvas.flush_events()
            plt.pause(0.001)

            # Lists for incoming data
            tval_list = []
            volt_list = []
            curr_list = []
            filename = datafile

            # Start test
            done = False
            dev.run_test(test_name)
            if filename is not None:
                fid = open(filename, 'w')
            while not done:
                # Get data from queue and add store for plotting
                have_new_data = False
                while True:

                    try:
                        data = dev.data_queue.get(False)
                    except Queue.Empty:
                        break

                    if data:
                        tval = data['tval']
                        volt = data['volt']
                        curr = data['curr']
                        print('{0:1.3f}, {1:1.4f}, {2:1.4f}'.format(tval, volt, curr))
                        tval_list.append(tval)
                        volt_list.append(volt)
                        curr_list.append(curr)
                        # Write data to file
                        if filename is not None:
                            fid.write('{0:1.3f}, {1:1.4f}, {2:1.4f}\n'.format(tval, volt, curr))
                        have_new_data = True
                    else:
                        done = True
                        break
                # # Update live plot
                if have_new_data:
                    volt_line.set_xdata(tval_list)
                    volt_line.set_ydata(volt_list)
                    ct_line.set_xdata(tval_list)
                    ct_line.set_ydata(curr_list)
                    fig.canvas.flush_events()
                    plt.pause(0.001)
                    plt.show()
            dev.atexit_cleanup()
            dev.close()
        print(test_name, sample_rate, quiet_time, quiet_value, duration1, value1, duration2, value2)
    elif test_name == "linear sweep":
        test_name = "linearSweep"
        sample_rate = name44.get()
        quiet_value = name48.get()
        quiet_time = name46.get()
        curr_range = C_range_chosen.get()
        duration = name411.get()
        startValue = name49.get()
        finalValue = name410.get()
        sta = max(startValue, finalValue)
        fin = min(startValue, finalValue)
        port = Port_list.get()
        # cur = int(curr_range[:-2])
        curr_unit = curr_range[-2:]
        volt_lims = [fin, sta]
        # curr_lims = [-cur, cur]
        if curr_range == "100nA" or curr_range == "60nA":
            cur = int(curr_range[:-2]) / 1000
        else:
            cur = int(curr_range[:-2])
        curr_lims = [-cur, cur]
        if startValue > 10 or startValue < -10:
            msg.showerror('Python Message Error Box',
                          '\nError: The startValue value should be between -10 to 10 V ')
        elif finalValue > 10 or finalValue < -10:
            msg.showerror('Python Message Error Box',
                          "\nError: The finalValue value should be between -10 to 10 V ")
        elif sample_rate == 0:
            msg.showerror('Python Message Error Box',
                          '\nError: please input the sample rate ')
        elif datafile is None:
            msg.showerror('Python Message Error Box',
                          '\nError: please input flie path and file name')
        else:
            dev = PotentiostatWithQueue(port=port)
            dev.set_curr_range(curr_range)
            dev.set_sample_rate(sample_rate)
            test_param = {
                'quietTime': quiet_time,
                'quietValue': quiet_value,
                'startValue': startValue,
                'finalValue': finalValue,
                'duration': duration,
            }
            dev.set_param(test_name, test_param)
            # global t_done
            # test_done_tval = dev.get_test_done_time(test_name, timeunit='ms')
            # t_done = test_done_tval / 1000
            # Create figure and live plot
            fig = plt.figure(figsize=(8, 8), dpi=100)
            plt.ion()
            ax3 = plt.subplot(111)
            curr_line, = plt.plot([0], [0], "b")
            plt.xlim(*volt_lims)
            plt.ylim(*curr_lims)
            plt.grid('on')
            plt.xlabel('Potential (V)')
            plt.ylabel('Current (uA)')
            plt.title('Potentiostat Live Plot')

            fig.canvas.flush_events()
            plt.pause(0.001)

            # Lists for incoming data
            tval_list = []
            volt_list = []
            curr_list = []
            filename = datafile

            # Start test
            done = False
            dev.run_test(test_name)
            if filename is not None:
                fid = open(filename, 'w')
            while not done:
                # Get data from queue and add store for plotting
                have_new_data = False
                while True:

                    try:
                        data = dev.data_queue.get(False)
                    except Queue.Empty:
                        break

                    if data:
                        tval = data['tval']
                        volt = data['volt']
                        curr = data['curr']
                        print('{0:1.3f}, {1:1.4f}, {2:1.4f}'.format(tval, volt, curr))
                        tval_list.append(tval)
                        volt_list.append(volt)
                        curr_list.append(curr)
                        # Write data to file
                        if filename is not None:
                            fid.write('{0:1.3f}, {1:1.4f}, {2:1.4f}\n'.format(tval, volt, curr))
                        have_new_data = True
                    else:
                        done = True
                        break
                # # Update live plot
                if have_new_data:
                    curr_line.set_xdata(volt_list)
                    curr_line.set_ydata(curr_list)
                    fig.canvas.flush_events()
                    plt.pause(0.001)
                    plt.show()
            dev.atexit_cleanup()
            dev.close()
        print(test_name, sample_rate, quiet_value, quiet_time, curr_range, duration, startValue, finalValue, port)
    #     ##############################################################
    elif test_name == "sinusoid":
        sample_rate = name54.get()
        amplitude = name511.get()
        num_cycles = name59.get()
        quiet_value = name58.get()
        quiet_time = name56.get()
        offset = name512.get()
        shift = name513.get()  # 0 = no phase shift, 0.5 = 180 deg phase shift, etc.
        period = name514.get()
        curr_range = C_range_chosen.get()
        amp = (amplitude + offset) / 0.8
        # cur = int(curr_range[:-2])
        curr_unit = curr_range[-2:]
        volt_lims = [-amp, amp]
        # curr_lims = [-cur, cur]
        port = Port_list.get()
        if curr_range == "100nA" or curr_range == "60nA":
            cur = int(curr_range[:-2]) / 1000
        else:
            cur = int(curr_range[:-2])
        curr_lims = [-cur, cur]
        if amplitude > 10 or amplitude < -10:
            msg.showerror('Python Message Error Box',
                          '\nError: The amplitude value should be between -10 to 10 V ')
        elif sample_rate == 0:
            msg.showerror('Python Message Error Box',
                          '\nError: please input the sample rate ')
        elif num_cycles == 0:
            msg.showerror('Python Message Error Box',
                          '\nError: please input the cycle number')
        elif datafile is None:
            msg.showerror('Python Message Error Box',
                          '\nError: please input flie path and file name')

        else:
            dev = PotentiostatWithQueue(port=port)
            dev.set_curr_range(curr_range)
            dev.set_sample_rate(sample_rate)
            # Create dictionary of waveform parameters for cyclic voltammetry test
            test_param = {
                'quietValue': quiet_value,
                'quietTime': quiet_time,
                'amplitude': amplitude,
                'offset': offset,
                'period': period,
                'numCycles': num_cycles,
                'shift': shift,
            }
            dev.set_param(test_name, test_param)
            test_done_tval = dev.get_test_done_time(test_name, timeunit='ms')
            t_done = test_done_tval / 1000
            # Create figure and live plot
            fig = plt.figure(figsize=(8, 8), dpi=100)
            plt.ion()

            ax1 = plt.subplot(311)
            volt_line, = plt.plot([0], [0], "b")
            plt.xlim(0, t_done)
            plt.ylim(*volt_lims)
            plt.grid('on')
            plt.ylabel('Potention (V)')
            plt.xlabel('t (s)')
            plt.title('Potentiostat Live Plot')

            ax3 = plt.subplot(313)
            curr_line, = plt.plot([0], [0], "b")
            plt.xlim(*volt_lims)
            plt.ylim(*curr_lims)
            plt.grid('on')
            plt.xlabel('Potention (V)')
            plt.ylabel('Current (uA)')

            ax2 = plt.subplot(312)
            ct_line, = plt.plot([0], [0], "b")
            plt.xlim(0, t_done)
            plt.ylim(*curr_lims)
            plt.grid('on')
            plt.xlabel('t (s)')
            plt.ylabel('Current (uA)')

            fig.canvas.flush_events()
            plt.pause(0.001)

            # Lists for incoming data
            tval_list = []
            volt_list = []
            curr_list = []
            filename = datafile

            # Start test
            done = False
            dev.run_test(test_name)
            if filename is not None:
                fid = open(filename, 'w')
            while not done:
                # Get data from queue and add store for plotting
                have_new_data = False
                while True:

                    try:
                        data = dev.data_queue.get(False)
                    except Queue.Empty:
                        break

                    if data:
                        tval = data['tval']
                        volt = data['volt']
                        curr = data['curr']
                        print('{0:1.3f}, {1:1.4f}, {2:1.4f}'.format(tval, volt, curr))
                        tval_list.append(tval)
                        volt_list.append(volt)
                        curr_list.append(curr)
                        # Write data to file
                        if filename is not None:
                            fid.write('{0:1.3f}, {1:1.4f}, {2:1.4f}\n'.format(tval, volt, curr))
                        have_new_data = True
                    else:
                        done = True
                        break
                # # Update live plot
                if have_new_data:
                    volt_line.set_xdata(tval_list)
                    volt_line.set_ydata(volt_list)
                    curr_line.set_xdata(volt_list)
                    curr_line.set_ydata(curr_list)
                    ct_line.set_xdata(tval_list)
                    ct_line.set_ydata(curr_list)
                    fig.canvas.flush_events()
                    plt.pause(0.001)
                    plt.show()
            # progress_bar.stop()
            dev.atexit_cleanup()
            dev.close()
        print(test_name, sample_rate, quiet_time, quiet_value, num_cycles, amplitude, shift, offset, period, curr_range,
              port)
    #     ###############################################################
    elif test_name == "squareWave":
        sample_rate = name60.get()
        quiet_value = name62.get()
        quiet_time = name61.get()
        curr_range = C_range_chosen.get()
        amplitude = name63.get()
        startValue = name64.get()
        finalValue = name65.get()
        stepValue = name66.get()
        window = name67.get()
        star = max(startValue, finalValue)
        fina = min(startValue, finalValue)
        # cur = int(curr_range[:-2])
        curr_unit = curr_range[-2:]
        volt_lims = [fina, star]
        # curr_lims = [-cur, cur]
        port = Port_list.get()
        if curr_range == "100nA" or curr_range == "60nA":
            cur = int(curr_range[:-2]) / 1000
        else:
            cur = int(curr_range[:-2])
        curr_lims = [-cur, cur]
        if startValue > 10 or startValue < -10:
            msg.showerror('Python Message Error Box',
                          '\nError: The startValue value should be between -10 to 10 V ')
        elif finalValue > 10 or finalValue < -10:
            msg.showerror('Python Message Error Box',
                          "\nError: The finalValue value should be between -10 to 10 V ")
        elif sample_rate == 0:
            msg.showerror('Python Message Error Box',
                          '\nError: please input the sample rate ')
        elif datafile is None:
            msg.showerror('Python Message Error Box',
                          '\nError: please input flie path and file name')
        else:
            dev = PotentiostatWithQueue(port=port)
            dev.set_curr_range(curr_range)
            dev.set_sample_rate(sample_rate)
            test_param = {
                'quietValue': quiet_value,
                'quietTime': quiet_time,
                'amplitude': amplitude,
                'startValue': startValue,
                'finalValue': finalValue,
                'stepValue': stepValue,
                'window': window,
            }
            dev.set_param(test_name, test_param)
            test_done_tval = dev.get_test_done_time(test_name, timeunit='ms')
            t_done = test_done_tval / 1000

            # Create figure and live plot
            fig = plt.figure(figsize=(8, 8), dpi=100)
            plt.ion()

            ax3 = plt.subplot(111)
            curr_line, = plt.plot([0], [0], "b")
            plt.xlim(*volt_lims)
            plt.ylim(*curr_lims)
            plt.grid('on')
            plt.xlabel('Potention (V)')
            plt.ylabel('Current (uA)')

            fig.canvas.flush_events()
            plt.pause(0.001)

            # Lists for incoming data
            tval_list = []
            volt_list = []
            curr_list = []
            filename = datafile

            # Start test
            done = False
            dev.run_test(test_name)
            if filename is not None:
                fid = open(filename, 'w')
            while not done:
                # Get data from queue and add store for plotting
                have_new_data = False
                while True:

                    try:
                        data = dev.data_queue.get(False)
                    except Queue.Empty:
                        break

                    if data:
                        tval = data['tval']
                        volt = data['volt']
                        curr = data['curr']
                        print('{0:1.3f}, {1:1.4f}, {2:1.4f}'.format(tval, volt, curr))
                        tval_list.append(tval)
                        volt_list.append(volt)
                        curr_list.append(curr)
                        # Write data to file
                        if filename is not None:
                            fid.write('{0:1.3f}, {1:1.4f}, {2:1.4f}\n'.format(tval, volt, curr))
                        have_new_data = True
                    else:
                        done = True
                        break
                # # Update live plot
                if have_new_data:
                    curr_line.set_xdata(volt_list)
                    curr_line.set_ydata(curr_list)
                    fig.canvas.flush_events()
                    plt.pause(0.001)
                    plt.show()
            dev.atexit_cleanup()
            dev.close()
        print(test_name, sample_rate, quiet_value, quiet_time, startValue, finalValue, amplitude, stepValue, window)


def to_page1(master):
    master.grab_set()
    first(master)


def first(master):
    mighty = ttk.LabelFrame(master, text='', width=50, height=200)
    mighty.grid(column=0, row=0, padx=8, pady=4)

    mighty1 = ttk.LabelFrame(master, text='', width=50, height=200)
    mighty1.grid(column=0, row=13, padx=8, pady=4)

    # mighty2 = ttk.LabelFrame(master, text='', width=600, height=600)
    # mighty2.grid(column=100, row=0, rowspan=30, sticky="w")

    a_label = ttk.Label(mighty, text="Test methods")
    a_label.grid(column=0, row=1, padx=8, pady=2)

    c_label = ttk.Label(mighty, text="Current Range")
    c_label.grid(column=0, row=2, padx=8, pady=2)

    com_label = ttk.Label(mighty, text="COM")
    com_label.grid(column=0, row=0, padx=8, pady=2)

    ############################plot figure####################
    fig = Figure(figsize=(6, 6), facecolor='white')
    axis1 = fig.add_subplot(211)  # 2 rows, 1 column, Top graph
    # axis1.plot(t, volt)
    axis1.set_ylabel('potential (V)')
    axis1.set_xlabel('time (s)')
    axis1.grid(linestyle='-')  # solid grid lines
    axis2 = fig.add_subplot(212)  # 2 rows, 1 column, Top graph
    # axis2.plot(volt, curr)
    axis2.set_xlabel('potential (V)')
    axis2.set_ylabel('current (uA)')
    axis2.grid(linestyle='-')  # solid grid lines
    # can = FigureCanvasTkAgg(fig, master=mighty2)
    # can._tkcanvas.grid(column=0, row=0, sticky="w")
    #
    # can._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    # can.get_tk_widget().pack()
    # toolbar = NavigationToolbar2Tk(can, mighty2)
    # can.get_tk_widget().pack()

    # ttk.Label(frame1, text="Device_Port").grid(column=0, row=0, pady=2)
    # Adding a Textbox Entry widget
    global Port_list
    Port_list = tk.StringVar()
    Port_list = ttk.Combobox(mighty, width=12, textvariable=Port_list, state='readonly')
    ListPorts = list(serial.tools.list_ports.comports())
    Port_list['values'] = [i[0] for i in ListPorts]
    Port_list.current(0)
    Port_list.grid(column=1, row=0, padx=8, pady=2)

    global number, number2, name, name1, name2, name3, name4, name5, name6, name7, number22, name24, name26, name28, name29, name211, number32, name34, \
        name36, name38, name39, name310, name311, name312, number42, name44, name46, name48, name49, name410, name411, number52, name54, name56, \
        name58, name59, name511, name512, name513, name514, number62, name60, name61, name62, name63, name64, name65, name66, name67, checkVar1, \
        checkVar2, checkVar3, number_chosen, C_range_chosen,C_range

    number_chosen = ttk.Combobox(mighty, width=12, textvariable=number)
    number_chosen['values'] = (
    "cyclic", "constant voltage", "chronoamperometry", 'linear sweep', 'sinusoid', 'squareWave')
    number_chosen.bind('<<ComboboxSelected>>',
                       lambda event: handler(event, number_chosen, [frame1, frame2, frame3, frame4, frame5, frame6]))
    number_chosen.grid(column=1, row=1, padx=8, pady=2)
    number_chosen.current(0)

    C_range_chosen = ttk.Combobox(mighty, width=12, textvariable=C_range)
    C_range_chosen['values'] = ('60nA', '100nA', '1uA', '10uA', '100uA', '1000uA', '24000uA')
    C_range_chosen.bind('<<ComboboxSelected>>',
                       lambda event: handler(event, number_chosen, [frame1, frame2, frame3, frame4, frame5, frame6]))
    C_range_chosen.grid(column=1, row=2, padx=8, pady=2)
    C_range_chosen.current(3)

    # frame1
    frame1 = tk.Frame(master, width=50, height=500)
    frame1.grid(column=0, row=4, padx=8, pady=4)

    a_label = ttk.Label(frame1, text="Sample Rate(Hz)")
    a_label.grid(column=0, row=1, padx=2, pady=4)

    name_entered = ttk.Entry(frame1, width=12, textvariable=name)
    name_entered.grid(column=1, row=1, padx=2, pady=4)

    a_label1 = ttk.Label(frame1, text="Quiet Time(ms)")
    a_label1.grid(column=0, row=2, padx=2, pady=4)

    name_entered1 = ttk.Entry(frame1, width=12, textvariable=name1)
    name_entered1.grid(column=1, row=2, padx=2, pady=4)

    a_label2 = ttk.Label(frame1, text="Quiet Value(V)")
    a_label2.grid(column=0, row=3, pady=2)

    name_entered2 = ttk.Entry(frame1, width=12, textvariable=name2)
    name_entered2.grid(column=1, row=3, padx=2, pady=4)

    a_label3 = ttk.Label(frame1, text="Min Value(V)")
    a_label3.grid(column=0, row=4, padx=2, pady=4)

    name_entered3 = ttk.Entry(frame1, width=12, textvariable=name3)
    name_entered3.grid(column=1, row=4, padx=2, pady=4)

    a_label4 = ttk.Label(frame1, text="Max Value(V)")
    a_label4.grid(column=0, row=5, padx=2, pady=4)

    name_entered4 = ttk.Entry(frame1, width=12, textvariable=name4)
    name_entered4.grid(column=1, row=5, padx=2, pady=4)

    a_label5 = ttk.Label(frame1, text="Scan Rate(V/s)")
    a_label5.grid(column=0, row=6, padx=2, pady=4)

    name_entered5 = ttk.Entry(frame1, width=12, textvariable=name5)
    name_entered5.grid(column=1, row=6, padx=2, pady=4)

    a_label6 = ttk.Label(frame1, text="Cycles")
    a_label6.grid(column=0, row=7, padx=2, pady=4)

    name_entered6 = ttk.Entry(frame1, width=12, textvariable=name6)
    name_entered6.grid(column=1, row=7, padx=2, pady=4)

    a_label6 = ttk.Label(frame1, text="Shift")
    a_label6.grid(column=0, row=8, padx=2, pady=4)

    name_entered6 = ttk.Entry(frame1, width=12, textvariable=name7)
    name_entered6.grid(column=1, row=8, padx=2, pady=4)

    # frame2
    frame2 = tk.Frame(master, width=50, height=500)

    a_label23 = ttk.Label(frame2, text="Sample Rate(Hz)")
    a_label23.grid(column=0, row=1, padx=2, pady=4)

    name_entered24 = ttk.Entry(frame2, width=12, textvariable=name24)
    name_entered24.grid(column=1, row=1, padx=2, pady=4)

    a_label25 = ttk.Label(frame2, text="Quiet Time(ms)")
    a_label25.grid(column=0, row=2, padx=2, pady=4)

    name_entered26 = ttk.Entry(frame2, width=12, textvariable=name26)
    name_entered26.grid(column=1, row=2, padx=2, pady=4)

    a_label27 = ttk.Label(frame2, text="Quiet Value(V)")
    a_label27.grid(column=0, row=3, padx=2, pady=4)

    name_entered28 = ttk.Entry(frame2, width=12, textvariable=name28)
    name_entered28.grid(column=1, row=3, padx=2, pady=4)

    a_label29 = ttk.Label(frame2, text="Value(V)")
    a_label29.grid(column=0, row=4, padx=2, pady=4)

    name_entered29 = ttk.Entry(frame2, width=12, textvariable=name29)
    name_entered29.grid(column=1, row=4, padx=2, pady=4)

    a_label210 = ttk.Label(frame2, text="Duration(ms)")
    a_label210.grid(column=0, row=5, padx=2, pady=4)

    name_entered211 = ttk.Entry(frame2, width=12, textvariable=name211)
    name_entered211.grid(column=1, row=5, padx=2, pady=4)

    # frame3
    frame3 = tk.Frame(master, width=50, height=500)

    a_label33 = ttk.Label(frame3, text="Sample Rate(Hz)")
    a_label33.grid(column=0, row=1, padx=2, pady=4)

    name_entered34 = ttk.Entry(frame3, width=12, textvariable=name34)
    name_entered34.grid(column=1, row=1, padx=2, pady=4)

    a_label35 = ttk.Label(frame3, text="Quiet Time(ms)")
    a_label35.grid(column=0, row=2, padx=2, pady=4)

    name_entered36 = ttk.Entry(frame3, width=12, textvariable=name36)
    name_entered36.grid(column=1, row=2, padx=2, pady=4)

    a_label37 = ttk.Label(frame3, text="Quiet Value(V)")
    a_label37.grid(column=0, row=3, padx=2, pady=4)

    name_entered38 = ttk.Entry(frame3, width=12, textvariable=name38)
    name_entered38.grid(column=1, row=3, padx=2, pady=4)

    a_label39 = ttk.Label(frame3, text="Step1 Duration(ms)")
    a_label39.grid(column=0, row=4, padx=2, pady=4)

    name_entered39 = ttk.Entry(frame3, width=12, textvariable=name39)
    name_entered39.grid(column=1, row=4, padx=2, pady=4)

    a_label310 = ttk.Label(frame3, text="Step1 Value(V)")
    a_label310.grid(column=0, row=5, padx=2, pady=4)

    name_entered310 = ttk.Entry(frame3, width=12, textvariable=name310)
    name_entered310.grid(column=1, row=5, padx=2, pady=4)

    a_label311 = ttk.Label(frame3, text="Step2 Duration(ms)")
    a_label311.grid(column=0, row=6, padx=2, pady=4)

    name_entered311 = ttk.Entry(frame3, width=12, textvariable=name311)
    name_entered311.grid(column=1, row=6, padx=2, pady=4)

    a_label312 = ttk.Label(frame3, text="Step2 Value(V)")
    a_label312.grid(column=0, row=7, padx=2, pady=4)

    name_entered312 = ttk.Entry(frame3, width=12, textvariable=name312)
    name_entered312.grid(column=1, row=7, padx=2, pady=4)

    # frame4
    frame4 = tk.Frame(master, width=50, height=500)

    a_label43 = ttk.Label(frame4, text="Sample Rate(Hz)")
    a_label43.grid(column=0, row=1, padx=2, pady=4)

    name_entered44 = ttk.Entry(frame4, width=12, textvariable=name44)
    name_entered44.grid(column=1, row=1, padx=2, pady=4)

    a_label45 = ttk.Label(frame4, text="Quiet Time(ms)")
    a_label45.grid(column=0, row=2, padx=2, pady=4)

    name_entered46 = ttk.Entry(frame4, width=12, textvariable=name46)
    name_entered46.grid(column=1, row=2, padx=2, pady=4)

    a_label47 = ttk.Label(frame4, text="Quiet Value(V)")
    a_label47.grid(column=0, row=3, padx=2, pady=4)

    name_entered48 = ttk.Entry(frame4, width=12, textvariable=name48)
    name_entered48.grid(column=1, row=3, padx=2, pady=4)

    a_label49 = ttk.Label(frame4, text="Start Value(V)")
    a_label49.grid(column=0, row=4, padx=2, pady=4)

    name_entered49 = ttk.Entry(frame4, width=12, textvariable=name49)
    name_entered49.grid(column=1, row=4, padx=2, pady=4)

    a_label410 = ttk.Label(frame4, text="Final Value(V)")
    a_label410.grid(column=0, row=5, padx=2, pady=4)

    name_entered410 = ttk.Entry(frame4, width=12, textvariable=name410)
    name_entered410.grid(column=1, row=5, padx=2, pady=4)

    a_label411 = ttk.Label(frame4, text="Duration(ms)")
    a_label411.grid(column=0, row=6, padx=2, pady=4)

    name_entered411 = ttk.Entry(frame4, width=12, textvariable=name411)
    name_entered411.grid(column=1, row=6, padx=2, pady=4)

    # frame5
    frame5 = tk.Frame(master, width=50, height=500)

    a_label53 = ttk.Label(frame5, text="Sample Rate(Hz)")
    a_label53.grid(column=0, row=1, padx=2, pady=4)

    name_entered54 = ttk.Entry(frame5, width=12, textvariable=name54)
    name_entered54.grid(column=1, row=1, padx=2, pady=4)

    a_label55 = ttk.Label(frame5, text="Quiet Time(ms)")
    a_label55.grid(column=0, row=2, padx=2, pady=4)

    name_entered56 = ttk.Entry(frame5, width=12, textvariable=name56)
    name_entered56.grid(column=1, row=2, padx=2, pady=4)

    a_label57 = ttk.Label(frame5, text="Quiet Value(V)")
    a_label57.grid(column=0, row=3, padx=2, pady=4)

    name_entered58 = ttk.Entry(frame5, width=12, textvariable=name58)
    name_entered58.grid(column=1, row=3, padx=2, pady=4)

    a_label59 = ttk.Label(frame5, text="Cycles")
    a_label59.grid(column=0, row=4, padx=2, pady=4)

    name_entered59 = ttk.Entry(frame5, width=12, textvariable=name59)
    name_entered59.grid(column=1, row=4, padx=2, pady=4)

    a_label510 = ttk.Label(frame5, text="Amplitude(V)")
    a_label510.grid(column=0, row=5, padx=2, pady=4)

    name_entered511 = ttk.Entry(frame5, width=12, textvariable=name511)
    name_entered511.grid(column=1, row=5, padx=2, pady=4)

    a_label512 = ttk.Label(frame5, text="Offset(V)")
    a_label512.grid(column=0, row=6, padx=2, pady=4)

    name_entered512 = ttk.Entry(frame5, width=12, textvariable=name512)
    name_entered512.grid(column=1, row=6, padx=2, pady=4)

    a_label513 = ttk.Label(frame5, text="Shifs")
    a_label513.grid(column=0, row=7, padx=2, pady=4)

    name_entered513 = ttk.Entry(frame5, width=12, textvariable=name513)
    name_entered513.grid(column=1, row=7, padx=2, pady=4)

    a_label514 = ttk.Label(frame5, text="Period(ms)")
    a_label514.grid(column=0, row=7, padx=2, pady=4)

    name_entered514 = ttk.Entry(frame5, width=12, textvariable=name514)
    name_entered514.grid(column=1, row=7, padx=2, pady=4)

    ##################
    # frame6
    frame6 = tk.Frame(master, width=50, height=500)

    a_label60 = ttk.Label(frame6, text="Sample Rate(Hz)")
    a_label60.grid(column=0, row=1, padx=2, pady=4)

    name_entered60 = ttk.Entry(frame6, width=12, textvariable=name60)
    name_entered60.grid(column=1, row=1, padx=2, pady=4)

    a_label61 = ttk.Label(frame6, text="Quiet Time(ms)")
    a_label61.grid(column=0, row=2, padx=2, pady=4)

    name_entered62 = ttk.Entry(frame6, width=12, textvariable=name61)
    name_entered62.grid(column=1, row=2, padx=2, pady=4)

    a_label63 = ttk.Label(frame6, text="Quiet Value(V)")
    a_label63.grid(column=0, row=3, padx=2, pady=4)

    name_entered64 = ttk.Entry(frame6, width=12, textvariable=name62)
    name_entered64.grid(column=1, row=3, padx=2, pady=4)

    a_label65 = ttk.Label(frame6, text="Amplitude(V)")
    a_label65.grid(column=0, row=4, padx=2, pady=4)

    name_entered66 = ttk.Entry(frame6, width=12, textvariable=name63)
    name_entered66.grid(column=1, row=4, padx=2, pady=4)

    a_label67 = ttk.Label(frame6, text="StartValue(V)")
    a_label67.grid(column=0, row=5, padx=2, pady=4)

    name_entered68 = ttk.Entry(frame6, width=12, textvariable=name64)
    name_entered68.grid(column=1, row=5, padx=2, pady=4)

    a_label69 = ttk.Label(frame6, text="FinalValue(V)")
    a_label69.grid(column=0, row=6, padx=2, pady=4)

    name_entered610 = ttk.Entry(frame6, width=12, textvariable=name65)
    name_entered610.grid(column=1, row=6, padx=2, pady=4)

    a_label611 = ttk.Label(frame6, text="StepValue(V)")
    a_label611.grid(column=0, row=7, padx=2, pady=4)

    name_entered612 = ttk.Entry(frame6, width=12, textvariable=name66)
    name_entered612.grid(column=1, row=7, padx=2, pady=4)

    a_label613 = ttk.Label(frame6, text="Window")
    a_label613.grid(column=0, row=8, padx=2, pady=4)

    name_entered614 = ttk.Entry(frame6, width=12, textvariable=name67)
    name_entered614.grid(column=1, row=8, padx=2, pady=4)

    botton1 = ttk.Button(mighty1, width=8, text='RUN', command=Starting)
    botton1.grid(column=0, row=2, padx=2, pady=4)

    botton2 = ttk.Button(mighty1, width=8, text='STOP', command=Stop)
    botton2.grid(column=1, row=2, padx=2, pady=4)

    botton2 = ttk.Button(mighty1, width=8, text='CLEAR', command=Clear)
    botton2.grid(column=2, row=2, padx=2, pady=4)

    # Adding a Button
    botton3 = ttk.Button(mighty1, width=8, text='Save Data', command=savefile)
    botton3.grid(column=0, row=0, padx=2, pady=4, )

    global val1
    val1 = tk.StringVar()
    l = tk.Label(mighty1, bg="white", fg="black", width=20, textvariable=val1)
    l.grid(column=1, row=0, columnspan=4, pady=2)


#########################################################
finish = False
def Starting():
    plt.close()
    # sleep(0.1)
    run_potentiostat()
    # finish =True

def Stop():
    # progress_bar.stop()
    sleep(0.1)
    plt.close()
    sleep(0.1)
    if dev.isOpen() and dev.test_running:
        dev.stop_test()
    sleep(0.1)
    # dev.close()

def Clear():
    dev.close()
    sleep(0.1)

first(tab1)


# Exit GUI cleanly
def _quit():
    win.quit()
    win.destroy()
    exit()


def _msgBox0():
    msg.showinfo('', 'Welcome to use this smart Electrochemical Potentiostat!'
                     '\n If any question, please contact aqchen@hdu.edu.cn.')


# Creating a Menu Bar
menu_bar = Menu(win)
win.config(menu=menu_bar)

# Add menu items
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=_quit)
menu_bar.add_cascade(label="File", menu=file_menu)

# Add another Menu to the Menu Bar and an item
help_menu = Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About", command=_msgBox0)
menu_bar.add_cascade(label="Help", menu=help_menu)

# name_entered.focus()  # Place cursor into name Entry


win.mainloop()

