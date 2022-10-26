#
# Serial.py
#
# Author: Nicholas Ball
#
# This file is used as the interface into handling serial communication to and
# from the radio
#
from Device import *
import numpy as np
import os
from Modulation import *
import threading


class Serial(object):
    """

    Serial is the heart of orbital coms and the 'hypervisor' of all things to
    with the radio such as (de)mod, encryption, and much more!

    """

    nope_counter = 0

    # Serial is a sigleton (Only has one instance of itself)
    def __new__(self,rx_freqency,tx_freqency,rx_channel,tx_channel,rx_gain,tx_gain):
        if not hasattr(self, 'instance'):
            # Set instance
            self.instance = super(Serial, self).__new__(self)

        return self.instance


    # This will put radio into standby and look for a radio and will hold the
    # thread till it gets a connection with another radio
    def connect(self):
        pass

    def disconnect(self):
        pass

    def tx(self,data):
        c = np.array(list(data))
        c.tofile("out.txt")
        os.system("python3 tx.py")
        os.system("\n")

    def rx(self):
        os.system("python3 rx.py > blank.txt")
        os.system("\n")
        f = np.fromfile(open("in.txt"), dtype=np.uint8)
        out = np.transpose(((f != 0) & (f != 255)).nonzero())
        try:
            hold = f[out[0][0]]
            return False
        except Exception as e:
            nope_counter += 1

            if nope_counter == 180:
                return True


    def get_debug(self):
        pass
