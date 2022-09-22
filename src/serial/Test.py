#
# Test.py
#
# Author: Nicholas Ball
#
# This file will handle testing the serial class
#

from Device import *
from Resampler import Resampler
import time
import matplotlib.pyplot as plt
import numpy as np
import os

#-------------------------------------------------------------------------------
# Configuration
#-------------------------------------------------------------------------------

rx_sample_rate = 4e6 # Freqency at which the radio samples waves
freqency       = 1e6 # Freqency at which the radio will read
sample_size    = int(4e6) # Number of data points to collect
num_data       = 40 # Number of data points to be displayed on the graph


#-------------------------------------------------------------------------------
# Collect data points
#-------------------------------------------------------------------------------

# Start radio
d = Device()
d.get()
d.start(RX,rx_sample_rate,freqency,0,sample_size)

# Read data
d.read()
s = d.get_arr()

# End stream
d.stop(RX)

#-------------------------------------------------------------------------------
# Display data points
#-------------------------------------------------------------------------------

plt.figure(num=1, figsize=(12.95, 7.8), dpi=150)
plt.subplot(211)
s = np.split(s,sample_size/num_data)[0]
t_us = np.arange(num_data) / freqency / 1e-6
plt.plot(t_us, s.real, 'k', label='I')
plt.plot(t_us, s.imag, 'r', label='Q')
plt.xlim(t_us[0], t_us[-1])
plt.xlabel('Time (us)')
plt.ylabel('Normalized Amplitude')

plt.show()

os._exit(1)
