#
# File: Serial.py
#
# Author(s): Nicholas Ball
#
# Description: This file will be directly interfaced for communication to and
# from the radio
#
import Device
from Modulation import *


Frequency  = int(915e6)
Channel    = 0
Gain       = 64
SampleRate = int(32e3)

counter = 0

class Serial(object):
    """Serial is the interface for sending and listening for radio transmissions"""

    def __init__(self):
        super(Serial, self).__init__()
        self.Device = Device.Device()

    def TX(self,data):
        '''
        Pass a string to be transmitted from the radio
        '''
        # add SOF and EOF to string
        #data = "<SOF>"+data+"<EOF>"
        #data = "1"

        # string to ascii values
        #asciis = [ord(char) for char in data]

        # Ascii to binary
        #bin = [str(np.binary_repr(ascii, width=8)) for ascii in asciis]

        #bin = np.array(list(''.join(bin)))
        #bin = bin.astype(int)
        #print(''.join(map(str, bin)))


        # Modulate data
        bin = np.array([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])
        out = Mod(bin,Frequency)

        self.Device.TX(out)

    def RX(self):
        '''
        This will return all collected data that was transmitted
        '''

        # Demod collected data
        out = Demod(self.Device.RX())

        # if a transmission was not detected, increase counter
        if not(1 in out):
            counter += 1
        else:
            counter = 0

        # after 5 minutes of no connection, return true
        if counter >= 300:
            return True
        else:
            return False


        #return (''.join(map(str, out)))
