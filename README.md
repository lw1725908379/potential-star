# potential-start

#### 介绍
基于teensy 3.2 开发板实现的定制化电化学测试小程序，功能包括：循环伏安测试（cv）、Cdl测试、lsv测试、tafel测试、i-t测试等功能。

### Python interface to IO Rodeo's Potentiostat Shield for the teensy 3.2 development board.


### Example

#!python

from potentiostat import Potentiostat

dev = Potentiostat('/dev/ttyACM0')
dev.set_curr_range('100uA')
dev.set_sample_period(10)

name = 'cyclic'
param = {
        'quietValue' : 0.0,
        'quietTime'  : 1000,
        'amplitude'  : 2.0,
        'offset'     : 0.0,
        'period'     : 1000,
        'numCycles'  : 5,
        'shift'      : 0.0,
        }

dev.set_param(name,param)
t,volt,curr = dev.run_test(name,display='pbar')

### Installation
#!bash

$ pip install iorodeo-potentiostat

### Links
* Documentation https://potentiostat.iorodeo.com
* Download https://bitbucket.org/iorodeo/potentiostat


