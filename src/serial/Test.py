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


d = Device()

d.get()

d.start(RX,10e6,10e6,0)

rs = Resampler()
rs.run(2.5e6)

time.sleep(1)

d.stop(RX)

print(len(rs.get_arr()))

os._exit(1)
