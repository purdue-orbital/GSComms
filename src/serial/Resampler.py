#
# Resampler.py
#
# Author: Nicholas Ball
#
# This file will resample the data  at a lower or same rate as the device being
# read from to create data over time
#

import Device
import threading
import time
import numpy as np
import ctypes

Arr = []

class Resampler(object):
    """Resampler will take in data points from the radio and make the data over time"""

    def __init__(self):
        super(Resampler, self).__init__()

        # Fetch the radio
        self.Radio = Device.Device()

        # Make the array of data points
        # self.arr = []
        self.arr = []

        self.i = 0

    def sample(self):
        out = self.Radio.read()

        print(out)

        # Take sample
        self.arr.append(out)

    # Run sampling in a loop
    def sample_run(self,sample_rate):
        while True:
            self.sample()
    # return array of sampled data
    def get_arr(self):
        return self.arr

    # start resampling in another thread
    def run(self,sample_rate):
        threading.Thread(target=self.sample_run,args=(sample_rate,)).start()
