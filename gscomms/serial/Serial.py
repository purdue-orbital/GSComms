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

    def rx(self):
        np.set_printoptions(threshold=600000)
        print("Reading...")
        f = np.fromfile(open("in.txt"), dtype=np.uint8)
        print("Printing...")
        out = np.transpose(((f != 0) & (f != 255)).nonzero())
        hold = (f[out[0][0] : out[0][0] + 6000])

        m = 8
        a = (((hold[:,None] & (1 << np.arange(m)))) > 0).astype(int)
        b = ''.join(''.join('%d' %x for x in y) for y in a)

        file = open("bin.txt","w+")
        file.write(b)
        file.close()

    def get_debug(self):
        pass
